import time
from unittest import TestCase

from openmodule_test.alert import AlertTestMixin


class AlertTestMixinTest(AlertTestMixin, TestCase):
    topics = ["alert"]

    def setUp(self):
        super().setUp()
        self.config = self.zmq_config()

    def example_alert(self, alert_type="test", status="error"):
        return dict(alert_type=alert_type, handle_type="state_change", status=status,
                    timestamp=time.time(), meta={}, name="om_fancy_test_1")

    def test_any_alert(self):
        self.zmq_client.send(b"alert", type="alert", data=self.example_alert())
        self.assertAlert()

    def test_no_alert(self):
        self.assertNoAlert()

    def test_specific_alert(self):
        alert_1 = self.example_alert()
        alert_2 = self.example_alert(status="ok")
        alert_3 = self.example_alert(alert_type="asdf")

        self.zmq_client.send(b"alert", type="alert", **alert_1)
        self.assertAlert(status="error", alert_type="test")

        self.zmq_client.send(b"alert", type="alert", **alert_2)
        self.assertNoAlert(status="error", alert_type="test")

        self.zmq_client.send(b"alert", type="alert", **alert_3)
        self.assertNoAlert(status="error", alert_type="test")
