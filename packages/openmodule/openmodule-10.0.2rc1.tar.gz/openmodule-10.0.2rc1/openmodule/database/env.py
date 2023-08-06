from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from openmodule.checks import check_invalid_database_column_type
from openmodule.database.custom_types import CustomType

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.

config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.attributes.get('configure_logging', True):
    fileConfig(config.config_file_name)

target_metadata = config.attributes["target_metadata"]


def render_item(type_, obj, autogen_context):
    """Apply custom rendering for selected items."""

    check_invalid_database_column_type(obj)
    custom_import, name = CustomType.custom_import(obj)
    if type_ == 'type' and custom_import:
        autogen_context.imports.add(f"from {custom_import} import {name}")
        return "%r" % obj
    return False


def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    connectable = config.attributes.get('connection', None)
    if connectable is None:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            render_item=render_item,
            render_as_batch=True
        )

        with context.begin_transaction():
            context.run_migrations()

        connection.execute("PRAGMA foreign_keys=ON")


if context.is_offline_mode():
    assert False, "Not in use"
else:
    run_migrations_online()
