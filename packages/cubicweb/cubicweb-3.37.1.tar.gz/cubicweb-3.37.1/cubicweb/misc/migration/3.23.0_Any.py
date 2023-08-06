from functools import partial

from cubicweb.schema import PURE_VIRTUAL_RTYPES
from cubicweb.server.schema2sql import build_index_name, check_constraint

sql = partial(sql, ask_confirm=False)

source = repo.system_source
helper = source.dbhelper

# drop all relations primary keys
for table, cstr in sql(
    r"""
    SELECT DISTINCT tc.table_name, tc.constraint_name
    FROM information_schema.table_constraints tc,
         information_schema.key_column_usage kc
    WHERE tc.constraint_type = 'PRIMARY KEY'
          AND kc.table_name = tc.table_name
          AND kc.table_name LIKE '%\_relation'
          AND kc.table_schema = tc.table_schema
          AND kc.constraint_name = tc.constraint_name;
"""
):
    sql(f"ALTER TABLE {table} DROP CONSTRAINT {cstr}")

for table, cstr in sql(
    r"""
    SELECT DISTINCT table_name, constraint_name FROM information_schema.constraint_column_usage
    WHERE table_name LIKE 'cw\_%' AND constraint_name LIKE '%\_key'"""
):
    sql(f"ALTER TABLE {table} DROP CONSTRAINT {cstr}")

for rschema in schema.relations():
    if rschema.rule or rschema in PURE_VIRTUAL_RTYPES:
        continue
    if rschema.final or rschema.inlined:
        for rdef in rschema.rdefs.values():
            table = f"cw_{rdef.subject}"
            column = f"cw_{rdef.rtype}"
            if rschema.inlined or rdef.indexed:
                old_name = f"{table.lower()}_{column.lower()}_idx"
                sql("DROP INDEX IF EXISTS %s" % old_name)
                source.create_index(cnx, table, column)
    else:
        table = f"{rschema}_relation"
        sql(
            "ALTER TABLE %s ADD CONSTRAINT %s PRIMARY KEY(eid_from, eid_to)"
            % (table, build_index_name(table, ["eid_from", "eid_to"], "key_"))
        )
        for column in ("from", "to"):
            sql(f"DROP INDEX IF EXISTS {table}_{column}_idx")
            sql(
                "CREATE INDEX %s ON %s(eid_%s);"
                % (build_index_name(table, ["eid_" + column], "idx_"), table, column)
            )

# we changed constraint serialization, which also changes their name

for table, cstr in sql(
    """
    SELECT DISTINCT table_name, constraint_name FROM information_schema.constraint_column_usage
    WHERE constraint_name LIKE 'cstr%'"""
):
    sql("ALTER TABLE %(table)s DROP CONSTRAINT %(cstr)s" % locals())

for cwconstraint in rql("Any C WHERE R constrained_by C").entities():
    cwrdef = cwconstraint.reverse_constrained_by[0]
    rdef = cwrdef.yams_schema()
    cstr = rdef.constraint_by_eid(cwconstraint.eid)
    with cnx.deny_all_hooks_but():
        cwconstraint.cw_set(value=str(cstr.serialize()))
    if cstr.type() not in (
        "BoundaryConstraint",
        "IntervalBoundConstraint",
        "StaticVocabularyConstraint",
    ):
        # These cannot be translate into backend CHECK.
        continue
    cstrname, check = check_constraint(rdef, cstr, helper, prefix="cw_")
    args = {"e": rdef.subject.type, "c": cstrname, "v": check}
    sql("ALTER TABLE cw_%(e)s ADD CONSTRAINT %(c)s CHECK(%(v)s)" % args)

commit()

if "identity_relation" in helper.list_tables(cnx.cnxset.cu):
    sql("DROP TABLE identity_relation")
