from unittest import TestCase

from openmodule.models.base import OpenModuleModel, base64_validator


class Base64TestModel(OpenModuleModel):
    __test__ = False
    some_field: bytes
    _some_field_validator = base64_validator("some_field")


class Base64ValidatorTest(TestCase):
    def test_corret(self):
        model = Base64TestModel(some_field="AAAA")
        self.assertEqual(model.some_field, b"AAAA")

    def test_wrong_padding(self):
        with self.assertRaises(ValueError):
            Base64TestModel(some_field="AAAAA")
