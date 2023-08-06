# copyright 2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
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
# with CubicWeb.  If not, see <http://www.gnu.org/licenses/>.

import collections
from logging import getLogger
from contextlib import contextmanager

LOGGER = getLogger("cubicweb")


def _compute_impacted_entities_and_relations_to_delete(
    cnx, eid, etype, to_delete, rels_to_delete, to_update
):
    if eid in to_delete.get(etype, []):
        # avoid loops
        return
    to_delete.setdefault(etype, set()).add(eid)

    eschema = cnx.repo.schema[etype]

    for rschema, related_etypes, role in eschema.relation_definitions():
        if rschema.type == "identity":
            continue
        composites = []
        non_composites = []
        for related_etype in related_etypes:
            rdef = rschema.role_relation_definition(eschema, related_etype, role)
            if role == rdef.composite:
                composites.append(related_etype.type)
            else:
                non_composites.append(related_etype.type)

        if composites and non_composites:
            raise NotImplementedError

        if non_composites and role == "subject" and rschema.inlined:
            continue

        if non_composites and role == "object" and rschema.inlined:
            for related_etype in non_composites:
                to_update.setdefault((related_etype, rschema.type), set()).add(eid)
        elif not rschema.inlined:
            rels_to_delete.setdefault((rschema.type, role), set()).add(eid)

        if composites:
            rql = "Any Y, E WHERE Y is ET, ET name E, X eid %(eid)s"
            if role == "subject":
                rql = ",".join([rql, "X {0} Y".format(rschema.type)])
            else:
                rql = ",".join([rql, "Y {0} X".format(rschema.type)])
            for related_eid, related_etype in cnx.execute(
                rql, {"eid": eid}, build_descr=False
            ):
                _compute_impacted_entities_and_relations_to_delete(
                    cnx,
                    related_eid,
                    related_etype,
                    to_delete,
                    rels_to_delete,
                    to_update,
                )


def _run_fast_drop_entities(cnx, to_update, rels_to_delete, to_delete):

    for (etype, rtype), eids in to_update.items():
        cnx.system_sql(
            "UPDATE cw_{0} SET cw_{1} = NULL WHERE cw_{1} IN ({2})".format(
                etype, rtype, ",".join(str(e) for e in eids)
            )
        )

    for (rtype, role), eids in rels_to_delete.items():
        cnx.system_sql(
            "DELETE FROM {0}_relation WHERE {1} IN ({2})".format(
                rtype,
                "eid_from" if role == "subject" else "eid_to",
                ",".join(str(e) for e in eids),
            )
        )

    deleted = set()
    for etype, eids in to_delete.items():
        deleted |= eids
        cnx.system_sql(
            "DELETE FROM cw_{0} WHERE cw_eid IN ({1})".format(
                etype, ",".join(str(e) for e in eids)
            )
        )
    if deleted:
        eids = ",".join(str(e) for e in deleted)
        cnx.system_sql("DELETE FROM appears WHERE uid IN ({0})".format(eids))
        cnx.system_sql("DELETE FROM entities WHERE eid IN ({0})".format(eids))


@contextmanager
def disable_constraints_check(cnx):
    # disable all triggers and constraint check
    if cnx.repo.system_source.dbdriver == "postgres":
        cnx.system_sql("SET session_replication_role = replica;")
    elif cnx.repo.system_source.dbdriver == "sqlite":
        cnx.system_sql("PRAGMA foreign_keys = ON;")
    else:
        LOGGER.warning(
            "Unknown db-driver : %s."
            "The triggers are **NOT** disable during deletion and "
            "the function might not be as fast as expected",
            cnx.repo.system_source.dbdriver,
        )

    try:
        yield cnx
    except Exception:
        cnx.rollback()
        raise
    finally:  # restore all triggers and constraint check
        if cnx.repo.system_source.dbdriver == "postgres":
            cnx.system_sql("SET session_replication_role = DEFAULT;")
        elif cnx.repo.system_source.dbdriver == "sqlite":
            cnx.system_sql("PRAGMA foreign_keys = OFF;")


def fast_drop_entities(rset, autocommit=True):
    """Delete entities faster using raw SQL and without executing hooks and
    without constraint check
    """
    cnx = rset.req
    to_delete = collections.OrderedDict()
    rels_to_delete = collections.OrderedDict()
    to_update = collections.OrderedDict()
    for entity in rset.entities():
        _compute_impacted_entities_and_relations_to_delete(
            cnx, entity.eid, entity.cw_etype, to_delete, rels_to_delete, to_update
        )

    with disable_constraints_check(cnx) as cnx:
        _run_fast_drop_entities(cnx, to_update, rels_to_delete, to_delete)

    if autocommit:
        cnx.commit()
