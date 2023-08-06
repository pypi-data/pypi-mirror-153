# copyright 2003-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

from datetime import datetime
from threading import Thread

import logilab.database as lgdb
from unittest_querier import FixedOffset

from cubicweb import ValidationError
from cubicweb.devtools import (
    PostgresApptestConfiguration,
    startpgcluster,
    stoppgcluster,
)
from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.entities.adapters import IFTIndexableAdapter
from cubicweb.predicates import is_instance


def setUpModule():
    startpgcluster(__file__)


def tearDownModule():
    stoppgcluster(__file__)


class PostgresTimeoutConfiguration(PostgresApptestConfiguration):
    def __init__(self, *args, **kwargs):
        self.default_sources = PostgresApptestConfiguration.default_sources.copy()
        self.default_sources["system"] = PostgresApptestConfiguration.default_sources[
            "system"
        ].copy()
        self.default_sources["system"]["db-statement-timeout"] = 200
        super().__init__(*args, **kwargs)


class PostgresFTITC(CubicWebTC):
    configcls = PostgresApptestConfiguration

    def test_eid_range(self):
        # concurrent allocation of eid ranges
        source = self.repo.system_source
        range1 = []
        range2 = []

        def allocate_eid_ranges(session, target):
            for x in range(1, 10):
                eid = source.create_eid(session, count=x)
                target.extend(range(eid - x, eid))

        t1 = Thread(target=lambda: allocate_eid_ranges(self.session, range1))
        t2 = Thread(target=lambda: allocate_eid_ranges(self.session, range2))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertEqual(range1, sorted(range1))
        self.assertEqual(range2, sorted(range2))
        self.assertEqual(set(), set(range1) & set(range2))

    def test_occurence_count(self):
        with self.admin_access.repo_cnx() as cnx:
            c1 = cnx.create_entity(
                "Card", title="c1", content="cubicweb cubicweb cubicweb"
            )
            c2 = cnx.create_entity("Card", title="c3", content="cubicweb")
            c3 = cnx.create_entity("Card", title="c2", content="cubicweb cubicweb")
            cnx.commit()
            self.assertEqual(
                cnx.execute(
                    "Card X ORDERBY FTIRANK(X) DESC " 'WHERE X has_text "cubicweb"'
                ).rows,
                [
                    [
                        c1.eid,
                    ],
                    [
                        c3.eid,
                    ],
                    [
                        c2.eid,
                    ],
                ],
            )

    def test_attr_weight(self):
        class CardIFTIndexableAdapter(IFTIndexableAdapter):
            __select__ = is_instance("Card")
            attr_weight = {"title": "A"}

        with self.temporary_appobjects(CardIFTIndexableAdapter):
            with self.admin_access.repo_cnx() as cnx:
                c1 = cnx.create_entity(
                    "Card", title="c1", content="cubicweb cubicweb cubicweb"
                )
                c2 = cnx.create_entity("Card", title="c2", content="cubicweb cubicweb")
                c3 = cnx.create_entity("Card", title="cubicweb", content="autre chose")
                cnx.commit()
                self.assertEqual(
                    cnx.execute(
                        "Card X ORDERBY FTIRANK(X) DESC " 'WHERE X has_text "cubicweb"'
                    ).rows,
                    [
                        [
                            c3.eid,
                        ],
                        [
                            c1.eid,
                        ],
                        [
                            c2.eid,
                        ],
                    ],
                )

    def test_entity_weight(self):
        class PersonneIFTIndexableAdapter(IFTIndexableAdapter):
            __select__ = is_instance("Personne")
            entity_weight = 2.0

        with self.temporary_appobjects(PersonneIFTIndexableAdapter):
            with self.admin_access.repo_cnx() as cnx:
                c1 = cnx.create_entity("Personne", nom="c1", prenom="cubicweb")
                c2 = cnx.create_entity(
                    "Comment", content="cubicweb cubicweb", comments=c1
                )
                c3 = cnx.create_entity(
                    "Comment", content="cubicweb cubicweb cubicweb", comments=c1
                )
                cnx.commit()
                self.assertEqual(
                    cnx.execute(
                        "Any X ORDERBY FTIRANK(X) DESC " 'WHERE X has_text "cubicweb"'
                    ).rows,
                    [
                        [
                            c1.eid,
                        ],
                        [
                            c3.eid,
                        ],
                        [
                            c2.eid,
                        ],
                    ],
                )

    def test_tz_datetime(self):
        with self.admin_access.repo_cnx() as cnx:
            bob = cnx.create_entity(
                "Personne",
                nom="bob",
                tzdatenaiss=datetime(1977, 6, 7, 2, 0, tzinfo=FixedOffset(1)),
            )
            datenaiss = cnx.execute("Any XD WHERE X nom 'bob', X tzdatenaiss XD")[0][0]
            self.assertIsNotNone(datenaiss.tzinfo)
            self.assertEqual(datenaiss.utctimetuple()[:5], (1977, 6, 7, 1, 0))
            cnx.commit()
            cnx.create_entity(
                "Personne", nom="boby", tzdatenaiss=datetime(1977, 6, 7, 2, 0)
            )
            datenaiss = cnx.execute("Any XD WHERE X nom 'boby', X tzdatenaiss XD")[0][0]
            self.assertIsNotNone(datenaiss.tzinfo)
            self.assertEqual(datenaiss.utctimetuple()[:5], (1977, 6, 7, 2, 0))
            rset = cnx.execute(
                "Any X WHERE X tzdatenaiss %(d)s",
                {"d": datetime(1977, 6, 7, 2, 0, tzinfo=FixedOffset(1))},
            )
            self.assertEqual(rset.rows, [[bob.eid]])

    def test_constraint_validationerror(self):
        with self.admin_access.repo_cnx() as cnx:
            with cnx.allow_all_hooks_but("integrity"):
                with self.assertRaises(ValidationError) as cm:
                    cnx.execute("INSERT Note N: N type 'nogood'")
                self.assertEqual(
                    cm.exception.errors,
                    {
                        "type-subject": "invalid value %(KEY-value)s, it must be one of %(KEY-choices)s"
                    },
                )
                self.assertEqual(
                    cm.exception.msgargs,
                    {
                        "type-subject-value": '"nogood"',
                        "type-subject-choices": '"todo", "a", "b", "T", "lalala"',
                    },
                )


class PostgresStatementTimeoutTC(CubicWebTC):
    configcls = PostgresTimeoutConfiguration

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.orig_connect_hooks = lgdb.SQL_CONNECT_HOOKS["postgres"][:]

    @classmethod
    def tearDownClass(cls):
        lgdb.SQL_CONNECT_HOOKS["postgres"] = cls.orig_connect_hooks

    def test_statement_timeout(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.system_sql("select pg_sleep(0.1)")
            with self.assertRaises(Exception) as cm:
                cnx.system_sql("select pg_sleep(0.3)")
        self.assertIn("statement timeout", str(cm.exception))


class PostgresLimitSizeTC(CubicWebTC):
    configcls = PostgresApptestConfiguration

    def test(self):
        with self.admin_access.repo_cnx() as cnx:

            def sql(string):
                return cnx.system_sql(string).fetchone()[0]

            for html, size, expected in [
                ("<p>hello</p>", 20, "<p>hello</p>"),
                ("<p>hello</p>", 2, "he..."),
                ("<br/>hello", 2, "he..."),
                ('<span class="1">he</span>llo', 2, "he..."),
                ("<span>a>b</span>", 2, "a>..."),
            ]:
                with self.subTest(html=html, size=size):
                    actual = sql(
                        "SELECT limit_size('%s', 'text/html', %d)" % (html, size)
                    )
                    self.assertEqual(actual, expected)


class PostgresGroupConcatTC(CubicWebTC):
    configcls = PostgresApptestConfiguration

    def test(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.create_entity("Personne", nom="ABC_1", prenom="Alice")
            cnx.create_entity("Personne", nom="ABC_2", prenom="Alice")
            cnx.create_entity("Personne", nom="ABC", prenom="Bob")
            cnx.create_entity("Personne", nom="ABC")

            cnx.commit()

            firstnames_rset = cnx.execute(
                "Any GROUP_CONCAT(P) WHERE X is Personne, X prenom P"
            )

            # spy's firstname is null, it should not appear in the result
            self.assertEqual(list(firstnames_rset), [["Alice, Bob"]])

            lastnames_rset = cnx.execute(
                "Any GROUP_CONCAT(N) WHERE X is Personne, X nom N"
            )

            # ABC should appear only once
            self.assertEqual(list(lastnames_rset), [["ABC_1, ABC_2, ABC"]])


if __name__ == "__main__":
    import unittest

    unittest.main()
