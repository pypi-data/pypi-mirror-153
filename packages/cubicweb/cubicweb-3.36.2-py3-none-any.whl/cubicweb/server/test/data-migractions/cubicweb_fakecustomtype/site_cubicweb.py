from logilab.database import get_db_helper
from yams import register_base_type

_NUMERIC_PARAMETERS = {"scale": 0, "precision": None}
register_base_type("Numeric", _NUMERIC_PARAMETERS)

# Add the datatype to the helper mapping
pghelper = get_db_helper("postgres")


def pg_numeric_sqltype(rdef):
    """Return a PostgreSQL column type corresponding to rdef"""
    return f"numeric({rdef.precision}, {rdef.scale})"


pghelper.TYPE_MAPPING["Numeric"] = pg_numeric_sqltype
