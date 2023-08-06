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
"""Package containing various utilities to import data into cubicweb."""

from logilab.common.deprecation import callable_moved


SQLGenSourceWrapper = callable_moved(
    "cubicweb.dataimport.pgstore", "SQLGenSourceWrapper"
)
count_lines = callable_moved("cubicweb.dataimport.csv", "count_lines")
ucsvreader = callable_moved("cubicweb.dataimport.csv", "ucsvreader")
ucsvreader_pb = callable_moved("cubicweb.dataimport.csv", "ucsvreader_pb")
NullStore = callable_moved("cubicweb.dataimport.stores", "NullStore")
RQLObjectStore = callable_moved("cubicweb.dataimport.stores", "RQLObjectStore")
NoHookRQLObjectStore = callable_moved(
    "cubicweb.dataimport.stores", "NoHookRQLObjectStore"
)
MetadataGenerator = callable_moved("cubicweb.dataimport.stores", "MetadataGenerator")
MetaGenerator = callable_moved("cubicweb.dataimport.stores", "MetaGenerator")


def callfunc_every(func, number, iterable):
    """yield items of `iterable` one by one and call function `func`
    every `number` iterations. Always call function `func` at the end.
    """
    for idx, item in enumerate(iterable):
        yield item
        if not idx % number:
            func()
    func()
