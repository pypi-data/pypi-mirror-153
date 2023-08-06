from unittest import TestCase

from openmodule.alert import AlertHandler, AlertHandleType
from openmodule.core import init_openmodule, shutdown_openmodule
from openmodule_test.alert import AlertTestMixin


class AlertTestCase(AlertTestMixin, TestCase):
    topics = ["alert"]

    def setUp(self):
        super().setUp()
        self.core = init_openmodule(context=self.zmq_context(), config=self.zmq_config())
        self.addCleanup(shutdown_openmodule)

    def tearDown(self):
        super().tearDown()

    def test_value_is_required_for_state(self):
        alert_handler = AlertHandler(self.core)
        alert_handler.send("some_alert", AlertHandleType.state, value=10, source="pin1")
        self.assertAlert()

        with self.assertRaises(ValueError) as e:
            alert_handler.send("some_alert", AlertHandleType.state, source="pin1")
        self.assertIn("value must not be none", str(e.exception).lower())
        self.assertNoAlert()

    def test_value_none_is_not_sent(self):
        alert_handler = AlertHandler(self.core)
        alert_handler.send("some_alert", AlertHandleType.state_change, source="pin1")
        alert = self.assertAlert(alert_type="some_alert")
        self.assertNotIn("value", alert)
