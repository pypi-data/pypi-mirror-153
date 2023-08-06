# copyright 2003-2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""unit tests for module cubicweb.server.sqlutils
"""

from logilab.common.testlib import TestCase, unittest_main

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.server.sqlutils import SQLAdapterMixIn

BASE_CONFIG = {
    "db-driver": "Postgres",
    "db-host": "crater",
    "db-name": "cubicweb2_test",
    "db-user": "toto",
    "db-upassword": "toto",
}


class SQLAdapterMixInTC(TestCase):
    def test_init(self):
        o = SQLAdapterMixIn(BASE_CONFIG)
        self.assertEqual(o.dbhelper.dbencoding, "UTF-8")

    def test_init_encoding(self):
        config = BASE_CONFIG.copy()
        config["db-encoding"] = "ISO-8859-1"
        o = SQLAdapterMixIn(config)
        self.assertEqual(o.dbhelper.dbencoding, "ISO-8859-1")


class SQLUtilsTC(CubicWebTC):
    def test_group_concat(self):
        with self.admin_access.repo_cnx() as cnx:
            g = cnx.create_entity("CWGroup", name="héhé")
            cnx.create_entity("CWUser", login="toto", upassword="", in_group=g.eid)
            rset = cnx.execute(
                "Any L,GROUP_CONCAT(G) GROUPBY L WHERE X login L,"
                'X in_group G, G name GN, NOT G name IN ("users", "héhé")'
            )
            self.assertEqual([["admin", "3"], ["anon", "2"]], rset.rows)
            rset = cnx.execute(
                "Any L,GROUP_CONCAT(GN) GROUPBY L WHERE X login L,"
                'X in_group G, G name GN, NOT G name "users"'
            )
            self.assertEqual(
                [["admin", "managers"], ["anon", "guests"], ["toto", "héhé"]], rset.rows
            )


if __name__ == "__main__":
    unittest_main()
