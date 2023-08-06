from openmodule_test.zeromq import ZMQTestMixin


class AlertTestMixin(ZMQTestMixin):
    def assertAlert(self, timeout=3, **alert_kwargs):
        self.assertSubscription(b"alert")
        while True:
            message = self.zmq_client.wait_for_message_on_topic(topic=b"alert", timeout=timeout)
            if all(message.get(k) == v for k, v in alert_kwargs.items()):
                return message

    def assertNoAlert(self, timeout=3, **alert_kwargs):
        with self.assertRaises(TimeoutError):
            self.assertAlert(timeout, **alert_kwargs)
