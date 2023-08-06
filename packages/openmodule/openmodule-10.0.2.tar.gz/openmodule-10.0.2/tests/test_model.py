import json

import os
import time
from datetime import datetime, timedelta
from typing import Optional
from unittest import TestCase

import freezegun
import orjson
from pydantic import ValidationError

from openmodule.models.backend import Access
from openmodule.models.base import OpenModuleModel, ZMQMessage, Gateway


class TestModel(OpenModuleModel):
    __test__ = False
    value: str


class ModelTestCase(TestCase):
    def test_json_is_forbidden(self):
        instance = TestModel(value="Hello World")
        with self.assertRaises(AssertionError):
            instance.json()

    def test_json_dumps_and_load(self):
        instance = TestModel(value="Hello World")
        instance2 = TestModel.parse_raw(instance.json_bytes())
        self.assertEqual(instance.value, instance2.value)

    def test_unset_default_are_serialized(self):
        class SomeZMQMessage(ZMQMessage):
            type: str = "my-type"

        msg = SomeZMQMessage(name="myname").json_bytes()
        data = orjson.loads(msg)

        self.assertIn("type", data)
        self.assertEqual("my-type", data.get("type"))

    def test_none_values_are_not_exported(self):
        class SomeZMQMessage(ZMQMessage):
            type: str = "test"
            value: Optional[float]

        data = orjson.loads(SomeZMQMessage(name="myname").json_bytes())
        self.assertNotIn("value", data)

        data = orjson.loads(SomeZMQMessage(name="myname", value=1).json_bytes())
        self.assertIn("value", data)
        self.assertEqual(1, data["value"])

        # to my understanding pydantic, openapi and jsonschema all do not agree how nullable but required
        # fields should correctly be handled / annotated. Currently our strategy is to use exclude_none=True
        # so null values are not exported, in an ideal world i would like to have value=None exported, but
        # it is currently not possible
        data = orjson.loads(SomeZMQMessage(name="myname", value=None).json_bytes())
        # self.assertIn("value", data)
        # self.assertEqual(None, data["value"])
        self.assertNotIn("value", data)


class ZMQMessageTestCase(TestCase):
    def test_timestamp_to_datetime(self):
        instance = ZMQMessage(timestamp=1607586354631, name="test", type="test")
        self.assertEqual(instance.timestamp.isoformat(), "2020-12-10T07:45:54.631000")

    def test_timestamp_is_now_if_unset(self):
        instance = ZMQMessage(name="test", type="test")
        self.assertAlmostEqual(instance.timestamp, datetime.utcnow(), delta=timedelta(seconds=1))

    def test_datetime_is_serialized_to_unix_timestamp(self):
        with freezegun.freeze_time("2020-01-01 00:00"):
            instance = ZMQMessage(name="test", type="test")
            json = instance.json_bytes()
            loaded_json = orjson.loads(json)
            self.assertIsInstance(loaded_json["timestamp"], float)
            self.assertEqual(loaded_json["timestamp"], 1577836800)

        instance = ZMQMessage(name="test", type="test")
        instance.timestamp = datetime(2020, 1, 1, 0, 0, 0, 0)
        self.assertEqual(instance.dict()["timestamp"], 1577836800)

    def test_receive_optional_gateway(self):
        class OptionalGateway(ZMQMessage):
            type = "something"
            gateway: Gateway = Gateway()

        message = OptionalGateway(name="test")
        self.assertEqual(message.gateway.direction, "")
        self.assertEqual(message.gateway.gate, "")

        message = OptionalGateway(name="test", gateway={"direction": "in"})
        self.assertEqual(message.gateway.direction, "in")
        self.assertEqual(message.gateway.gate, "")

        with self.assertRaises(ValidationError) as e:
            OptionalGateway(name="test", gateway={"direction": "incorrect"})

        errors = e.exception.errors()
        self.assertEqual(errors[0]["loc"], ("gateway", "direction"))

    def test_unicode_decode_with_old_omutils(self):
        msg = ZMQMessage(name="tä\nst", type="tö\tst")

        data = msg.json_bytes()
        self.assertTrue(isinstance(data, bytes))

        # ensure no unicode symbols are present
        as_unicode = data.decode()
        as_unicode.encode("ascii")  # check its ascii only
        self.assertNotIn("ä", as_unicode)
        self.assertNotIn("ö", as_unicode)
        self.assertIn("\\t", as_unicode)

        # ensure orjson and legacy json return the same result
        res1 = json.loads(as_unicode)
        res2 = json.loads(data)
        res3 = orjson.loads(as_unicode)
        res4 = orjson.loads(data)

        self.assertEqual(res1, res2)
        self.assertEqual(res2, res3)
        self.assertEqual(res3, res4)

        res1.pop("timestamp")
        self.assertDictEqual(res1, {"name": "tä\nst", "type": "tö\tst"})


