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
"""entities tests schema"""

from yams.buildobjs import EntityType, String, RichString, Int

from cubicweb.schema import make_workflowable
from cubicweb.schemas import bootstrap, Bookmark


class Company(EntityType):
    order = Int()
    name = String()
    description = RichString()


class Division(Company):
    __specializes_schema__ = True


class SubDivision(Division):
    __specializes_schema__ = True


make_workflowable(bootstrap.CWGroup)
make_workflowable(Bookmark.Bookmark)
