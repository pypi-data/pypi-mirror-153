import os
import shutil
from unittest import TestCase

from openmodule.config import override_context
from openmodule.utils.package_reader import PackageReader, is_bridged_slave
from openmodule_test.fake_package_creator import FakePackageCreator
from openmodule_test.utils import DeveloperError


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package_creator = FakePackageCreator()
        cls.reader = PackageReader()

    def setUp(self) -> None:
        super().setUp()
        self.package_creator.clean_dist_folder()

    def tearDown(self) -> None:
        self.package_creator.clean_dist_folder()
        super().tearDown()


class PackageCreatorReaderTest(BaseTest):
    def test_missing_revision(self):
        self.package_creator.create_service("om-service-eventlog_1", revision=None, env="NAME=om_service_eventlog_1", yml="")
        self.package_creator.create_service("om-service-eventlog_2", env="NAME=om_service_eventlog_2\n", yml="")

        res = self.reader.load_with_service_prefix("")
        self.assertEqual(1, len(res))
        res = res.get("om_service_eventlog_2")
        self.assertIsNotNone(res)
        self.assertEqual("om_service_eventlog_2", res.env["NAME"])

        self.assertEqual(["om_service_eventlog_2"], self.reader.installed_services(""))

    def test_missing_files(self):
        self.package_creator.create_service("om-service-eventlog_1", env=None, yml="")
        with self.assertLogs() as cm:
            res = self.reader.load_with_service_prefix("")
        self.assertIn("env does not exist", str(cm.output))
        self.assertEqual(1, len(res))

        self.package_creator.create_service("om-service-eventlog_2", env="", yml=None)
        with self.assertLogs() as cm1:
            res = self.reader.load_with_service_prefix("")
        # no log triggered for yml
        self.assertEqual(len(cm.output), len(cm1.output))
        self.assertEqual(2, len(res))

    def test_corrupt_files(self):
        self.package_creator.create_service("om-service-eventlog_1", env="", yml="a\nb:1")
        with self.assertLogs() as cm:
            self.reader.load_with_service_prefix("")
        self.assertIn("yml could not be read", str(cm.output))

        self.package_creator.create_service("om-service-eventlog_2", env="=")
        with self.assertLogs() as cm1:
            self.reader.load_with_service_prefix("")
        self.assertIn("Python-dotenv could not parse statement", str(cm1.output))

    def test_prefix(self):
        self.package_creator.create_service("om-service-eventlog_1", env="")
        self.package_creator.create_service("hw-compute-nuc_1", env="")
        self.package_creator.create_service("om-service-stuff_1", env="")

        services = list(self.reader.load_with_service_prefix("om").keys())
        self.assertEqual(2, len(services))
        for x in ["om_service_eventlog_1", "om_service_stuff_1"]:
            self.assertTrue(x in services)
        self.assertEqual(["om_service_eventlog_1"],
                         list(self.reader.load_with_service_prefix("om-service-e").keys()))
        self.assertEqual(["hw_compute_nuc_1"],
                         list(self.reader.load_with_service_prefix("hw").keys()))

    def test_parent(self):
        self.package_creator.create_service("om-fancy-ass_1", env="PARENT=hw_compute_nuc_1")
        self.package_creator.create_service("hw-compute-nuc_1", env="")
        self.package_creator.create_service("om-service-stuff_1", env="")

        res = self.reader.load_with_service_prefix("om", with_parent=True)
        self.assertEqual(2, len(res))
        self.assertIsNone(res["om_service_stuff_1"].parent)
        self.assertIsNotNone(res["om_fancy_ass_1"].parent)

    def test_hw_type(self):
        self.package_creator.create_service("hw-compute-nuc_1", env='HARDWARE_TYPE=["compute-nuc", "nice-stuff", "stuff-bad"]')
        self.assertEqual(1, len(self.reader.load_with_hardware_type_prefix("compute")))
        self.assertEqual(1, len(self.reader.load_with_hardware_type_prefix("nice")))
        self.assertEqual(1, len(self.reader.load_with_hardware_type_prefix("nice-st")))
        self.assertEqual(0, len(self.reader.load_with_hardware_type_prefix("bad")))

    def test_parent_type(self):
        self.package_creator.create_service("om-fancy-ass_1", env="PARENT=hw_compute_nuc_1\nPARENT_TYPE=[\"compute-nuc\", \"bad-nuc\"]")
        self.assertEqual(1, len(self.reader.load_with_parent_type_prefix("compute")))
        self.assertEqual(1, len(self.reader.load_with_parent_type_prefix("bad")))
        self.assertEqual(0, len(self.reader.load_with_parent_type_prefix("nuc")))

    def test_create_om(self):
        with self.assertRaises(DeveloperError):
            self.package_creator.create_om_service("hw", dict())

        self.package_creator.create_om_service("om-service-test-1", dict(name="asdf"))
        self.package_creator.create_om_service("om_service_test-2", dict(bla=1234), yml="this: good")

        data = self.reader.load_with_service_prefix("om-service-test_1")["om_service_test_1"]
        self.assertEqual("om_service_test_1", data.env["NAME"])
        self.assertEqual({}, data.yml)

        data = self.reader.load_with_service_prefix("om-service-test_2")["om_service_test_2"]
        self.assertEqual("om_service_test_2", data.env["NAME"])
        self.assertEqual("1234", data.env["BLA"])
        self.assertEqual("good", data.yml["this"])

    def test_create_hw(self):
        with self.assertRaises(DeveloperError):
            self.package_creator.create_hw_service("om", dict(), "1.2.3.4", dict())

        self.package_creator.create_hw_service("hw-service-test-1", dict(name="asdf"), "1.2.3.4")
        self.package_creator.create_hw_service("hw_service_test-2", dict(bla=1234), "1.2.3.4", dict(ip="2.3.4.5"))

        data = self.reader.load_with_service_prefix()
        entry = data["hw_service_test_1"]
        self.assertEqual("hw_service_test_1", entry.env["NAME"])
        self.assertEqual("1.2.3.4", entry.yml["ip"])
        self.assertEqual("1.2.3.4/24", entry.yml["network"]["addresses"][0])
        self.assertEqual("1.2.3.1", entry.yml["network"]["gateway"])

        entry = data["hw_service_test_2"]
        self.assertEqual("hw_service_test_2", entry.env["NAME"])
        self.assertEqual("1234", entry.env["BLA"])
        self.assertEqual("2.3.4.5", entry.yml["ip"])
        self.assertEqual("1.2.3.4/24", entry.yml["network"]["addresses"][0])
        self.assertEqual("1.2.3.1", entry.yml["network"]["gateway"])


class BridgedSlaveTest(BaseTest):
    def test_overwrite(self):
        with override_context(BRIDGED_SLAVE=False):
            self.assertFalse(is_bridged_slave())
        with override_context(BRIDGED_SLAVE=True):
            self.assertTrue(is_bridged_slave())

    def test_master_from_directory(self):
        self.package_creator.create_service("om_service_bridge_1", env="MASTER=")
        self.assertFalse(is_bridged_slave())

    def test_slave_from_directory(self):
        self.package_creator.create_service("om_service_bridge_1", env="MASTER=10.1.1.1")
        self.assertTrue(is_bridged_slave())

    def test_config_fail(self):
        # multiple bridges
        self.package_creator.create_service("om_service_bridge_1", env="MASTER=", yml="")
        self.package_creator.create_service("om_service_bridge_2", env="MASTER=1234", yml="")
        self.assertIsNone(is_bridged_slave())

        # wrong directory
        self.assertIsNone(is_bridged_slave())
