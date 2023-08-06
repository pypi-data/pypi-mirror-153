import time
from threading import Thread
from unittest import TestCase

from openmodule.models.base import ZMQMessage, Gateway, Direction
from openmodule_test.gate import TestGate
from openmodule_test.utils import DeveloperError
from openmodule_test.zeromq import ZMQTestMixin


class DummyAccessMessage(ZMQMessage):
    name = "test"
    type = "access"
    gateway: Gateway


class TestGateTestCase(ZMQTestMixin, TestCase):
    topics = [b"access_accept", b"access_reject"]

    def setUp(self):
        super().setUp()

        self.gate1 = TestGate("gate1", Direction.IN, self.zmq_client.zmq_dispatcher)
        self.gate2 = TestGate("gate2", Direction.OUT, self.zmq_client.zmq_dispatcher)

    def send_access_accept(self, gate: str, direction: str):
        self.zmq_client.send("access_accept", DummyAccessMessage(gateway=Gateway(gate=gate, direction=direction)))

    def send_access_reject(self, gate: str, direction: str):
        self.zmq_client.send("access_reject", DummyAccessMessage(gateway=Gateway(gate=gate, direction=direction)))

    def test_wait_for_open(self):
        self.send_access_accept("gate1", "in")
        with self.assertRaises(TimeoutError):
            self.gate2.wait_for_open()
        self.gate1.wait_for_open()

    def test_wait_for_reject(self):
        self.send_access_reject("gate1", "in")
        with self.assertRaises(TimeoutError):
            self.gate2.wait_for_reject()
        self.gate1.wait_for_reject()

    def test_first_reject_then_open(self):
        self.send_access_reject("gate1", "in")

        def _send_accept_in_1s():
            time.sleep(1)
            self.send_access_accept("gate1", "in")

        thread = Thread(target=_send_accept_in_1s())
        thread.start()

        with self.assertRaises(AssertionError):
            # in this case an assertion instead of a timeout is raised, because the gate way opened, while
            # we expected a reject
            self.gate1.wait_for_reject(timeout=5)
        with self.assertRaises(TimeoutError):
            self.gate2.wait_for_reject()

        # gate 1 is rejected, but it opened, so assert opened is still true
        with self.assertRaises(AssertionError):
            self.gate1.assert_rejected()
        self.gate1.assert_opened()

        # gate 2 received no messages, so everything asserts
        with self.assertRaises(AssertionError):
            self.gate2.assert_rejected()
        with self.assertRaises(AssertionError):
            self.gate2.assert_opened()

        thread.join()

    def test_reset_counts_required(self):
        self.send_access_accept("gate1", "in")
        self.gate1.wait_for_open()

        with self.assertRaises(DeveloperError) as e:
            self.gate1.wait_for_open()

        self.assertIn("reset_counts()", str(e.exception))
