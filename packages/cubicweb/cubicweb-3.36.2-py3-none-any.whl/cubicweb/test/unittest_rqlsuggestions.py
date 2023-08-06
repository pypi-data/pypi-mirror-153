# copyright 2021 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Unit tests for cw.rqlsuggestions"""

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.rqlsuggestions import RQLSuggestionsBuilder


class RQLSuggestionsBuilderTC(CubicWebTC):
    def suggestions(self, rql):
        with self.admin_access.web_request() as req:
            suggestions_builder = RQLSuggestionsBuilder(req)
            return suggestions_builder.build_suggestions(rql)

    def test_no_restrictions_rql(self):
        self.assertListEqual([], self.suggestions(""))
        self.assertListEqual([], self.suggestions("An"))
        self.assertListEqual([], self.suggestions("Any X"))
        self.assertListEqual([], self.suggestions("Any X, Y"))

    def test_invalid_rql(self):
        self.assertListEqual([], self.suggestions("blabla"))
        self.assertListEqual([], self.suggestions("Any X WHERE foo, bar"))

    def test_is_rql(self):
        self.assertListEqual(
            [
                "Any X WHERE X is %s" % eschema
                for eschema in sorted(self.vreg.schema.entities())
                if not eschema.final
            ],
            self.suggestions("Any X WHERE X is"),
        )

        self.assertListEqual(
            ["Any X WHERE X is Personne", "Any X WHERE X is Produit"],
            self.suggestions("Any X WHERE X is P"),
        )

        self.assertListEqual(
            [
                "Any X WHERE X is Personne, Y is Personne",
                "Any X WHERE X is Personne, Y is Produit",
            ],
            self.suggestions("Any X WHERE X is Personne, Y is P"),
        )

    def test_relations_rql(self):
        self.assertListEqual(
            [
                "Any X WHERE X is Personne, X actionnaire A",
                "Any X WHERE X is Personne, X associe A",
                "Any X WHERE X is Personne, X connait A",
                "Any X WHERE X is Personne, X dirige A",
                "Any X WHERE X is Personne, X evaluee A",
                "Any X WHERE X is Personne, X nom A",
                "Any X WHERE X is Personne, X prenom A",
                "Any X WHERE X is Personne, X promo A",
                "Any X WHERE X is Personne, X travaille A",
                "Any X WHERE X is Personne, X type A",
            ],
            self.suggestions("Any X WHERE X is Personne, X "),
        )
        self.assertListEqual(
            [
                "Any X WHERE X is Personne, X travaille A",
                "Any X WHERE X is Personne, X type A",
            ],
            self.suggestions("Any X WHERE X is Personne, X t"),
        )
        # try completion on selected
        self.assertListEqual(
            [
                "Any X WHERE X is Personne, Y is Societe, X travaille Y",
                "Any X WHERE X is Personne, Y is Societe, X type A",
            ],
            self.suggestions("Any X WHERE X is Personne, Y is Societe, X t"),
        )
        # invalid relation should not break
        self.assertListEqual(
            [], self.suggestions("Any X WHERE X is Personne, X asdasd")
        )

    def test_attribute_vocabulary_rql(self):
        self.assertListEqual(
            [
                'Any X WHERE X is Personne, X promo "bon"',
                'Any X WHERE X is Personne, X promo "pasbon"',
            ],
            self.suggestions('Any X WHERE X is Personne, X promo "'),
        )
        self.assertListEqual(
            [
                'Any X WHERE X is Personne, X promo "pasbon"',
            ],
            self.suggestions('Any X WHERE X is Personne, X promo "p'),
        )
        # "bon" should be considered complete, hence no suggestion
        self.assertListEqual(
            [], self.suggestions('Any X WHERE X is Personne, X promo "bon"')
        )
        # no valid vocabulary starts with "po"
        self.assertListEqual(
            [], self.suggestions('Any X WHERE X is Personne, X promo "po')
        )

    def test_attribute_value_rql(self):
        # suggestions should contain any possible value for
        # a given attribute (limited to 10)
        with self.admin_access.web_request() as req:
            for i in range(15):
                req.create_entity("Personne", nom="n%s" % i, prenom="p%s" % i)
            req.cnx.commit()
        self.assertListEqual(
            [
                'Any X WHERE X is Personne, X nom "n0"',
                'Any X WHERE X is Personne, X nom "n1"',
                'Any X WHERE X is Personne, X nom "n10"',
                'Any X WHERE X is Personne, X nom "n11"',
                'Any X WHERE X is Personne, X nom "n12"',
                'Any X WHERE X is Personne, X nom "n13"',
                'Any X WHERE X is Personne, X nom "n14"',
                'Any X WHERE X is Personne, X nom "n2"',
                'Any X WHERE X is Personne, X nom "n3"',
                'Any X WHERE X is Personne, X nom "n4"',
                'Any X WHERE X is Personne, X nom "n5"',
                'Any X WHERE X is Personne, X nom "n6"',
                'Any X WHERE X is Personne, X nom "n7"',
                'Any X WHERE X is Personne, X nom "n8"',
                'Any X WHERE X is Personne, X nom "n9"',
            ],
            self.suggestions('Any X WHERE X is Personne, X nom "'),
        )
        self.assertListEqual(
            [
                'Any X WHERE X is Personne, X nom "n1"',
                'Any X WHERE X is Personne, X nom "n10"',
                'Any X WHERE X is Personne, X nom "n11"',
                'Any X WHERE X is Personne, X nom "n12"',
                'Any X WHERE X is Personne, X nom "n13"',
                'Any X WHERE X is Personne, X nom "n14"',
            ],
            self.suggestions('Any X WHERE X is Personne, X nom "n1'),
        )
