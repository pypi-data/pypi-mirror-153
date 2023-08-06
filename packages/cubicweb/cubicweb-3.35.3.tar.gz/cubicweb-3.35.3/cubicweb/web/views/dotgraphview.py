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
"""some basic stuff to build dot generated graph images"""

import codecs
import os
import tempfile

from logilab.common.graph import GraphGenerator, DotBackend

from cubicweb.view import EntityView


class DotGraphView(EntityView):
    __abstract__ = True
    backend_class = DotBackend
    backend_kwargs = {"ratio": "compress", "size": "30,10"}

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        visitor = self.build_visitor(entity)
        prophdlr = self.build_dotpropshandler()
        graphname = "dotgraph%s" % str(entity.eid)
        generator = GraphGenerator(
            self.backend_class(graphname, None, **self.backend_kwargs)
        )
        # image file
        fd, tmpfile = tempfile.mkstemp(".svg")
        os.close(fd)
        generator.generate(visitor, prophdlr, tmpfile)
        with codecs.open(tmpfile, "rb", encoding="utf-8") as svgfile:
            self.w(svgfile.read())

    def build_visitor(self, entity):
        raise NotImplementedError

    def build_dotpropshandler(self):
        return DotPropsHandler(self._cw)


class DotPropsHandler:
    def __init__(self, req):
        self._ = req._

    def node_properties(self, entity):
        """return default DOT drawing options for a state or transition"""
        return {
            "label": entity.dc_long_title(),
            "href": entity.absolute_url(),
            "fontname": "Courier",
            "fontsize": 10,
            "shape": "box",
        }

    def edge_properties(self, transition, fromstate, tostate):
        return {"label": "", "dir": "forward", "color": "black", "style": "filled"}
