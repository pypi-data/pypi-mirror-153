# copyright 2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2014-2016 UNLISH S.A.S. (Montpellier, FRANCE), all rights reserved.
#
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

"""Pyramid resources definitions for CubicWeb."""

from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPNotFound
from rql import TypeResolverException

from cubicweb import rdf


def negociate_mime_type(request, possible_mimetypes):
    accepted_headers_by_weight = sorted(
        request.accept.parsed or [], key=lambda h: h[1], reverse=True
    )
    mime_type_negociated = None
    for parsed_header in accepted_headers_by_weight:
        accepted_mime_type = parsed_header[0]
        if accepted_mime_type in possible_mimetypes:
            mime_type_negociated = accepted_mime_type
            break
    return mime_type_negociated


def rdf_context_from_eid(request):
    mime_type = negociate_mime_type(request, rdf.RDF_MIMETYPE_TO_FORMAT)
    if mime_type is None:
        raise HTTPNotFound()
    entity = EntityResource.from_eid()(request).rset.one()
    return RDFResource(entity, mime_type)


def rdf_context_from_identifier(request):
    mime_type = negociate_mime_type(request, rdf.RDF_MIMETYPE_TO_FORMAT)
    if mime_type is None:
        raise HTTPNotFound()
    entity = ETypeResource.from_match("etype")(request)[
        request.matchdict["identifier"]
    ].rset.one()
    return RDFResource(entity, mime_type)


class RDFResource:
    def __init__(self, entity, mime_type):
        self.entity = entity
        self.mime_type = mime_type


class EntityResource:

    """A resource class for an entity. It provides method to retrieve an entity
    by eid.
    """

    @classmethod
    def from_eid(cls):
        def factory(request):
            return cls(request, None, None, request.matchdict["eid"])

        return factory

    def __init__(self, request, cls, attrname, value):
        self.request = request
        self.cls = cls
        self.attrname = attrname
        self.value = value

    @reify
    def rset(self):
        req = self.request.cw_request
        if self.cls is None:
            return req.execute("Any X WHERE X eid %(x)s", {"x": int(self.value)})
        st = self.cls.fetch_rqlst(self.request.cw_cnx.user, ordermethod=None)
        st.add_constant_restriction(
            st.get_variable("X"), self.attrname, "x", "Substitute"
        )
        if self.attrname == "eid":
            try:
                rset = req.execute(st.as_string(), {"x": int(self.value)})
            except (ValueError, TypeResolverException):
                # conflicting eid/type
                raise HTTPNotFound()
        else:
            rset = req.execute(st.as_string(), {"x": self.value})
        return rset


class ETypeResource:
    """A resource for etype."""

    @classmethod
    def from_match(cls, matchname):
        def factory(request):
            return cls(request, request.matchdict[matchname])

        return factory

    def __init__(self, request, etype):
        vreg = request.registry["cubicweb.registry"]

        self.request = request
        self.etype = vreg.case_insensitive_etypes[etype.lower()]
        self.cls = vreg["etypes"].etype_class(self.etype)

    def __getitem__(self, value):
        (rest_attr, needcheck) = self.cls.cw_rest_attr_info()
        resource = EntityResource(self.request, self.cls, rest_attr, value)
        rset = resource.rset
        if rset.rowcount and (not needcheck or rset.rowcount == 1):
            return resource
        raise KeyError(value)

    @reify
    def rset(self):
        rql = self.cls.fetch_rql(self.request.cw_cnx.user)
        rset = self.request.cw_request.execute(rql)
        return rset
