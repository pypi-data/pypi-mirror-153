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
"""A rql query completer. Given the start of a RQL query, provides possible
completions.
"""
from logging import getLogger

from rql import parse
from rql.utils import rqlvar_maker
from yams.interfaces import IVocabularyConstraint


class RQLSuggestionsBuilder:
    """main entry point is `build_suggestions()` which takes
    an incomplete RQL query and returns a list of suggestions to complete
    the query.

    .. automethod:: cubicweb.rqlsuggestions.RQLSuggestionsBuilder.build_suggestions
    """

    # maximum number of results to fetch when suggesting attribute values
    attr_value_limit = 20

    def __init__(self, req):
        self.req = req
        self.logger = getLogger("cubicweb.rqlsuggestions")

    def build_suggestions(self, user_rql):
        """return a list of suggestions to complete `user_rql`

        :param user_rql: an incomplete RQL query
        """
        req = self.req
        try:
            if (
                "WHERE" not in user_rql
            ):  # don't try to complete if there's no restriction
                return []
            variables, restrictions = [
                part.strip() for part in user_rql.split("WHERE", 1)
            ]
            if "," in restrictions:
                restrictions, incomplete_part = restrictions.rsplit(",", 1)
                user_rql = f"{variables} WHERE {restrictions}"
            else:
                restrictions, incomplete_part = "", restrictions
                user_rql = variables
            select = parse(user_rql, print_errors=False).children[0]
            req.vreg.rqlhelper.annotate(select)
            req.vreg.compute_var_types(req, select, {})
            if restrictions:
                return [
                    f"{user_rql}, {suggestion}"
                    for suggestion in self._rql_build_suggestions(
                        select, incomplete_part
                    )
                ]
            else:
                return [
                    f"{user_rql} WHERE {suggestion}"
                    for suggestion in self._rql_build_suggestions(
                        select, incomplete_part
                    )
                ]
        except Exception as exc:  # we never want to crash
            print(exc)
            self.logger.debug("failed to build suggestions: %s", exc)
            return []

    # actual completion entry points #########################################
    def _rql_build_suggestions(self, select, incomplete_part):
        """
        :param select: the annotated select node (rql syntax tree)
        :param incomplete_part: the part of the rql query that needs
                                to be completed, (e.g. ``X is Pr``, ``X re``)
        """
        chunks = incomplete_part.split(None, 2)
        if not chunks:  # nothing to complete
            return []
        if len(chunks) == 1:  # `incomplete` looks like "MYVAR"
            return self._complete_rqlvar(select, *chunks)
        elif len(chunks) == 2:  # `incomplete` looks like "MYVAR some_rel"
            return self._complete_rqlvar_and_rtype(select, *chunks)
        elif len(chunks) == 3:  # `incomplete` looks like "MYVAR some_rel something"
            return self._complete_relation_object(select, *chunks)
        else:  # would be anything else, hard to decide what to do here
            return []

    def _complete_rqlvar(self, select, rql_var):
        """return suggestions for "variable only" incomplete_part

        as in :

        - Any X WHERE X
        - Any X WHERE X is Project, Y
        - etc.
        """
        return [
            f"{rql_var} {rtype} {dest_var}"
            for rtype, dest_var in self._possible_relations(select, rql_var)
        ]

    def _complete_rqlvar_and_rtype(self, select, rql_var, user_rtype):
        """return suggestions for "variable + rtype" incomplete_part

        as in :

        - Any X WHERE X is
        - Any X WHERE X is Person, X firstn
        - etc.
        """
        # special case `user_type` == 'is', return every possible type.
        if user_rtype == "is":
            return self._complete_is_relation(select, rql_var)
        else:
            return [
                f"{rql_var} {rtype} {dest_var}"
                for rtype, dest_var in self._possible_relations(select, rql_var)
                if rtype.startswith(user_rtype)
            ]

    def _complete_relation_object(self, select, rql_var, user_rtype, user_value):
        """return suggestions for "variable + rtype + some_incomplete_value"

        as in :

        - Any X WHERE X is Per
        - Any X WHERE X is Person, X firstname "
        - Any X WHERE X is Person, X firstname "Pa
        - etc.
        """
        # special case `user_type` == 'is', return every possible type.
        if user_rtype == "is":
            return self._complete_is_relation(select, rql_var, user_value)
        elif user_value:
            if user_value[0] in ('"', "'"):
                # if finished string, don't suggest anything
                if len(user_value) > 1 and user_value[-1] == user_value[0]:
                    return []
                user_value = user_value[1:]
                return [
                    f'{rql_var} {user_rtype} "{value}"'
                    for value in self._vocabulary(
                        select, rql_var, user_rtype, user_value
                    )
                ]
        return []

    def _complete_is_relation(self, select, rql_var, prefix=""):
        """return every possible types for rql_var

        :param prefix: if specified, will only return entity types starting
                       with the specified value.
        """
        return [
            f"{rql_var} is {etype}"
            for etype in self._possible_etypes(select, rql_var, prefix)
        ]

    def _etypes_suggestion_set(self):
        """return the list of possible entity types to suggest

        The default is to return any non-final entity type available
        in the schema.

        Can be overridden for instance if an application decides
        to restrict this list to a meaningful set of business etypes.
        """
        schema = self.req.vreg.schema
        return {eschema.type for eschema in schema.entities() if not eschema.final}

    def _possible_etypes(self, select, rql_var, prefix=""):
        """return all possible etypes for `rql_var`

        The returned list will always be a subset of meth:`etypes_suggestion_set`

        :param select: the annotated select node (rql syntax tree)
        :param rql_var: the variable name for which we want to know possible types
        :param prefix: if specified, will only return etypes starting with it
        """
        available_etypes = self._etypes_suggestion_set()
        possible_etypes = set()
        for sol in select.solutions:
            if rql_var in sol and sol[rql_var] in available_etypes:
                possible_etypes.add(sol[rql_var])
        if not possible_etypes:
            # `Any X WHERE X is Person, Y is`
            # -> won't have a solution, need to give all etypes
            possible_etypes = available_etypes
        return sorted(etype for etype in possible_etypes if etype.startswith(prefix))

    def _possible_relations(self, select, rql_var, include_meta=False):
        """return a list of couple (rtype, dest_var) for each possible
        relations with `rql_var` as subject.

        ``dest_var`` will be picked among availabel variables if types match,
        otherwise a new one will be created.
        """
        schema = self.req.vreg.schema
        relations = set()
        untyped_dest_var = next(rqlvar_maker(defined=select.defined_vars))
        # for each solution
        # 1. find each possible relation
        # 2. for each relation:
        #    2.1. if the relation is meta, skip it
        #    2.2. for each possible destination type, pick up possible
        #         variables for this type or use a new one
        for sol in select.solutions:
            etype = sol[rql_var]
            sol_by_types = {}
            for varname, var_etype in sol.items():
                # don't push subject var to avoid "X relation X" suggestion
                if varname != rql_var:
                    sol_by_types.setdefault(var_etype, []).append(varname)
            for rschema in list(schema[etype].subject_relations.values()):
                if include_meta or not rschema.meta:
                    for dest in rschema.objects(etype):
                        for varname in sol_by_types.get(dest.type, (untyped_dest_var,)):
                            suggestion = (rschema.type, varname)
                            if suggestion not in relations:
                                relations.add(suggestion)
        return sorted(relations)

    def _vocabulary(self, select, rql_var, user_rtype, rtype_incomplete_value):
        """return acceptable vocabulary for `rql_var` + `user_rtype` in `select`

        Vocabulary is either found from schema (Yams) definition or
        directly from database.
        """
        schema = self.req.vreg.schema
        vocab = []
        for sol in select.solutions:
            # for each solution :
            # - If a vocabulary constraint exists on `rql_var+user_rtype`, use it
            #   to define possible values
            # - Otherwise, query the database to fetch available values from
            #   database (limiting results to `self.attr_value_limit`)
            try:
                eschema = schema.entity_schema_for(sol[rql_var])
                rdef = eschema.relation_definition(user_rtype)
            except KeyError:  # unknown relation
                continue
            cstr = rdef.constraint_by_interface(IVocabularyConstraint)
            if cstr is not None:
                # a vocabulary is found, use it
                vocab += [
                    value
                    for value in cstr.vocabulary()
                    if value.startswith(rtype_incomplete_value)
                ]
            elif rdef.final:
                # no vocab, query database to find possible value
                vocab_rql = "DISTINCT Any V LIMIT {} WHERE X is {}, X {} V".format(
                    self.attr_value_limit,
                    eschema.type,
                    user_rtype,
                )
                vocab_kwargs = {}
                if rtype_incomplete_value:
                    vocab_rql += ", X %s LIKE %%(value)s" % user_rtype
                    vocab_kwargs["value"] = "%s%%" % rtype_incomplete_value
                vocab += [value for value, in self.req.execute(vocab_rql, vocab_kwargs)]
        return sorted(set(vocab))
