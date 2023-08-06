import random
import string
import time
from contextlib import suppress
from unittest import TestCase

import orjson
import zmq

from openmodule.config import override_context
from openmodule.messaging import get_pub_socket, get_sub_socket, receive_message_from_socket, wait_for_connection
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.zeromq import TestBroker, fake_config, TestClient


class MessagingTest(TestCase):
    pub_socket: zmq.Socket
    sub_socket: zmq.Socket
    broker: TestBroker

    def setUp(self) -> None:
        super().setUp()

        # we cannot use ZMQTestMixin here, because the zmq client crashes (on purpose) when receiving invalid messages

        random_suffix = "".join(random.choices(string.ascii_letters, k=10))
        sub = f"inproc://test-sub-{random_suffix}"
        pub = f"inproc://test-pub-{random_suffix}"
        self.broker = TestBroker(sub, pub)
        self.broker.start()

        self.pub_socket = get_pub_socket(self.broker.context, fake_config(self.broker))
        self.sub_socket = get_sub_socket(self.broker.context, fake_config(self.broker))
        self.sub_socket.subscribe(b"topic")

        connected = False
        for x in range(30):
            self.pub_socket.send_multipart((b"topic", b"data"))
            time.sleep(0.1)
            try:
                self.sub_socket.recv_multipart(flags=zmq.NOBLOCK)
                connected = True
                break
            except zmq.Again:
                pass

        # sometimes a stray message is received afterwards, we have to deal with them here in quite a "dumb" way
        # the test client handles this much better because it can differentiate between connect pings and actual
        # messages
        with suppress(zmq.Again):  # pragma: no cover
            self.sub_socket.recv_multipart(flags=zmq.NOBLOCK)
            time.sleep(0.1)
            self.sub_socket.recv_multipart(flags=zmq.NOBLOCK)

        assert connected, "sockets did not connect"

    def tearDown(self) -> None:
        self.pub_socket.close()
        self.sub_socket.close()
        self.broker.stop()
        super().tearDown()

    def test_test_client_raises_on_invalid_message(self):
        client = TestClient(self.broker)
        client.start()
        client.subscribe(b"topic")

        self.pub_socket.send_multipart((b"topic", b"many", b"parts"))
        with self.assertRaises(TimeoutError):
            client.wait_for_message(filter=lambda x: True)

        self.assertFalse(client.is_alive())

    def test_single_part(self):
        self.pub_socket.send_multipart((b"topic",))
        with self.assertLogs() as cm:
            res = receive_message_from_socket(self.sub_socket)
        self.assertEqual(res, (None, None))
        self.assertIn("invalid number of parts: 1", str(cm.output))

    def test_three_parts(self):
        self.pub_socket.send_multipart((b"topic", b"many", b"parts"))
        with self.assertLogs() as cm:
            res = receive_message_from_socket(self.sub_socket)
        self.assertEqual(res, (None, None))
        self.assertIn("invalid number of parts: 3", str(cm.output))

    def test_invalid_json(self):
        self.pub_socket.send_multipart((b"topic", b"ma-_:\"ny"))
        with self.assertLogs() as cm:
            res = receive_message_from_socket(self.sub_socket)
        self.assertEqual(res, (None, None))
        self.assertIn("invalid json", str(cm.output))

    def test_not_a_dict(self):
        payload = b'"asd"'
        self.assertEqual("asd", orjson.loads(payload))

        self.pub_socket.send_multipart((b"topic", payload))
        with self.assertLogs() as cm:
            res = receive_message_from_socket(self.sub_socket)
        self.assertEqual(res, (None, None))
        self.assertIn("not a dict", str(cm.output))


class WaitForConnectionTestCase(OpenModuleCoreTestMixin, TestCase):
    protocol = "tcp://"

    def test_wait_for_connection_uses_core(self):
        wait_for_connection(self.core.messages)

    def test_wait_for_connection(self):
        pub_socket = get_pub_socket(self.zmq_context(), self.zmq_config())
        wait_for_connection(self.core.messages, pub_socket)

    def test_wait_for_connection_timeout(self):
        try:
            with override_context(BROKER_SUB="tcp://127.0.0.1:900"):
                incorrect_pub_socket = get_pub_socket(self.zmq_context(), self.zmq_config())

            with self.assertRaises(TimeoutError):
                wait_for_connection(self.core.messages, incorrect_pub_socket, timeout=3)
        finally:
            incorrect_pub_socket.close()
