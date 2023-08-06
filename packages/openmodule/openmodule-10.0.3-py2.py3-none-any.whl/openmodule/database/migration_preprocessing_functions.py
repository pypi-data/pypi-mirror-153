import warnings

from alembic import op

from openmodule.database.database import drop_alembic_tmp_tables

warnings.warn("""\n\n
`prep_upgrade` is deprecated. Replace it with `op.pre_upgrade()`
BEWARE: op.pre_upgrade has NO "p", its pre not prep!
""", DeprecationWarning)


def prep_upgrade():
    drop_alembic_tmp_tables(op)
