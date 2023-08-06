import os
from glob import glob
from unittest import TestCase

from sqlalchemy import MetaData

from openmodule.config import database_folder, settings
from openmodule.database.database import Database, database_path

_first_start = True


def truncate_all_tables(database: Database, keep=("alembic_version",)):
    assert any(x in database.db_folder for x in ["/test/"]), "deleting all tables is only for testing"
    metadata = MetaData(bind=database._engine)
    metadata.reflect()
    with database._engine.connect() as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            if table.name not in keep:
                con.execute(table.delete())
        trans.commit()


class SQLiteTestMixin(TestCase):
    """
    Mixin for database cleanup in test cases
    * use create_database = True for an automatic generation of a database
    * use create_database = False and set the database directly
    """
    create_database = True
    database = None
    database_folder: str = None  # defaults to settings.DATABASE_FOLDER
    alembic_path = "../src/database"
    database_name = "database"

    @classmethod
    def get_database_folder(cls):
        return cls.database_folder or settings.DATABASE_FOLDER

    @classmethod
    def setUpClass(cls) -> None:
        # we only know which databases are in use on tear down, so truncating only works in teardown
        # but in order to not be annoyed by failed tests which left broken databases, we delete all databases
        # once initially
        global _first_start
        if _first_start:
            for file in glob(os.path.join(cls.get_database_folder(), "*.sqlite3")):
                os.unlink(file)
            _first_start = False
        if cls.create_database:
            cls.database = Database(cls.get_database_folder(), cls.database_name, cls.alembic_path)
        return super().setUpClass()

    def delete_database(self, database: Database):
        assert not database.is_open(), "database must be shutdown before it can be deleted"
        try:
            os.unlink(database_path(database.db_folder, database.name))
        except FileNotFoundError:
            pass

    def tearDown(self):
        super().tearDown()
        if self.create_database:
            truncate_all_tables(self.database)

    @classmethod
    def tearDownClass(cls):
        if cls.create_database:
            cls.database.shutdown()
        super().tearDownClass()
