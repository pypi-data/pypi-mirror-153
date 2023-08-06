# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""xbel views"""


from cubicweb import _

from cubicweb.predicates import is_instance
from cubicweb.view import EntityView
from cubicweb.web.views.xmlrss import XMLView


class XbelView(XMLView):
    __regid__ = "xbel"
    title = _("xbel export")
    templatable = False
    content_type = "text/xml"  # application/xbel+xml

    def cell_call(self, row, col):
        self.wview("xbelitem", self.cw_rset, row=row, col=col)

    def call(self):
        """display a list of entities by calling their <item_vid> view"""
        self.w('<?xml version="1.0" encoding="%s"?>\n', self._cw.encoding)
        self.w(
            '<!DOCTYPE xbel PUBLIC "+//IDN python.org//DTD XML Bookmark Exchange Language 1.0//EN//XML" "http://www.python.org/topics/xml/dtds/xbel-1.0.dtd">'
        )
        self.w('<xbel version="1.0">')
        self.w("<title>%s</title>", self._cw._("bookmarks"))
        for i in range(self.cw_rset.rowcount):
            self.cell_call(i, 0)
        self.w("</xbel>")


class XbelItemView(EntityView):
    __regid__ = "xbelitem"

    def cell_call(self, row, col):
        entity = self.cw_rset.complete_entity(row, col)
        self.w('<bookmark href="%s">', self.url(entity))
        self.w("  <title>%s</title>", entity.dc_title())
        self.w("</bookmark>")

    def url(self, entity):
        return entity.absolute_url()


class XbelItemBookmarkView(XbelItemView):
    __select__ = is_instance("Bookmark")

    def url(self, entity):
        return entity.actual_url()
