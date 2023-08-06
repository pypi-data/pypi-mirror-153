# copyright 2020 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

from logilab.common.testlib import unittest_main

from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.ext.markdown import markdown_publish


class MarkdownTC(CubicWebTC):
    def context(self, req):
        return req.execute('CWUser X WHERE X login "admin"').get_entity(0, 0)

    def test_basic(self):
        self.assertEqual(markdown_publish(None, "_test_"), "<p><em>test</em></p>")

    def test_urlify(self):
        self.assertEqual(
            markdown_publish(None, "https://www.logilab.fr/"),
            '<p><a href="https://www.logilab.fr/">https://www.logilab.fr/</a></p>',
        )

    def test_table(self):
        self.maxDiff = None
        self.assertEqual(
            markdown_publish(
                None,
                """\
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
""",
            ),
            """\
<table>
<thead>
<tr>
<th>First Header</th>
<th>Second Header</th>
</tr>
</thead>
<tbody>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
<tr>
<td>Content Cell</td>
<td>Content Cell</td>
</tr>
</tbody>
</table>""",
        )


if __name__ == "__main__":
    unittest_main()
