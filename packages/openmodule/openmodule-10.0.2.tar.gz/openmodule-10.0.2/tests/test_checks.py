from datetime import datetime
from unittest import TestCase

from dateutil.tz import gettz, tzutc
from sqlalchemy.exc import StatementError

from tests.database_models_test import DatabaseTimezoneTestModel
from openmodule.config import database_folder
from openmodule.database.database import Database
from openmodule.models.base import OpenModuleModel, timezone_validator
from openmodule_test.database import SQLiteTestMixin


class TimezoneCheckTest(TestCase):
    def test_validator_is_enforced(self):
        with self.assertRaises(AssertionError) as e:
            class MyModel(OpenModuleModel):
                some_field: datetime

        self.assertIn("timezone_validator", str(e.exception))

    def test_datetime_fields_are_converted_to_utc(self):
        class MyModel(OpenModuleModel):
            field: datetime
            _tz_field = timezone_validator("field")

        self.assertEqual("2021-03-25T08:19:42", MyModel(field=1616660382).field.isoformat())
        self.assertEqual("2021-03-25T08:19:42", MyModel(field="2021-03-25 08:19:42").field.isoformat())
        self.assertEqual("2021-03-25T08:19:42", MyModel(field="2021-03-25T08:19:42").field.isoformat())
        self.assertEqual("2021-03-25T08:19:42", MyModel(field="2021-03-25T08:19:42+00:00").field.isoformat())
        self.assertEqual("2021-03-25T08:19:42", MyModel(field="2021-03-25T09:19:42+01:00").field.isoformat())

        self.assertIsNone(MyModel(field="2021-03-25T08:19:42+00:00").field.tzinfo)
        self.assertIsNone(MyModel(field="2021-03-25T09:19:42+01:00").field.tzinfo)

    def test_no_datetime_fields(self):
        with self.assertRaises(AssertionError) as e:
            Database(database_folder(), "test_database", "../tests/invalid_database")
        self.assertIn("Do NOT use DateTime fields, use TZDateTime fields instead", str(e.exception))


class DatabaseDatetimeTest(SQLiteTestMixin):
    alembic_path = "../tests/test_database"

    def test_sqlite_timezone(self):
        with self.assertRaises(StatementError) as e:
            with self.database as db:
                now = datetime.now(tzutc()).astimezone(gettz("Europe/Vienna"))
                model = DatabaseTimezoneTestModel(tz_datetime=now)
                db.add(model)
        self.assertIn("You need to convert a datetime to a naive time", str(e.exception))

        with self.database as db:
            now = datetime.utcnow()
            model = DatabaseTimezoneTestModel(tz_datetime=now)
            db.add(model)
