from datetime import datetime
from unittest import TestCase

import freezegun
from dateutil.parser import parse

from openmodule.config import settings
from openmodule.models.backend import Access, AccessCategory


class AccessModelTestCase(TestCase):
    def assertTzNaive(self, d):
        self.assertTrue(d.tzinfo is None)

    def tearDown(self) -> None:
        super().tearDown()
        settings.reset()

    def is_valid_at(self, access, dt, timezone="Europe/Vienna"):
        dt = parse(dt)
        return access.is_valid_at(dt, timezone)

    def test_deserialized_datetimes_are_timezone_native(self):
        # unix timestamps
        json_bytes = b'{"start": 1600000, "user": "some-user", "category": "booked-digimon"}'
        access = Access.parse_raw(json_bytes)
        self.assertTzNaive(access.start)

        # tz aware iso strings
        json_bytes = b'{"start": "2017-02-15T20:26:08.937881-06:00", "user": "some-user", "category": "booked-digimon"}'
        access = Access.parse_raw(json_bytes)
        self.assertTzNaive(access.start)

        # naive iso strings
        json_bytes = b'{"start": "2017-02-15T20:26:08.937881", "user": "some-user", "category": "booked-digimon"}'
        access = Access.parse_raw(json_bytes)
        self.assertTzNaive(access.start)

    def test_is_valid_non_recurrent_start_end(self):
        access = Access(start="2000-01-02T00:00", end="2000-01-03T00:00", user="test", category="booked-digimon")

        # naive test
        self.assertFalse(self.is_valid_at(access, "2000-01-01T23:59:59"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T00:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-03T00:00"))
        self.assertFalse(self.is_valid_at(access, "2000-01-03T00:00:01"))

        # timezone aware test
        self.assertFalse(self.is_valid_at(access, "2000-01-02T01:59+02:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T02:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-03T02:00+02:00"))
        self.assertFalse(self.is_valid_at(access, "2000-01-03T02:01+02:00"))

    def test_is_valid_timezone_issue(self):
        access = Access(user="b1", start="2020-01-01 00:00", end="2020-01-01 04:00",
                        category=AccessCategory.booked_digimon)

        with freezegun.freeze_time("2020-01-01 03:30"):
            access = access.parse_raw(access.json_bytes())
            self.assertTrue(access.is_valid_at(datetime.utcnow(), None))

    def test_is_valid_non_recurrent_start_no_end(self):
        access = Access(start="2000-01-02T00:00", user="test", category="booked-digimon")

        # naive test
        self.assertFalse(self.is_valid_at(access, "2000-01-01T23:59:59"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T00:00"))
        self.assertTrue(self.is_valid_at(access, "3000-02-02T00:00"))

        # timezone aware test
        self.assertFalse(self.is_valid_at(access, "2000-01-01T01:59:59+02:00"))
        self.assertTrue(self.is_valid_at(access, "2000-01-02T02:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "3000-02-02T02:00+02:00"))

    def test_is_valid_recurrent_start_end_recurrent(self):
        access = Access(start="2000-01-01T00:00", end="2000-01-07T23:59", user="test", category="booked-visitor",
                        recurrence="DTSTART:19990108T110000\nRRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
                        duration=3600 * 9)  # from 12:00 to 21:00

        # before the start date
        self.assertFalse(self.is_valid_at(access, "1999-12-30T13:00"))  # SA
        self.assertFalse(self.is_valid_at(access, "1999-12-31T13:00"))  # FR

        # between start and end
        self.assertFalse(self.is_valid_at(access, "2000-01-01T13:00"))  # SA
        self.assertFalse(self.is_valid_at(access, "2000-01-02T13:00"))  # SO
        self.assertTrue(self.is_valid_at(access, "2000-01-03T13:00"))  # MO
        self.assertTrue(self.is_valid_at(access, "2000-01-04T13:00"))  # TU
        self.assertTrue(self.is_valid_at(access, "2000-01-05T13:00"))  # WE
        self.assertTrue(self.is_valid_at(access, "2000-01-06T13:00"))  # TH
        self.assertTrue(self.is_valid_at(access, "2000-01-07T13:00"))  # FR

        # Test the exact limits on friday
        self.assertFalse(self.is_valid_at(access, "2000-01-07T11:59:59+01:00"))  # FR
        self.assertTrue(self.is_valid_at(access, "2000-01-07T12:00+01:00"))  # FR
        self.assertTrue(self.is_valid_at(access, "2000-01-07T20:59:59+01:00"))  # FR
        self.assertFalse(self.is_valid_at(access, "2000-01-07T21:00:00+01:00"))  # FR

        # after the end date
        self.assertFalse(self.is_valid_at(access, "2000-01-08T13:00"))  # SA
        self.assertFalse(self.is_valid_at(access, "2000-01-09T13:00"))  # FR

    def test_is_valid_recurrent_start_no_end_recurrent(self):
        access = Access(start="2000-01-01T00:00", end=None, user="test", category="booked-visitor",
                        recurrence="DTSTART:19990108T110000\nRRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
                        duration=3600 * 9)  # from 12:00 to 21:00

        # before the start date
        self.assertFalse(self.is_valid_at(access, "1999-12-30T13:00"))  # SA
        self.assertFalse(self.is_valid_at(access, "1999-12-31T13:00"))  # FR

        # between start and end
        self.assertFalse(self.is_valid_at(access, "2000-01-01T13:00"))  # SA
        self.assertFalse(self.is_valid_at(access, "2000-01-02T13:00"))  # SO
        self.assertTrue(self.is_valid_at(access, "2000-01-03T13:00"))  # MO
        self.assertTrue(self.is_valid_at(access, "2000-01-04T13:00"))  # TU
        self.assertTrue(self.is_valid_at(access, "2000-01-05T13:00"))  # WE
        self.assertTrue(self.is_valid_at(access, "2000-01-06T13:00"))  # TH
        self.assertTrue(self.is_valid_at(access, "2000-01-07T13:00"))  # FR

        # years later
        self.assertFalse(self.is_valid_at(access, "2022-01-01T13:00"))  # SA
        self.assertFalse(self.is_valid_at(access, "2022-01-02T13:00"))  # SO
        self.assertTrue(self.is_valid_at(access, "2022-01-03T13:00"))  # MO
        self.assertTrue(self.is_valid_at(access, "2022-01-04T13:00"))  # TU
        self.assertTrue(self.is_valid_at(access, "2022-01-05T13:00"))  # WE
        self.assertTrue(self.is_valid_at(access, "2022-01-06T13:00"))  # TH
        self.assertTrue(self.is_valid_at(access, "2022-01-07T13:00"))  # FR

    def test_recurrence_during_dst_change(self):
        access = Access(start="2000-01-01T00:00", end=None, user="test", category="booked-visitor",
                        recurrence="DTSTART:19990108T000000\nRRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU",
                        duration=3600 * 3 + 1)  # from 01:00 to 04:00

        # normal day
        self.assertFalse(self.is_valid_at(access, "2021-03-27T00:00+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-27T01:00+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-27T01:59+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-27T03:00+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-27T04:00+01:00"))
        self.assertFalse(self.is_valid_at(access, "2021-03-27T05:00+01:00"))  # this is the normal case
        self.assertFalse(self.is_valid_at(access, "2021-03-27T06:00+01:00"))

        # from +01:00 to +02:00
        self.assertFalse(self.is_valid_at(access, "2021-03-28T00:00+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-28T01:00+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-28T01:59+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-28T03:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "2021-03-28T04:00+02:00"))
        # usually it goes only until 4 o'clock, but during dst change we add the hour to avoid conflicts
        self.assertTrue(self.is_valid_at(access, "2021-03-28T05:00+02:00"))  # special case
        self.assertFalse(self.is_valid_at(access, "2021-03-28T06:00+02:00"))

        # from +02:00 to +01:00
        self.assertFalse(self.is_valid_at(access, "2021-10-31T00:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "2021-10-31T01:00+02:00"))
        self.assertTrue(self.is_valid_at(access, "2021-10-31T01:59+02:00"))
        self.assertTrue(self.is_valid_at(access, "2021-10-31T03:00+01:00"))
        self.assertTrue(self.is_valid_at(access, "2021-10-31T04:00+01:00"))
        # usually it goes only until 4 o'clock, but during dst change we add the hour to avoid conflicts
        self.assertTrue(self.is_valid_at(access, "2021-10-31T05:00+01:00"))  # special case
        self.assertFalse(self.is_valid_at(access, "2021-10-31T06:00+01:00"))
