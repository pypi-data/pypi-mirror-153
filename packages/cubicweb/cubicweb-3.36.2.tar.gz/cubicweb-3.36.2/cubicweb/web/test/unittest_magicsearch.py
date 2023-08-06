# copyright 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.
"""Unit tests for cw.web.views.magicsearch"""

from contextlib import contextmanager

from logilab.common.testlib import unittest_main
from rql import BadRQLQuery, RQLSyntaxError

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.web.views.magicsearch import (
    QSPreProcessor,
    QueryTranslator,
)

translations = {
    "CWUser": "Utilisateur",
    "EmailAddress": "Adresse",
    "name": "nom",
    "alias": "nom",
    "surname": "nom",
    "firstname": "prÃ©nom",
    "state": "Ã©tat",
    "address": "adresse",
    "use_email": "adel",
}


def _translate(msgid):
    return translations.get(msgid, msgid)


def _ctxtranslate(ctx, msgid):
    return _translate(msgid)


class QueryTranslatorTC(CubicWebTC):
    """test suite for QueryTranslatorTC"""

    @contextmanager
    def proc(self):
        with self.admin_access.web_request() as req:
            self.vreg.config.translations = {"en": (_translate, _ctxtranslate)}
            proc = self.vreg["components"].select("magicsearch", req)
            proc = [p for p in proc.processors if isinstance(p, QueryTranslator)][0]
            yield proc

    def test_basic_translations(self):
        """tests basic translations (no ambiguities)"""
        with self.proc() as proc:
            rql = "Any C WHERE C is Adresse, P adel C, C adresse 'Logilab'"
            (rql,) = proc.preprocess_query(rql)
            self.assertEqual(
                rql, 'Any C WHERE C is EmailAddress, P use_email C, C address "Logilab"'
            )

    def test_ambiguous_translations(self):
        """tests possibly ambiguous translations"""
        with self.proc() as proc:
            rql = "Any P WHERE P adel C, C is EmailAddress, C nom 'Logilab'"
            (rql,) = proc.preprocess_query(rql)
            self.assertEqual(
                rql, 'Any P WHERE P use_email C, C is EmailAddress, C alias "Logilab"'
            )
            rql = "Any P WHERE P is Utilisateur, P adel C, P nom 'Smith'"
            (rql,) = proc.preprocess_query(rql)
            self.assertEqual(
                rql, 'Any P WHERE P is CWUser, P use_email C, P surname "Smith"'
            )


class QSPreProcessorTC(CubicWebTC):
    """test suite for QSPreProcessor"""

    @contextmanager
    def proc(self):
        self.vreg.config.translations = {"en": (_translate, _ctxtranslate)}
        with self.admin_access.web_request() as req:
            proc = self.vreg["components"].select("magicsearch", req)
            proc = [p for p in proc.processors if isinstance(p, QSPreProcessor)][0]
            proc._cw = req
            yield proc

    def test_entity_translation(self):
        """tests QSPreProcessor._get_entity_name()"""
        with self.proc() as proc:
            translate = proc._get_entity_type
            self.assertEqual(translate("EmailAddress"), "EmailAddress")
            self.assertEqual(translate("emailaddress"), "EmailAddress")
            self.assertEqual(translate("Adresse"), "EmailAddress")
            self.assertEqual(translate("adresse"), "EmailAddress")
            self.assertRaises(BadRQLQuery, translate, "whatever")

    def test_attribute_translation(self):
        """tests QSPreProcessor._get_attribute_name"""
        with self.proc() as proc:
            translate = proc._get_attribute_name
            eschema = self.schema.entity_schema_for("CWUser")
            self.assertEqual(translate("prÃ©nom", eschema), "firstname")
            self.assertEqual(translate("nom", eschema), "surname")
            eschema = self.schema.entity_schema_for("EmailAddress")
            self.assertEqual(translate("adresse", eschema), "address")
            self.assertEqual(translate("nom", eschema), "alias")
            # should fail if the name is not an attribute for the given entity schema
            self.assertRaises(BadRQLQuery, translate, "whatever", eschema)
            self.assertRaises(BadRQLQuery, translate, "prÃ©nom", eschema)

    def test_one_word_query(self):
        """tests the 'one word shortcut queries'"""
        with self.proc() as proc:
            transform = proc._one_word_query
            self.assertEqual(
                transform("123"), ("Any X WHERE X eid %(x)s", {"x": 123}, "x")
            )
            self.assertEqual(transform("CWUser"), ("CWUser C",))
            self.assertEqual(transform("Utilisateur"), ("CWUser C",))
            self.assertEqual(transform("Adresse"), ("EmailAddress E",))
            self.assertEqual(transform("adresse"), ("EmailAddress E",))
            self.assertRaises(BadRQLQuery, transform, "Workcases")

    def test_two_words_query(self):
        """tests the 'two words shortcut queries'"""
        with self.proc() as proc:
            transform = proc._two_words_query
            self.assertEqual(transform("CWUser", "E"), ("CWUser E",))
            self.assertEqual(
                transform("CWUser", "Smith"),
                (
                    "CWUser C ORDERBY FTIRANK(C) DESC WHERE C has_text %(text)s",
                    {"text": "Smith"},
                ),
            )
            self.assertEqual(
                transform("utilisateur", "Smith"),
                (
                    "CWUser C ORDERBY FTIRANK(C) DESC WHERE C has_text %(text)s",
                    {"text": "Smith"},
                ),
            )
            self.assertEqual(
                transform("adresse", "Logilab"),
                (
                    "EmailAddress E ORDERBY FTIRANK(E) DESC WHERE E has_text %(text)s",
                    {"text": "Logilab"},
                ),
            )
            self.assertEqual(
                transform("adresse", "Logi%"),
                ("EmailAddress E WHERE E alias LIKE %(text)s", {"text": "Logi%"}),
            )
            self.assertRaises(BadRQLQuery, transform, "pers", "taratata")

    def test_three_words_query(self):
        """tests the 'three words shortcut queries'"""
        with self.proc() as proc:
            transform = proc._three_words_query
            self.assertEqual(
                transform("utilisateur", "prÃ©nom", "cubicweb"),
                ("CWUser C WHERE C firstname %(text)s", {"text": "cubicweb"}),
            )
            self.assertEqual(
                transform("utilisateur", "nom", "cubicweb"),
                ("CWUser C WHERE C surname %(text)s", {"text": "cubicweb"}),
            )
            self.assertEqual(
                transform("adresse", "nom", "cubicweb"),
                ("EmailAddress E WHERE E alias %(text)s", {"text": "cubicweb"}),
            )
            self.assertEqual(
                transform("EmailAddress", "nom", "cubicweb"),
                ("EmailAddress E WHERE E alias %(text)s", {"text": "cubicweb"}),
            )
            self.assertEqual(
                transform("utilisateur", "prÃ©nom", "cubicweb%"),
                ("CWUser C WHERE C firstname LIKE %(text)s", {"text": "cubicweb%"}),
            )
            # expanded shortcuts
            self.assertEqual(
                transform("CWUser", "use_email", "Logilab"),
                (
                    "CWUser C ORDERBY FTIRANK(C1) DESC WHERE C use_email C1, C1 has_text %(text)s",
                    {"text": "Logilab"},
                ),
            )
            self.assertEqual(
                transform("CWUser", "use_email", "%Logilab"),
                (
                    "CWUser C WHERE C use_email C1, C1 alias LIKE %(text)s",
                    {"text": "%Logilab"},
                ),
            )
            self.assertRaises(BadRQLQuery, transform, "word1", "word2", "word3")

    def test_quoted_queries(self):
        """tests how quoted queries are handled"""
        queries = [
            (
                'Adresse "My own EmailAddress"',
                (
                    "EmailAddress E ORDERBY FTIRANK(E) DESC WHERE E has_text %(text)s",
                    {"text": "My own EmailAddress"},
                ),
            ),
            (
                'Utilisateur prÃ©nom "Jean Paul"',
                ("CWUser C WHERE C firstname %(text)s", {"text": "Jean Paul"}),
            ),
            (
                'Utilisateur firstname "Jean Paul"',
                ("CWUser C WHERE C firstname %(text)s", {"text": "Jean Paul"}),
            ),
            (
                'CWUser firstname "Jean Paul"',
                ("CWUser C WHERE C firstname %(text)s", {"text": "Jean Paul"}),
            ),
        ]
        with self.proc() as proc:
            transform = proc._quoted_words_query
            for query, expected in queries:
                self.assertEqual(transform(query), expected)
            self.assertRaises(BadRQLQuery, transform, "unquoted rql")
            self.assertRaises(BadRQLQuery, transform, 'pers "Jean Paul"')
            self.assertRaises(
                BadRQLQuery, transform, 'CWUser firstname other "Jean Paul"'
            )

    def test_process_query(self):
        """tests how queries are processed"""
        queries = [
            ("Utilisateur", ("CWUser C",)),
            ("Utilisateur P", ("CWUser P",)),
            (
                "Utilisateur cubicweb",
                (
                    "CWUser C ORDERBY FTIRANK(C) DESC WHERE C has_text %(text)s",
                    {"text": "cubicweb"},
                ),
            ),
            (
                "CWUser prÃ©nom cubicweb",
                (
                    "CWUser C WHERE C firstname %(text)s",
                    {"text": "cubicweb"},
                ),
            ),
        ]
        with self.proc() as proc:
            for query, expected in queries:
                self.assertEqual(proc.preprocess_query(query), expected)
            self.assertRaises(
                BadRQLQuery, proc.preprocess_query, "Any X WHERE X is Something"
            )


# Processor Chains tests ############################################


class ProcessorChainTC(CubicWebTC):
    """test suite for magic_search's processor chains"""

    @contextmanager
    def proc(self):
        self.vreg.config.translations = {"en": (_translate, _ctxtranslate)}
        with self.admin_access.web_request() as req:
            proc = self.vreg["components"].select("magicsearch", req)
            yield proc

    def test_main_preprocessor_chain(self):
        """tests QUERY_PROCESSOR"""
        queries = [
            (
                "foo",
                (
                    "Any X ORDERBY FTIRANK(X) DESC WHERE X has_text %(text)s",
                    {"text": "foo"},
                ),
            ),
            # XXX this sounds like a language translator test...
            # and it fails
            (
                "Utilisateur Smith",
                (
                    "CWUser C ORDERBY FTIRANK(C) DESC WHERE C has_text %(text)s",
                    {"text": "Smith"},
                ),
            ),
            (
                "utilisateur nom Smith",
                ("CWUser C WHERE C surname %(text)s", {"text": "Smith"}),
            ),
            (
                'Any P WHERE P is Utilisateur, P nom "Smith"',
                ('Any P WHERE P is CWUser, P surname "Smith"', None),
            ),
        ]
        with self.proc() as proc:
            for query, expected in queries:
                rset = proc.process_query(query)
                self.assertEqual((rset.rql, rset.args), expected)

    def test_accentuated_fulltext(self):
        """we must be able to type accentuated characters in the search field"""
        with self.proc() as proc:
            rset = proc.process_query("écrire")
            self.assertEqual(
                rset.rql, "Any X ORDERBY FTIRANK(X) DESC WHERE X has_text %(text)s"
            )
            self.assertEqual(rset.args, {"text": "écrire"})

    def test_explicit_component(self):
        with self.proc() as proc:
            self.assertRaises(
                RQLSyntaxError,
                proc.process_query,
                'rql: CWUser E WHERE E noattr "Smith",',
            )
            self.assertRaises(
                BadRQLQuery, proc.process_query, 'rql: CWUser E WHERE E noattr "Smith"'
            )
            rset = proc.process_query("text: utilisateur Smith")
            self.assertEqual(
                rset.rql, "Any X ORDERBY FTIRANK(X) DESC WHERE X has_text %(text)s"
            )
            self.assertEqual(rset.args, {"text": "utilisateur Smith"})


if __name__ == "__main__":
    unittest_main()
