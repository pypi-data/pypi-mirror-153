import logging
import os
import socket
import warnings
from types import SimpleNamespace
from typing import Optional, Any
from unittest import TestCase

from pydantic import ValidationError

from openmodule import config
from openmodule.config import validate_config_module, LazySettings, override_settings, settings, \
    override_context
from openmodule.models.base import OpenModuleModel
from openmodule_test.files import temp_file
from openmodule_test.zeromq import ZMQTestMixin
from tests.resources.configs import test_config


class EnvTestCase(TestCase):
    initial_env: dict

    def env(self, value, key="t"):
        os.environ[key] = value

    def setUp(self) -> None:
        self.initial_env = os.environ.copy()
        super().setUp()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.initial_env)
        super().tearDown()


class ConfigTest(EnvTestCase):
    def test_int(self):
        self.env("1")
        self.assertEqual(1, config.int("t", 0))

        self.env("a")
        self.assertEqual(0, config.int("t", 0))

        self.env("0x16")
        self.assertEqual(0, config.int("t", 0))

        with self.assertRaises(AssertionError):
            config.int("t", 1.1)

    def test_float(self):
        self.env("1")
        self.assertEqual(1, config.float("t", 0))
        self.env("1.0")
        self.assertEqual(1, config.float("t", 0))
        self.env("1.1")
        self.assertEqual(1.1, config.float("t", 0))

        self.env("a")
        self.assertEqual(0, config.float("t", 0))

        self.env("0x16")
        self.assertEqual(0, config.float("t", 0))

        with self.assertRaises(AssertionError):
            config.float("t", "a")

    def test_str(self):
        self.env("1")
        self.assertEqual("1", config.string("t", "a"))

        self.env(" \"'1' \r\n\t")  # config.string strips unnecessary whitespace and quotes
        self.assertEqual("1", config.string("t", "a"))

        with self.assertRaises(AssertionError):
            config.string("t", 1.0)  # noqa

    def test_bool(self):
        self.env("1")
        self.assertTrue(config.bool("t", False))
        self.env("y")
        self.assertTrue(config.bool("t", False))
        self.env("Y")
        self.assertTrue(config.bool("t", False))
        self.env("t")
        self.assertTrue(config.bool("t", False))
        self.env("true")
        self.assertTrue(config.bool("t", False))
        self.env("yes")
        self.assertTrue(config.bool("t", False))

        # empty string is default value
        self.env("")
        self.assertTrue(config.bool("t", True))
        self.assertFalse(config.bool("t", False))

        with self.assertRaises(AssertionError):
            config.bool("t", "a")  # noqa

    def test_log_level(self):
        self.env("", "LOG_LEVEL")
        self.assertEqual(logging.INFO, config.log_level())  # info is the default value
        self.env("info", "LOG_LEVEL")
        self.assertEqual(logging.INFO, config.log_level())
        self.env("WARN", "LOG_LEVEL")
        self.assertEqual(logging.WARNING, config.log_level())
        self.env("ERROR", "LOG_LEVEL")
        self.assertEqual(logging.ERROR, config.log_level())
        self.env("CRITICAL", "LOG_LEVEL")
        self.assertEqual(logging.CRITICAL, config.log_level())
        self.env("VERBOSE", "LOG_LEVEL")
        self.assertEqual(logging.DEBUG, config.log_level())
        self.env("DEbUG", "LOG_LEVEL")
        self.assertEqual(logging.DEBUG, config.log_level())

    def test_version(self):
        # read version from env first
        self.env("1.0.0", "VERSION")
        self.assertEqual("1.0.0", config.version())

        # if it is not present, read it from VERSION file
        self.env("", "VERSION")
        try:
            with open("VERSION", "w") as f:
                f.write("1.0.0\n")
            self.assertEqual("1.0.0", config.version())
        finally:
            os.unlink("VERSION")

        # if we find nothing, version === "unknown"
        self.assertEqual("unknown", config.version())

    def test_resource(self):
        # no auth credentials set -> use hostname which is nice during development
        self.assertEqual(socket.gethostname(), config.resource())

        self.env("TEST123", "AUTH_RESOURCE")
        self.assertEqual("TEST123", config.resource())


class ConfigYamlTest(EnvTestCase):
    class ExampleModel(OpenModuleModel):
        string: str = "default"

    class NonConstructable(OpenModuleModel):
        string: str

    def test_path_from_env(self):
        with temp_file("string: not-default") as path:
            self.env(path, "CONFIG_YAML")
            instance = config.yaml(self.ExampleModel)
            self.assertEqual('not-default', instance.string)

    def test_default_model(self):
        instance = config.yaml(self.ExampleModel)
        self.assertEqual("default", instance.string)

    def test_invalid_default_model(self):
        # we do not protect against any validation errors, but simply log them
        # in any case this is mostly a developer's fault, and hardly ever a user fault
        with self.assertRaises(ValidationError):
            with self.assertLogs() as cm:
                config.yaml(self.NonConstructable)

        self.assertIn("wrong with the configuration", str(cm.output))

    def test_yaml_ignores_custom_constructors(self):
        yaml = """\
        test: string
        some: !<CustomObject>
            a: b
        """

        class TestModel(OpenModuleModel):
            test: str
            some: Optional[Any]

        with temp_file(yaml) as f:
            model = config.yaml(TestModel, f)

        self.assertIsNone(model.some, msg="Not parsed custom elements must be none")
        self.assertEqual(model.test, "string")

    def test_empty_yml(self):
        yaml = ""

        class TestModel(OpenModuleModel):
            some: Optional[Any]

        with temp_file(yaml) as f:
            model = config.yaml(TestModel, f)

        self.assertIsNone(model.some, msg="Not parsed custom elements must be none")


class LegacyConfigSupportTest(EnvTestCase):
    def test_broker_pub(self):
        # nothing found -> defaults
        self.assertEqual("tcp://127.0.0.1:10200", config.broker_pub())

        # legacy configs
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_PUB_PORT")
        self.assertEqual("tcp://1.2.3.4:1234", config.broker_pub())

        # new configs overrule
        self.env("inproc://test-pub", "BROKER_PUB")
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_PUB_PORT")
        self.assertEqual("inproc://test-pub", config.broker_pub())

    def test_broker_sub(self):
        # nothing found -> defaults
        self.assertEqual("tcp://127.0.0.1:10100", config.broker_sub())

        # legacy configs
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_SUB_PORT")
        self.assertEqual("tcp://1.2.3.4:1234", config.broker_sub())

        # new configs overrule
        self.env("inproc://test-pub", "BROKER_SUB")
        self.env("1.2.3.4", "BROKER_HOST")
        self.env("1234", "BROKER_SUB_PORT")
        self.assertEqual("inproc://test-pub", config.broker_sub())

    def test_missing_keys_in_config_cause_assertion(self):
        fake_config = SimpleNamespace()
        fake_config.NAME = "test"
        with self.assertRaises(AssertionError):
            validate_config_module(fake_config)

    def test_legacy_broker_configs_cause_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            fake_config = SimpleNamespace()
            fake_config.NAME = "test"
            fake_config.RESOURCE = "test"
            fake_config.VERSION = "test"
            fake_config.DEBUG = False
            fake_config.TESTING = True
            fake_config.BROKER_PUB_PORT = "10000"
            validate_config_module(fake_config)

        self.assertEqual(1, len(w))
        self.assertTrue(issubclass(w[0].category, DeprecationWarning))
        self.assertIn("BROKER_PUB", str(w[0].message))


class LazyConfigTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        os.environ.pop("SETTINGS_MODULE", None)
        settings.reset()

    def tearDown(self) -> None:
        super().tearDown()
        settings.reset()
        os.environ.pop("SETTINGS_MODULE", None)

    def test_default_config(self):
        self.assertEqual("test", settings.NAME)

    def test_configured(self):
        settings.configure(test_config)
        self.assertEqual("THIS_IS_MY_NAME", settings.NAME)

    def test_priority(self):
        settings.configure(test_config)
        os.environ["SETTINGS_MODULE"] = "../tests/resources/test_config_1.py"
        self.assertEqual("THIS_IS_MY_NAME", settings.NAME)

    def test_double_configure(self):
        settings.configure(test_config)
        with self.assertRaises(AssertionError) as e:
            settings.configure(test_config)
        self.assertIn("Settings are already configured", str(e.exception))

        second_setting = LazySettings()
        with self.assertRaises(AssertionError) as e:
            second_setting.configure(test_config)
        self.assertIn("Do not use multiple settings", str(e.exception))

    def test_environment(self):
        os.environ["SETTINGS_MODULE"] = "tests.resources.configs.test_config_1"
        self.assertEqual("THIS_IS_MY_NAME_TOO", settings.NAME)
        self.assertEqual("bsdf", settings.TEST)
        del os.environ["SETTINGS_MODULE"]

    @override_settings(NAME="ABC")
    def test_overwrite(self):
        @override_settings(NAME="ASDF")
        def asdf():
            self.assertEqual("ASDF", settings.NAME)
            self.assertTrue(settings._wrapped.is_overridden("NAME"))

        settings.configure(test_config)
        asdf()

        self.assertEqual("ABC", settings.NAME)
        self.assertTrue(settings._wrapped.is_overridden("NAME"))

    def test_override_var_which_does_not_exist(self):
        @override_settings(VAR_DOES_NOT_EXIST=True)
        def testfunction():
            self.assertEqual(True, settings.VAR_DOES_NOT_EXIST)

        self.assertFalse(hasattr(settings, "VAR_DOES_NOT_EXIST"))
        testfunction()
        self.assertFalse(hasattr(settings, "VAR_DOES_NOT_EXIST"))

    def test_context(self):
        settings.configure(test_config)
        self.assertEqual("THIS_IS_MY_NAME", settings.NAME)

        with override_context(NAME="abc"):
            self.assertEqual("abc", settings.NAME)
        self.assertEqual("THIS_IS_MY_NAME", settings.NAME)


@override_settings(BROKER_SUB=f"inproc://test-sub-aaaaaaaaaa")
class ZmqConfigTest(ZMQTestMixin):
    """
    the zmq test mixin dictates the broker pub and sub addresses,
    this test ensures that, in order to avoid accidentially testing on a different protocol,
    because the default settings of a service say so. 
    
    This together with test_test_zeromq.py:ZMQTestMixinInprocTest tests for a bug introduced in
    11a75bf0ae5556d058ae4f1bee4fc1eae5f655e2
    """

    def test_sub(self):
        self.assertNotIn("aaaaaaaaaa", self.zmq_config().BROKER_SUB)
