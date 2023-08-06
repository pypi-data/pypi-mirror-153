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

"""Contains predicates used in Pyramid views.
"""

from cubicweb._exceptions import UnknownEid
from cubicweb.pyramid.resources import ETypeResource, negociate_mime_type


class MatchIsETypePredicate:
    """A predicate that match if a given etype exist in schema."""

    def __init__(self, matchname, config):
        self.matchname = matchname

    def text(self):
        return "match_is_etype = %s" % self.matchname

    phash = text

    def __call__(self, info, request):
        return (
            info["match"][self.matchname].lower()
            in request.registry["cubicweb.registry"].case_insensitive_etypes
        )


class MatchIsEIDPredicate(object):
    """A predicate that match if a given eid exist in the database."""

    def __init__(self, matchname, config):
        self.matchname = matchname

    def text(self):
        return "match_is_eid = %s" % self.matchname

    phash = text

    def __call__(self, info, request):
        try:
            eid = int(info["match"][self.matchname])
        except ValueError:
            return False

        if request.cw_cnx is None:
            return False

        try:
            request.cw_cnx.entity_from_eid(eid)
        except UnknownEid:
            return False
        return True


class MatchIsETypeAndIdentifierPredicate(object):
    """A predicate which verifiy if the given identifier match one of the rest_attr
    for the given entity type"""

    def __init__(self, matchnames, config):
        self.match_etype, self.match_identifier = matchnames

    def text(self):
        return (
            "match_is_etype_and_identifier ="
            f" {self.match_etype}/{self.match_identifier}"
        )

    phash = text

    def __call__(self, info, request):
        [etype, identifier] = request.path.split("/")[1::]
        try:
            etype_resource = ETypeResource(request, etype)
            resource = etype_resource[identifier]
            entity = resource.rset.one()
            if entity:
                return True
        except Exception:
            pass
        return False


class HasCWPermissionRoutePredicate:
    """A route predicate that matches if the current user has given permission
    on the entity given by its eid, using cubicweb.predicates.has_permission.

    The main purpose of this predicate is to restrain access on specific pages,
    based on the permission of the current user.
    """

    def __init__(self, permission, config):
        self.permission = permission

    def text(self):
        return f"has_cw_permission = {self.permission}"

    phash = text

    def __call__(self, info, request):
        eid = self._get_eid(info, request)
        if not eid:
            return False

        if request.cw_cnx is None:
            return False

        try:
            entity = request.cw_cnx.entity_from_eid(eid)
        except UnknownEid:
            return False

        return entity.cw_has_perm(self.permission)

    def _get_eid(self, info, request):
        try:
            eid = int(info["match"]["eid"])
        except (KeyError, ValueError):
            return None
        return eid


class HasCWPermissionViewPredicate(HasCWPermissionRoutePredicate):
    """This predicate is quite the same as its route pendant, but for
    view.

    The main purpose of this predicate is to have different views for a
    single route, but with different features according to current user
    permissions on the entity.
    """

    def _get_eid(self, info, request):
        try:
            eid = int(request.matchdict["eid"])
        except (KeyError, ValueError):
            return None
        return eid


class IsRequestMimeTypeRDFFormat:
    def __init__(self, val, info):
        self.available_rdf_mimetype = val

    def text(self):
        return f"is_request_mimetype_rdf_format = {self.available_rdf_mimetype}"

    phash = text

    def __call__(self, info, request):
        mime_type = negociate_mime_type(request, self.available_rdf_mimetype)
        return mime_type is not None


def includeme(config):
    config.add_route_predicate("match_is_etype", MatchIsETypePredicate)
    config.add_route_predicate("has_cw_permission", HasCWPermissionRoutePredicate)
    config.add_view_predicate("has_cw_permission", HasCWPermissionViewPredicate)
    config.add_route_predicate("match_is_eid", MatchIsEIDPredicate)
    config.add_route_predicate(
        "match_is_etype_and_identifier", MatchIsETypeAndIdentifierPredicate
    )
    config.add_route_predicate(
        "is_request_mimetype_rdf_format", IsRequestMimeTypeRDFFormat
    )
