import logging
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Union, Callable
from unittest import TestCase
from uuid import uuid4

from pydantic.types import conint

from openmodule.config import settings, override_context
from openmodule.models.base import OpenModuleModel, EmptyModel, ZMQMessage
from openmodule.rpc import server
from openmodule.rpc.client import RPCClient
from openmodule.rpc.common import channel_to_response_topic, channel_to_request_topic
from openmodule.rpc.server import RPCServer, RPCRequest
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.rpc import RPCServerTestMixin


def _fake_request(gate=..., direction=...):
    gateway = {}
    if gate != Ellipsis:
        gateway["gate"] = gate
    if direction != Ellipsis:
        gateway["direction"] = direction

    request = {}
    if gateway:
        request["gateway"] = gateway

    return request


class RPCCommonTestCase(TestCase):
    def test_topics(self):
        self.assertEqual(b"rpc-rep-test", channel_to_response_topic(b"test"))
        self.assertEqual(b"rpc-req-test", channel_to_request_topic(b"test"))

    def test_gateway_filter(self):
        filter_full = server.gateway_filter("gate1", "in")
        self.assertTrue(filter_full(_fake_request(gate="gate1", direction="in"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate1", direction="out"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2", direction="in"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2", direction="out"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_full(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_full(_fake_request(direction="in"), None, None))
        self.assertFalse(filter_full(_fake_request(direction="out"), None, None))
        self.assertFalse(filter_full(_fake_request(), None, None))

        filter_direction = server.gateway_filter(direction="in")
        self.assertTrue(filter_direction(_fake_request(gate="gate1", direction="in"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate1", direction="out"), None, None))
        self.assertTrue(filter_direction(_fake_request(gate="gate2", direction="in"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate2", direction="out"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_direction(_fake_request(gate="gate2"), None, None))
        self.assertTrue(filter_direction(_fake_request(direction="in"), None, None))
        self.assertFalse(filter_direction(_fake_request(direction="out"), None, None))
        self.assertFalse(filter_direction(_fake_request(), None, None))

        filter_gate = server.gateway_filter(gate="gate1")
        self.assertTrue(filter_gate(_fake_request(gate="gate1", direction="in"), None, None))
        self.assertTrue(filter_gate(_fake_request(gate="gate1", direction="out"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2", direction="in"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2", direction="out"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_gate(_fake_request(gate="gate2"), None, None))
        self.assertFalse(filter_gate(_fake_request(direction="in"), None, None))
        self.assertFalse(filter_gate(_fake_request(direction="out"), None, None))
        self.assertFalse(filter_gate(_fake_request(), None, None))


class TestRPCRequest(OpenModuleModel):
    __test__ = False
    pass


class TestRPCResponse(OpenModuleModel):
    __test__ = False
    pass


class TestRPCResponse2(OpenModuleModel):
    __test__ = False
    some_payload: str


class RPCServerTestCase(RPCServerTestMixin):
    rpc_channels = ["channel", "channel2", "a", "ab"]
    topics = ["test"]

    server: RPCServer

    def setUp(self):
        super().setUp()
        self.called_types = {}
        self.server = RPCServer(self.zmq_context())
        self.server_thread = self.server.run_as_thread()

    def tearDown(self):
        self.server.shutdown()
        self.server_thread.join()
        super().tearDown()

    def set_called(self, request, message: RPCRequest, value=True):
        """test rpc handler"""
        self.called_types[message.type] = value

    def set_called_value(self, value):
        return partial(self.set_called, value=value)

    def test_invalid_rpc_request(self):
        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        rpc_request = RPCRequest(name="testclient", type="test-type", rpc_id=uuid4(), request={})
        broken_data = rpc_request.dict()
        del broken_data["rpc_id"]
        self.zmq_client.send(f"rpc-req-channel".encode("ascii"), broken_data)

        _, error_response = self.zmq_client.wait_for_message(
            filter=lambda topic, message: topic == b"rpc-rep-channel" and message.get("type") == "unknown"
        )
        self.assertIsNone(error_response.get("rpc_id"))

    def test_no_filter(self):
        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        self.rpc("channel", "test-type", {})
        self.assertTrue(self.called_types.get("test-type"))

    def test_exception_in_filter_function(self):
        def bad_filter(*args, **kwargs) -> bool:
            raise Exception("Error123")

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)
        self.server.add_filter(bad_filter)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCFailure(response, "filter_error")
        self.assertEqual("Error123", response["response"]["exception"])

    def test_filter(self):
        def allow_only_type_test(message: RPCRequest, **kwargs) -> bool:
            return message.type == "test-type"

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.server.register_handler("channel", "test-type2", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)
        self.assertTrue(self.called_types.get("test-type"))

        response = self.rpc("channel", "test-type2", {})
        self.assertTrue(self.called_types.get("test-type2"))
        self.assertRPCSuccess(response)

        # clear stats, and add the filter
        del self.called_types["test-type"]
        del self.called_types["test-type2"]
        self.server.add_filter(allow_only_type_test)

        # should still work as before
        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)
        self.assertTrue(self.called_types.get("test-type"))

        # times out
        with self.assertRaises(TimeoutError):
            self.rpc("channel", "test-type2", {})
        self.assertNotIn("test-type2", self.called_types)

    def test_filter_channel_type(self):
        def f(*args, **kwargs):
            return False

        def check_ok():
            response = self.rpc("channel", "test-type", {})
            self.assertRPCSuccess(response)
            self.assertTrue(self.called_types.get("test-type"))
            self.called_types.clear()

        def check_not_called():
            with self.assertRaises(TimeoutError):
                response = self.rpc("channel", "test-type", {})
            self.assertEqual(None, self.called_types.get("test-type"))
            self.called_types.clear()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)

        self.server.add_filter(f, "abc")
        check_ok()

        self.server.add_filter(f, "channel", "abc")
        check_ok()

        self.server.add_filter(f, "channel")
        check_not_called()

        self.server.filters.clear()
        self.server.add_filter(f, "channel", "test-type")
        check_not_called()

    def test_can_only_register_once(self):
        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.wait_for_rpc_server(self.server)
        with self.assertRaises(ValueError) as e:
            self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, self.set_called)
        self.assertIn("already registered", str(e.exception))

    def test_exception_in_handler(self):
        def handler(*_, **__):
            """ test rpc handler"""
            raise Exception("Error123")

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCFailure(response, "handler_error")
        self.assertEqual("Error123", response["response"]["exception"])

    def test_handler_returns_none(self):
        def handler(*_, **__):
            """ test rpc handler"""
            return None

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_dict(self):
        def handler(*_, **__):
            """ test rpc handler"""
            return {}

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_model(self):
        def handler(*_, **__):
            """ test rpc handler"""
            return TestRPCResponse()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_wrong_dict(self):
        def bad_handler(*_, **__):
            """ test rpc handler"""
            return {}

        def good_handler(*_, **__):
            """ test rpc handler"""
            return {"some_payload": "test"}

        self.server.register_handler("channel", "test-type1", TestRPCRequest, TestRPCResponse2, bad_handler)
        self.server.register_handler("channel", "test-type2", TestRPCRequest, TestRPCResponse2, good_handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type1", {})
        self.assertRPCFailure(response, "handler_error")

        response = self.rpc("channel", "test-type2", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_wrong_response_type(self):
        def bad_handler(*_, **__):
            """ test rpc handler"""
            return TestRPCResponse()

        def good_handler(*_, **__):
            """ test rpc handler"""
            return TestRPCResponse2(some_payload="test")

        self.server.register_handler("channel", "test-type1", TestRPCRequest, TestRPCResponse2, bad_handler)
        self.server.register_handler("channel", "test-type2", TestRPCRequest, TestRPCResponse2, good_handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type1", {})
        self.assertRPCFailure(response, "handler_error")

        response = self.rpc("channel", "test-type2", {})
        self.assertRPCSuccess(response)

    def test_handler_returns_additional_data(self):
        """
        additional data is dropped, just as the serializer dictates
        """

        def too_much_handler(*_, **__):
            """ test rpc handler"""
            return {"some_payload": "test", "nobody_wants_you": ":("}

        self.server.register_handler("channel", "test-type1", TestRPCRequest, TestRPCResponse2, too_much_handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type1", {})
        self.assertRPCSuccess(response)
        self.assertDictEqual(response["response"], {"some_payload": "test", "status": "ok"})

    def test_serializer_error(self):
        class SomeValidator(OpenModuleModel):
            max_int: conint(gt=0, lt=10)

        def handler(*_, **__):
            """ test rpc handler"""
            pass

        self.server.register_handler("channel", "test-type", SomeValidator, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        self.assertRPCSuccess(self.rpc("channel", "test-type", {"max_int": 1}))
        self.assertRPCSuccess(self.rpc("channel", "test-type", {"max_int": 5}))
        self.assertRPCFailure(self.rpc("channel", "test-type", {"max_int": 0}), "validation_error")
        self.assertRPCFailure(self.rpc("channel", "test-type", {"max_int": 10}), "validation_error")

    def test_no_handler_found(self):
        def handler(*_, **__):
            """ test rpc handler"""
            return TestRPCResponse()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler)
        self.wait_for_rpc_server(self.server)

        response = self.rpc("channel", "test-type", {})  # correct type and channel
        self.assertRPCSuccess(response)

        with self.assertRaises(TimeoutError):  # wrong type
            self.rpc("channel", "test-type-doesnotexist", {})

        with self.assertRaises(TimeoutError):  # wrong channel (correct prefix chosen on purpose)
            self.rpc("channel2", "test-type", {})

        with self.assertRaises(TimeoutError):  # wrong everything
            self.rpc("channel2", "test-type-doesnotexist", {})

    def test_correct_resource(self):
        def handler1(*_, **__):
            """ test rpc handler"""
            logging.info("handler 1")
            return TestRPCResponse()

        self.server.register_handler("channel", "test-type", TestRPCRequest, TestRPCResponse, handler1)
        self.wait_for_rpc_server(self.server)

        with self.assertLogs() as cm:
            response = self.rpc("channel", "test-type", {}, resource=None)
        self.assertRPCSuccess(response)
        self.assertIn("handler 1", str(cm.output))

        with self.assertLogs() as cm:
            response = self.rpc("channel", "test-type", {}, resource=settings.RESOURCE)
        self.assertRPCSuccess(response)
        self.assertIn("handler 1", str(cm.output))

        with self.assertRaises(TimeoutError):
            self.rpc("channel", "test-type", {}, resource="test-2")

    def test_prefix_matched_topic(self):
        def handler1(*_, **__):
            """ test rpc handler"""
            logging.info("handler 1")
            return TestRPCResponse()

        self.server.register_handler("a", "test-type", TestRPCRequest, TestRPCResponse, handler1)
        self.wait_for_rpc_server(self.server)

        with self.assertLogs() as cm:
            # we use assertLogs here to capture log output, but we would need assertNoLogs from python3.10
            # so we log some dummy message and check assertNotIn afterwards
            logging.info("some-log-so assert works")

            with self.assertRaises(TimeoutError):
                self.rpc("ab", "test-type", {})

        self.assertNotIn("no handler found", str(cm.output))

    def test_union_response_parsing(self):
        """
        tests that the rpc server correctly response when Union types are used as responses
        """

        class Integer(OpenModuleModel):
            some_int: int

        class String(OpenModuleModel):
            some_str: str

        def dict_handler(*_, **__):
            """Test handler."""
            return {"some_str": "str"}

        def integer_handler(*_, **__):
            """Test handler."""
            return Integer(some_int=1)

        def string_handler(*_, **__):
            """Test handler."""
            return String(some_str=1)

        def none_handler(*_, **__):
            """Test handler."""
            return

        def test_response_handler(*_, **__):
            """Test handler."""
            return TestRPCResponse()

        class response_type(OpenModuleModel):
            __root__: Union[Integer, String]

        self.server.register_handler("channel", "dict", EmptyModel, response_type, dict_handler)
        self.server.register_handler("channel", "string", EmptyModel, response_type, string_handler)
        self.server.register_handler("channel", "integer", EmptyModel, response_type, integer_handler)
        self.server.register_handler("channel", "none", EmptyModel, response_type, none_handler)
        self.server.register_handler("channel", "test_response", EmptyModel, response_type, test_response_handler)
        self.wait_for_rpc_server(self.server)

        # dict, should work
        response = self.rpc("channel", "dict", {}, resource=None)
        self.assertRPCSuccess(response)
        self.assertEqual(response["response"], {"some_str": "str", "status": "ok"})

        # string response, should work
        response = self.rpc("channel", "string", {}, resource=None)
        self.assertRPCSuccess(response)
        self.assertEqual(response["response"], {"some_str": "1", "status": "ok"})

        # integer response, should work
        response = self.rpc("channel", "integer", {}, resource=None)
        self.assertRPCSuccess(response)
        self.assertEqual(response["response"], {"some_int": 1, "status": "ok"})

        # none response, should not work, as required fields are not set
        response = self.rpc("channel", "none", {}, resource=None)
        self.assertGreater(response["response"].items(), {"status": "handler_error"}.items())

        # test_response, an incorrect response should not work
        response = self.rpc("channel", "none", {}, resource=None)
        self.assertGreater(response["response"].items(), {"status": "handler_error"}.items())

    def test_async_receive(self):
        """
        this test cases shows a usage example for async receive. The handler emits a message before the
        rpc response. in this case we need to first capture the response. This is a limitation because
        the rpc mixin uses the same zmq client as the other wait for message functions
        """

        def publishing_handler(*_, **__):
            """test handler which publishes a message"""
            message = ZMQMessage(type="abc")
            message.publish_on_topic(self.server.pub, b"test")

        self.server.register_handler("channel", "test", EmptyModel, EmptyModel, publishing_handler)
        self.wait_for_rpc_server(self.server)

        # this shows the current limitation in the test framework, if we ever do change the setup to better
        # support capturing messages from multiple topics, case will fail
        response = self.rpc("channel", "test", EmptyModel())
        self.assertRPCSuccess(response)
        with self.assertRaises(TimeoutError):
            self.zmq_client.wait_for_message_on_topic(b"test")

        # this shows how we can capture the message
        rpc_id = self.rpc("channel", "test", EmptyModel(), receive_response=False)
        message = self.zmq_client.wait_for_message_on_topic(b"test")
        self.assertEqual(message["type"], "abc")
        response = self.receive_rpc_response("channel", rpc_id)
        self.assertRPCSuccess(response)


class RpcClientTest(RPCServerTestMixin, OpenModuleCoreTestMixin):
    rpc_channels = ["channel"]

    @staticmethod
    def handler1(*_, **__):
        """test handler"""
        logging.info("handler 1")
        return TestRPCResponse2(some_payload="abc")

    @staticmethod
    def timeout_handler(*_, **__):
        """test handler"""
        logging.info("timout_handler")
        time.sleep(3)
        return TestRPCResponse2(some_payload="abc")

    def setUp(self):
        super().setUp()
        self.server = RPCServer(context=self.zmq_context(), filter_resource=False)
        self.server.register_handler("channel", "test", TestRPCRequest, TestRPCResponse2, self.handler1)
        self.server.register_handler("channel", "timeout", TestRPCRequest, TestRPCResponse2, self.timeout_handler)
        self.server.run_as_thread()
        self.wait_for_rpc_server(self.server)

        self.client = RPCClient(self.core.messages, channels=[b"channel"], _warn=False)
        self.wait_for_dispatcher(self.core.messages)

    def test_blocking(self):
        result = self.client.rpc(b"channel", "test", EmptyModel(), timeout=1)
        self.assertEqual("ok", result.status)

        with self.assertRaises(TimeoutError):
            self.client.rpc(b"channel", "timeout", EmptyModel(), timeout=1)

    def test_non_blocking(self):
        result = self.client.rpc(b"channel", "test", EmptyModel(), timeout=1, blocking=False)
        self.assertFalse(None, result.done())
        self.assertEqual(None, result.response)

        time.sleep(1)

        self.assertTrue(result.done())
        result = result.result()
        self.assertEqual("ok", result.status)
        self.assertIn("some_payload", result.response)

    def test_non_blocking_via_result(self):
        result = self.client.rpc(b"channel", "test", EmptyModel(), timeout=1, blocking=False)
        result = result.result()
        self.assertEqual("ok", result.status)
        self.assertIn("some_payload", result.response)

    def test_non_blocking_timeout(self):
        result = self.client.rpc(b"channel", "timeout", EmptyModel(), timeout=1, blocking=False)
        with self.assertRaises(TimeoutError):
            result.result(timeout=1)

    def test_non_blocking_higher_timeout_than_at_request(self):
        result = self.client.rpc(b"channel", "timeout", EmptyModel(), timeout=1, blocking=False)
        with self.assertRaises(TimeoutError):
            with self.assertWarns(UserWarning) as cm:
                result.result(timeout=2)
        self.assertIn("cannot extend", str(cm.warnings[0].message))

    def test_non_blocking_no_timeout(self):
        result = self.client.rpc(b"channel", "timeout", EmptyModel(), timeout=4, blocking=False)
        result = result.result()
        self.assertEqual("ok", result.status)
        self.assertIn("some_payload", result.response)

    def test_proactive_timeout(self):
        """
        tests a case where the rpc result is cehcked after the timeout, in this case
        we time-out immediately
        """
        result = self.client.rpc(b"channel", "timeout", EmptyModel(), timeout=1, blocking=False)
        time.sleep(2)
        start = time.time()
        with self.assertRaises(TimeoutError):
            result.result()
        duration = time.time() - start
        self.assertTrue(duration < 0.5)

    def test_maximum_wait_time(self):
        """
        tests that we can atmost wait for the maximum timeout since the *request was sent*
        because the cleanup will clean the message internally anways, there is no point in
        waiting for a longer duration
        """
        result = self.client.rpc(b"channel", "does-not-exist", EmptyModel(), timeout=4, blocking=False)
        time.sleep(2)
        start = time.time()
        with self.assertRaises(TimeoutError):
            result.result()
        duration = time.time() - start
        # we waited 2 seconds before starting the result() call
        # thus the result call can only wait ~2 seconds, since the total timeout is 4 seconds
        self.assertTrue(1.5 < duration < 2.5)

    def test_no_proactive_timeout_if_received_in_time(self):
        """
        this test ensures that if we call .result() _after_ the timeout,
        but the response was received _within_ the timeout, that the
        result is still retrievable
        """
        result = self.client.rpc(b"channel", "test", EmptyModel(), timeout=1, blocking=False)
        time.sleep(3)
        self.assertTrue(result.done())
        result = result.result()
        self.assertEqual("ok", result.status)
        self.assertIn("some_payload", result.response)


class TestRPCResponseNotSerializable(OpenModuleModel):
    __test__ = False
    some_payload: Callable


class RPCServerMultithreadingTest(OpenModuleCoreTestMixin, TestCase):
    """
    serialization errors were not captured in multithreaded rpc server
    this testcase ensures that this is not the case anymore
    """

    rpc_channels = ["test"]
    topics = ["sentry"]
    init_kwargs = {"sentry": True}

    def raise_exception_handler(self, _, __):
        """
        returns a model which cannot be serialized to json
        """
        return {"some_payload": self.rpc}

    def setUp(self):
        super().setUp()

        self.executor = ThreadPoolExecutor(max_workers=3)
        self.server = RPCServer(self.zmq_context(), executor=self.executor)
        self.server.register_handler("test", "test", EmptyModel, TestRPCResponseNotSerializable,
                                     self.raise_exception_handler, register_schema=False)
        self.server.run_as_thread()

    def tearDown(self):
        super().tearDown()
        self.server.shutdown()

    def test_executor_logs_exceptions(self):
        """
        ensures that when using a multiprocessing executor exceptions are logged to logging and sentry
        """
        with self.assertLogs(level=logging.ERROR) as cm:
            self.rpc("test", "test", EmptyModel(), receive_response=False)
            self.zmq_client.wait_for_message_on_topic(b"sentry")
        self.assertTrue(cm.output)


