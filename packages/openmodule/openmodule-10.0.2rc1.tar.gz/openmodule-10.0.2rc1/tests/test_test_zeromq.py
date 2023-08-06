import threading
import time
from unittest import TestCase

import zmq

from openmodule.config import settings, override_settings
from openmodule_test.utils import DeveloperError
from openmodule_test.zeromq import patch_bind_string, TestBroker, TestClient, fake_config, ZMQTestMixin


class ZMQUtilsTest(TestCase):
    def test_patch_zmq_bind_str(self):
        self.assertEqual("tcp://127.0.0.1:10100", patch_bind_string("tcp://*:10100"))
        self.assertEqual("tcp://0.0.0.0:10100", patch_bind_string("tcp://0.0.0.0:10100"))
        self.assertEqual("unix:///tmp/asdf", patch_bind_string("unix:///tmp/asdf"))
        self.assertEqual("inproc://endpoint", patch_bind_string("inproc://endpoint"))

    def test_fake_config(self):
        broker = TestBroker("inproc://sub", "inproc://pub")
        config = fake_config(broker)

        self.assertEqual("inproc://pub", config.BROKER_PUB)
        self.assertEqual("inproc://sub", config.BROKER_SUB)


class TestBrokerTest(TestCase):
    def test_start_and_stop(self):
        broker = TestBroker("tcp://127.0.0.1:10001", "tcp://127.0.0.1:10002")
        broker.start()
        broker.stop()

    def _run_message_test(self, sub, pub):
        broker = TestBroker(sub, pub)
        broker.start()

        pub_socket = broker.context.socket(zmq.PUB)
        sub_socket = broker.context.socket(zmq.SUB)

        try:
            pub_socket.connect(sub)
            sub_socket.connect(pub)
            sub_socket.subscribe(b"test-topic")

            # sleep to prevent slow joiner
            time.sleep(1)

            pub_socket.send_multipart((b"test-topic", b"message"))
            topic, message = sub_socket.recv_multipart()

            self.assertEqual(b"test-topic", topic)
            self.assertEqual(b"message", message)

        finally:
            pub_socket.close()
            sub_socket.close()
            broker.stop()

    def test_single_message_tcp(self):
        self._run_message_test(
            "tcp://127.0.0.1:10003",
            "tcp://127.0.0.1:10004",
        )

    def test_single_message_inproc(self):
        self._run_message_test(
            "inproc://sub",
            "inproc://pub",
        )


class TestClientTest(TestCase):
    def test_detect_infinite_linger(self):
        broker = TestBroker("tcp://127.0.0.1:10099", "tcp://127.0.0.1:10098")
        broker.start()

        socket = broker.context.socket(zmq.PUB)
        socket.connect("tcp://127.0.0.1:10098")

        with self.assertRaises(AssertionError) as e:
            broker.stop()
        self.assertIn("linger", str(e.exception).lower())

    def _run_test_start_and_stop(self, sub, pub):
        broker = TestBroker(sub, pub)
        broker.start()

        client = TestClient(broker)
        client.start()

        broker.stop()
        client.stop()

    def test_start_and_stop_tcp(self):
        self._run_test_start_and_stop(
            "tcp://127.0.0.1:10007",
            "tcp://127.0.0.1:10008",
        )

    def test_start_and_stop_inproc(self):
        self._run_test_start_and_stop(
            "inproc://sub",
            "inproc://pub",
        )

    def test_recv_timeout_during_other_messages(self):
        # test client has two timeout conditions
        # - no message received at all during <timeout>
        # - some messages received during <timeout> but not the one we want
        # this case tests the second one
        broker = TestBroker("tcp://127.0.0.1:10009", "tcp://127.0.0.1:10010")
        broker.start()

        client = TestClient(broker)
        client.start()

        try:
            client.subscribe(b"test1", b"test2")

            def spam():
                for x in range(15):
                    client.send(b"test1", type="some-type", data="yes!")
                    time.sleep(0.1)

            spammer = threading.Thread(target=spam)
            spammer.start()

            with self.assertRaises(TimeoutError):
                client.wait_for_message_on_topic(b"test2", timeout=0.5)

            spammer.join()

        finally:
            client.stop()
            broker.stop()

    def test_one_client_in_two_threads(self):
        broker = TestBroker("tcp://127.0.0.1:10011", "tcp://127.0.0.1:10012")
        broker.start()

        client = TestClient(broker)
        client.start()
        client.subscribe(b"test")

        try:
            counter_lock = threading.Lock()
            assertions = 0

            def second_thread_func():
                nonlocal assertions
                try:
                    client.wait_for_message_on_topic(b"test")
                except DeveloperError as e:  # pragma: no cover
                    self.assertIn("the test client is not thread safe", str(e))
                    with counter_lock:
                        assertions += 1
                except TimeoutError:  # pragma: no cover
                    pass

            second_thread = threading.Thread(target=second_thread_func)
            second_thread.start()

            try:
                client.wait_for_message_on_topic(b"test")
            except DeveloperError as e:  # pragma: no cover
                self.assertIn("the test client is not thread safe", str(e))
                with counter_lock:
                    assertions += 1
            except TimeoutError:  # pragma: no cover
                pass

            second_thread.join()

            self.assertEqual(1, assertions)

        finally:
            client.stop()
            broker.stop()

    def test_two_clients(self):
        # two clients should be able to start and stop independently
        broker = TestBroker("tcp://127.0.0.1:10013", "tcp://127.0.0.1:10014")
        broker.start()

        client1 = TestClient(broker)
        client1.start()

        client2 = TestClient(broker)
        client2.start()

        try:
            client1.stop()

            client2.subscribe(b"test")
            client2.send(b"test", type="some-type", data="yes!")
            message = client2.wait_for_message_on_topic(b"test")
            self.assertEqual("yes!", message["data"])
        finally:
            client2.stop()
            broker.stop()

    def test_recv_message(self):
        broker = TestBroker("tcp://127.0.0.1:10015", "tcp://127.0.0.1:10016")
        broker.start()

        client = TestClient(broker)
        client.start()

        try:
            # this assertion catches developer errors, we cannot receive on a not-subscribed topic
            with self.assertRaises(DeveloperError) as e:
                client.wait_for_message_on_topic(b"test")
            self.assertIn("please subscribe", str(e.exception))

            # receive a message
            client.subscribe(b"test")
            client.send(b"test", type="some-type", data="yes!")
            message = client.wait_for_message_on_topic(b"test")
            self.assertEqual("yes!", message["data"])

            # receive a second time -> timeout
            with self.assertRaises(TimeoutError):
                client.wait_for_message_on_topic(b"test")

        finally:
            client.stop()
            broker.stop()


class ZMQTestMixinTCPTest(ZMQTestMixin, TestCase):
    topics = ["test"]
    protocol = "tcp://"

    def test_send_and_receive(self):
        self.assertTrue(self.zmq_config().BROKER_PUB.startswith("tcp://"))
        self.assertTrue(self.zmq_config().BROKER_SUB.startswith("tcp://"))

        self.zmq_client.send(b"test", type="some-type", data="yes!")
        message = self.zmq_client.wait_for_message_on_topic(b"test")
        self.assertEqual("yes!", message["data"])

    def test_client_ignores_ping_commands(self):
        # we do not want to accidentially receive ping commands used during connecting in our tests
        self.zmq_client.send(b"test", type="some-type", data="yes!")
        self.zmq_client.wait_for_message_on_topic(b"test")

        self.zmq_client._zmq_cmd("some-command", topic=b"test")
        with self.assertRaises(TimeoutError):
            self.zmq_client.wait_for_message_on_topic(b"test")


@override_settings(BROKER_SUB="tcp://127.0.0.1:1234",
                   BROKER_PUB="tcp://127.0.0.1:1236")
class ZMQTestMixinInprocTest(ZMQTestMixin, TestCase):
    """
    ensures that the protocol variable is actually considered during test broker startup
    this is to check for a bug we introduced in 11a75bf0ae5556d058ae4f1bee4fc1eae5f655e2
    """
    topics = ["test"]
    protocol = "inproc://"

    def test_send_and_receive(self):
        self.assertTrue(self.zmq_config().BROKER_PUB.startswith("inproc://"))
        self.assertTrue(self.zmq_config().BROKER_SUB.startswith("inproc://"))

        self.zmq_client.send(b"test", type="some-type", data="yes!")
        message = self.zmq_client.wait_for_message_on_topic(b"test")
        self.assertEqual("yes!", message["data"])

    def test_client_ignores_ping_commands(self):
        # we do not want to accidentially receive ping commands used during connecting in our tests
        self.zmq_client.send(b"test", type="some-type", data="yes!")
        self.zmq_client.wait_for_message_on_topic(b"test")

        self.zmq_client._zmq_cmd("some-command", topic=b"test")
        with self.assertRaises(TimeoutError):
            self.zmq_client.wait_for_message_on_topic(b"test")


class ZMQTestMixinTest(ZMQTestMixin, TestCase):
    topics = ["test"]
    rpc_channels = ["channel"]

    def test_send_and_receive(self):
        self.zmq_client.send(b"test", type="some-type", data="yes!")
        message = self.zmq_client.wait_for_message_on_topic(b"test")
        self.assertEqual("yes!", message["data"])

    def test_rpc(self):
        rpc_server_client = TestClient(self.zmq_broker)
        rpc_server_client.start()
        rpc_server_client.subscribe(b"rpc-req-channel")

        def fake_rpc_server():
            message = rpc_server_client.wait_for_message_on_topic(b"rpc-req-channel")
            rpc_server_client.send(b"rpc-rep-channel", type="type", response={"test": "yes"}, rpc_id=message["rpc_id"])

        rpc_server = threading.Thread(target=fake_rpc_server)
        rpc_server.start()

        self.rpc("channel", "type", {"some-request": True})

        rpc_server.join()
        rpc_server_client.stop()
