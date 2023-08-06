# copyright 2003-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""functional tests for fast_drop_entities"""

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.misc.scripts.fast_drop_entities import (
    fast_drop_entities,
    _compute_impacted_entities_and_relations_to_delete,
)


class FastDropEntitiesTC(CubicWebTC):
    def test_simple_deletion(self):
        with self.admin_access.repo_cnx() as cnx:
            for letter in "abc":
                cnx.execute(
                    "INSERT Ami X: X nom %(n)s, X prenom %(p)s",
                    {"n": letter.upper(), "p": letter},
                )

            cnx.commit()

            self.assertEqual(len(cnx.find("Ami")), 3)

            fast_drop_entities(cnx.find("Ami"))

            self.assertEqual(len(cnx.find("Ami")), 0)

    def test_deletion_with_inlined_relation(self):
        with self.admin_access.repo_cnx() as cnx:
            u = cnx.create_entity("Usine", lieu="Paris")
            p = cnx.create_entity("Produit", fabrique_par=u)
            cnx.commit()

            self.assertEqual(p.fabrique_par, (u,))

            fast_drop_entities(cnx.find("Usine"))

            self.assertEqual(len(cnx.find("Usine")), 0)
            self.assertEqual(cnx.find("Produit").one().fabrique_par, ())

    def test_deletion_with_relation(self):
        with self.admin_access.repo_cnx() as cnx:
            alfred = cnx.create_entity("Personne", nom="Alfred")
            tag = cnx.create_entity("Tag", name="A Tag", tags=alfred)
            cnx.commit()

            self.assertEqual(alfred.reverse_tags, (tag,))

            fast_drop_entities(cnx.find("Personne"))

            self.assertEqual(len(cnx.find("Personne")), 0)
            self.assertEqual(cnx.find("Tag", name="A Tag").one().tags, ())

    def test_deletion_with_composites(self):
        with self.admin_access.repo_cnx() as cnx:
            abc = cnx.create_entity("Ami", nom="ABC")
            comment_ABC = cnx.create_entity("Comment", content="ABC", comments=abc)
            comment_about_ABC = cnx.create_entity(
                "Comment", content="I would say BCD instead", comments=comment_ABC
            )
            cnx.commit()

            self.assertEqual(comment_ABC.comments, (abc,))
            self.assertEqual(comment_about_ABC.comments, (comment_ABC,))

            fast_drop_entities(cnx.find("Ami"))

            self.assertEqual(len(cnx.find("Comment")), 0)

    def test_expected_computed_impacted_entities_and_relations(self):
        with self.admin_access.repo_cnx() as cnx:
            abc = cnx.create_entity("Ami", nom="ABC")
            cnx.create_entity("Tag", name="A Tag", tags=abc)
            comment = cnx.create_entity("Comment", content="ABC", comments=abc)
            cnx.commit()

            to_delete = {}
            rels_to_delete = {}
            to_update = {}
            _compute_impacted_entities_and_relations_to_delete(
                cnx, abc.eid, abc.cw_etype, to_delete, rels_to_delete, to_update
            )

            self.assertEqual(to_delete, {"Ami": {abc.eid}, "Comment": {comment.eid}})

            self.assertEqual(to_update, {})  # FIXME: Populate to_update

            self.assertEqual(
                rels_to_delete,
                {
                    ("is", "subject"): {
                        abc.eid,
                        comment.eid,
                    },
                    ("is_instance_of", "subject"): {
                        abc.eid,
                        comment.eid,
                    },
                    ("cw_source", "subject"): {
                        abc.eid,
                        comment.eid,
                    },
                    ("owned_by", "subject"): {
                        abc.eid,
                        comment.eid,
                    },
                    ("created_by", "subject"): {
                        abc.eid,
                        comment.eid,
                    },
                    ("tags", "object"): {
                        abc.eid,
                    },
                },
            )
