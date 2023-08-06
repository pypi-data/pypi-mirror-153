import os
import sys
import threading
import types
import warnings
from typing import Optional

from alembic import command, context
from alembic.autogenerate import comparators, renderers
from alembic.config import Config
from alembic.operations import Operations, MigrateOperation
from sqlalchemy import create_engine, event, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from openmodule.checks import check_invalid_database_column_type


def drop_alembic_tmp_tables(op):
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    for table in tables:
        if table.startswith("_alembic_tmp_"):
            op.drop_table(table)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@Operations.register_operation("pre_upgrade")
class PreUpgradeOp(MigrateOperation):
    def __init__(self, schema=None):
        self.schema = schema

    @classmethod
    def pre_upgrade(cls, operations, **kw):
        op = PreUpgradeOp(**kw)
        return operations.invoke(op)

    def reverse(self):
        # only needed to support autogenerate
        return PostDowngradeOp(schema=self.schema)


@Operations.register_operation("post_upgrade")
class PostUpgradeOp(MigrateOperation):
    def __init__(self, schema=None):
        self.schema = schema

    @classmethod
    def post_upgrade(cls, operations, **kw):
        op = PostUpgradeOp(**kw)
        return operations.invoke(op)

    def reverse(self):
        # only needed to support autogenerate
        return PreDowngradeOp(schema=self.schema)


@Operations.register_operation("pre_downgrade")
class PreDowngradeOp(MigrateOperation):
    def __init__(self, schema=None):
        self.schema = schema

    @classmethod
    def pre_downgrade(cls, operations, sequence_name, **kw):
        op = PreDowngradeOp(sequence_name, **kw)
        return operations.invoke(op)

    def reverse(self):
        # only needed to support autogenerate
        return PostUpgradeOp(schema=self.schema)


@Operations.register_operation("post_downgrade")
class PostDowngradeOp(MigrateOperation):
    def __init__(self, schema=None):
        self.schema = schema

    @classmethod
    def post_downgrade(cls, operations, sequence_name, **kw):
        op = PostDowngradeOp(sequence_name, **kw)
        return operations.invoke(op)

    def reverse(self):
        # only needed to support autogenerate
        return PreUpgradeOp(schema=self.schema)


@Operations.implementation_for(PreUpgradeOp)
def pre_upgrade(operations, operation):
    # NOTE: This is currently in sync with pre_downgrade, if you want to have
    # different behavior, you'll need to change th pre_downgrade function below
    drop_alembic_tmp_tables(operations)
    operations.execute("PRAGMA foreign_keys = OFF")


@Operations.implementation_for(PostUpgradeOp)
def post_upgrade(operations, operation):
    pass


@Operations.implementation_for(PreDowngradeOp)
def pre_downgrade(operations, operation):
    pre_upgrade(operations, operation)


@Operations.implementation_for(PostDowngradeOp)
def post_downgrade(operations, operation):
    pass


@renderers.dispatch_for(PreUpgradeOp)
def render_create_sequence(autogen_context, op):
    return "op.pre_upgrade()"


@renderers.dispatch_for(PreDowngradeOp)
def render_drop_sequence(autogen_context, op):
    return "op.pre_downgrade()"


@renderers.dispatch_for(PostUpgradeOp)
def render_create_sequence(autogen_context, op):
    return "op.post_upgrade()"


@renderers.dispatch_for(PostDowngradeOp)
def render_drop_sequence(autogen_context, op):
    return "op.post_downgrade()"


@comparators.dispatch_for("schema")
def add_pre_upgrade_hooks(autogen_context, upgrade_ops, schemas):
    # only add those if any operations exist, otherwise we always have changes
    if len(upgrade_ops.ops):
        upgrade_ops.ops.insert(0, PreUpgradeOp())
        upgrade_ops.ops.append(PostUpgradeOp())


def alembic_config(connection, alembic_path):
    alembic_cfg = Config(os.path.join(alembic_path, "alembic.ini"),
                         attributes={
                             "configure_logging": False,
                             "connection": connection,
                         })
    alembic_cfg.set_main_option("script_location", os.path.join(alembic_path, "alembic"))
    return alembic_cfg


def migrate_database(connection, alembic_path=None):
    if alembic_path is None:
        alembic_path = os.path.join(os.getcwd(), "database")
    assert os.path.exists(os.path.abspath(alembic_path)), f"alembic path {os.path.abspath(alembic_path)} does not exist"
    config = alembic_config(connection, alembic_path)
    command.upgrade(config, "head")
    assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1, "foreign keys are not enabled"


active_databases = {}


def register_bases(bases, show_deprecation_warning=True):
    if show_deprecation_warning:
        warnings.warn(
            '\n\n`register_bases([...])` followed by `from openmodule.database.env import *` is deprecated.\n '
            'Please replace these lines with `run_env_py([bases...])`\n',
            DeprecationWarning
        )

    target_metadata = MetaData()

    if not isinstance(bases, list):
        bases = [bases]

    for base in bases:
        for table in base.metadata.tables.values():
            for x in table.columns:
                check_invalid_database_column_type(x.type)
            table.tometadata(target_metadata)
    context.config.attributes["target_metadata"] = target_metadata


def run_env_py(bases):
    register_bases(bases, show_deprecation_warning=False)
    # noinspection PyUnresolvedReferences
    import openmodule.database.env
    del sys.modules["openmodule.database.env"]  # unload the module, so we can re-run it (mostly testcases)


def database_path(db_folder, db_name):
    return os.path.join(db_folder, db_name) + ".sqlite3"


def get_database(db_folder: str, name: str, alembic_path=None):
    global active_databases
    tmp = database_path(db_folder, name)
    assert active_databases.get(tmp) is None, f"database {tmp} already exists," \
                                              f" check if it was shutdown before a new one was created"
    os.makedirs(db_folder, exist_ok=True)
    path = f"sqlite:///{tmp}"
    engine = create_engine(path, poolclass=StaticPool, connect_args={'check_same_thread': False})
    migrate_database(engine, alembic_path)
    active_databases[tmp] = engine

    return engine


class DatabaseContext:
    def __init__(self, database: 'Database', expire_on_commit=True):
        self.database = database
        self.expire_on_commit = expire_on_commit

    def __enter__(self) -> Session:
        return self.database.__enter__(expire_on_commit=self.expire_on_commit)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.database.__exit__(exc_type, exc_val, exc_tb)


class SessionWrapper(Session):
    _closed = False

    def __getattribute__(self, item):
        attr = super().__getattribute__(item)
        if isinstance(attr, types.MethodType) and self._closed:
            raise AssertionError("Session is already closed")
        return attr

    def close(self):
        super().close()
        self._closed = True


class Database:
    active_session: Optional[Session]

    def __init__(self, database_folder, name="database", alembic_path=None):
        self.db_folder = database_folder
        self.name = name
        self._engine = get_database(database_folder, name, alembic_path)
        self._session = sessionmaker(bind=self._engine, class_=SessionWrapper)
        self.active_session = None
        self.lock = threading.RLock()

    def is_open(self):
        return bool(self._session)

    def shutdown(self):
        assert self.is_open(), "database is already closed, you called shutdown twice somewhere"

        with self.lock:
            self._session = None
            global active_databases
            active_databases.pop(database_path(self.db_folder, self.name), None)

    def __call__(self, expire_on_commit=True) -> DatabaseContext:
        return DatabaseContext(self, expire_on_commit=expire_on_commit)

    def __enter__(self, expire_on_commit=True) -> Session:
        assert self._session, "Session is already closed"
        self.lock.acquire()
        self.active_session = self._session(expire_on_commit=expire_on_commit)
        return self.active_session

    def flush(self, objects=None):
        assert self._session and self.active_session, "Session is already closed"
        self.active_session.flush(objects)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is None:
                self.active_session.commit()
            else:
                self.active_session.rollback()
        finally:
            self.active_session.close()
            self.active_session = None
            self.lock.release()
