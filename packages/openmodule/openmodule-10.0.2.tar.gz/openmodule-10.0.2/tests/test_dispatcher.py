from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from typing import Any
from unittest import TestCase

from openmodule.config import settings
from openmodule.dispatcher import MessageDispatcher, SubscribingMessageDispatcher
from openmodule.models.base import ZMQMessage, OpenModuleModel
from openmodule.utils.io import IoListener
from openmodule.utils.presence import PresenceListener


class MessageDispatcherBaseTest(TestCase):
    dispatcher: MessageDispatcher
    message: Any

    def dummy_message(self, type="test", **kwargs):
        return {"type": type, "name": "testclient", **kwargs}

    def _set_true_handler(self, message, var="message"):
        """test handler"""
        setattr(self, var, message)

    def setUp(self):
        super().setUp()
        self.dispatcher = MessageDispatcher()
        self.message = None

    def tearDown(self) -> None:
        settings.reset()
        super().tearDown()


class MessageDispatcherBasicsTestCase(MessageDispatcherBaseTest):
    def test_topic_is_str(self):
        self.dispatcher.register_handler("test", ZMQMessage, self._set_true_handler, match_type=False)
        self.assertIsNone(self.message)

        self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIsNotNone(self.message)

    def test_no_filter(self):
        self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler, match_type=False)
        self.assertIsNone(self.message)

        self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIsNotNone(self.message)

    def test_filter(self):
        self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler,
                                         match_type=False,
                                         filter=lambda msg: msg.get("type") == "some-type")

        # filter does not match
        self.dispatcher.dispatch(b"test", self.dummy_message(type="incorrect"))
        self.assertIsNone(self.message)

        # filter matches
        self.dispatcher.dispatch(b"test", self.dummy_message("some-type"))
        self.assertIsNotNone(self.message)

    def test_multiple_filter(self):
        # multiple handlers with identical filters and topics are allowed
        self.message1 = None
        self.message2 = None

        self.dispatcher.register_handler(b"test", ZMQMessage, partial(self._set_true_handler, var="message1"),
                                         match_type=False,
                                         filter=lambda msg: msg.get("type") == "some-type")
        self.dispatcher.register_handler(b"test", ZMQMessage, partial(self._set_true_handler, var="message2"),
                                         match_type=False,
                                         filter=lambda msg: msg.get("type") == "some-type")

        # filter does not match
        self.dispatcher.dispatch(b"test", self.dummy_message(type="incorrect"))
        self.assertIsNone(self.message1)
        self.assertIsNone(self.message2)

        # filter matches
        self.dispatcher.dispatch(b"test", self.dummy_message("some-type"))
        self.assertIsNotNone(self.message1)
        self.assertIsNotNone(self.message2)

    def test_prefix_does_not_match(self):
        # since zmq subscribes on all topics as prefixes, the dispatcher
        # has to full-match the topic
        self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler, match_type=False)
        self.dispatcher.dispatch(b"testp", self.dummy_message())
        self.assertIsNone(self.message)

        # exact match works
        self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIsNotNone(self.message)

    def test_match_type(self):
        class TypedZMQMessage(ZMQMessage):
            type: str = "test1"

        self.dispatcher.register_handler(b"test", TypedZMQMessage, self._set_true_handler, match_type=True)

        # wrong type does not match
        self.dispatcher.dispatch(b"test", ZMQMessage(type="test2"))
        self.assertIsNone(self.message)

        # correct type, message is dispatched
        self.dispatcher.dispatch(b"test", ZMQMessage(type="test1"))
        self.assertIsNotNone(self.message)

    def test_match_type_without_default_value(self):
        # empty string is also "false" thus not a valid type
        with self.assertRaises(AssertionError) as e:
            self.dispatcher.register_handler(b"test", ZMQMessage, self._set_true_handler, match_type=True)
        self.assertIn("class definition does not set a `type` field", str(e.exception))

        class MessageWithoutType(OpenModuleModel):
            pass

        with self.assertRaises(AssertionError) as e:
            self.dispatcher.register_handler(b"test", MessageWithoutType, self._set_true_handler, match_type=True)
        self.assertIn("class definition does not set a `type` field", str(e.exception))


class MessageDispatcherWithoutExecutorTestCase(MessageDispatcherBaseTest):
    def test_exception_in_handler(self):
        def raises_exception(message):
            raises_exception.register_schema = False
            raise Exception("something broke!")

        self.dispatcher.register_handler(b"test", ZMQMessage, raises_exception, register_schema=False, match_type=False)
        with self.assertLogs() as cm:
            self.dispatcher.dispatch(b"test", self.dummy_message())
        self.assertIn("something broke!", cm.output[0])

    def test_validation_error(self):
        def handler(x):
            pass

        handler.register_schema = False
        self.dispatcher.register_handler("test", ZMQMessage, handler, register_schema=False, match_type=False)
        with self.assertLogs() as cm:
            self.dispatcher.dispatch(b"test", {})
        self.assertIn("validation error", cm.output[0])


class MessageDispatcherWithExecutorTestCase(TestCase):
    def test_is_multithreaded(self):
        self.assertFalse(MessageDispatcher(executor=ThreadPoolExecutor(max_workers=1)).is_multi_threaded)
        self.assertFalse(MessageDispatcher(executor=ProcessPoolExecutor(max_workers=1)).is_multi_threaded)
        self.assertFalse(MessageDispatcher(executor=None).is_multi_threaded)

        self.assertTrue(MessageDispatcher(executor=dict(a=1)).is_multi_threaded)  # default fallback -> multithreaded
        self.assertTrue(MessageDispatcher(executor=ThreadPoolExecutor(max_workers=2)).is_multi_threaded)
        self.assertTrue(MessageDispatcher(executor=ProcessPoolExecutor(max_workers=2)).is_multi_threaded)

    def test_presence_listener_asserts_on_muiltithreaded_dispatcher(self):
        with self.assertRaises(AssertionError):
            PresenceListener(MessageDispatcher(executor=ThreadPoolExecutor(max_workers=2)))

    def test_io_listener_asserts_on_muiltithreaded_dispatcher(self):
        with self.assertRaises(AssertionError):
            IoListener(MessageDispatcher(executor=ThreadPoolExecutor(max_workers=2)))


class SubscribingMessageDispatcherTestCase(TestCase):
    subscriptions = set()

    def subscribe(self, topic):
        self.subscriptions.add(topic)

    def unsubscribe(self, topic):
        self.subscriptions.remove(topic)

    def setUp(self) -> None:
        self.subscriptions.clear()
        self.dispatcher = SubscribingMessageDispatcher(
            subscribe=self.subscribe,
            unsubscribe=self.unsubscribe
        )

    def test_subscribe(self):
        self.dispatcher.register_handler(b"topic1", ZMQMessage, lambda *x: x, register_schema=False, match_type=False)
        self.assertEqual({b"topic1"}, self.subscriptions)

    def test_unsubscribe(self):
        listener1 = self.dispatcher.register_handler(b"topic1", ZMQMessage, lambda *x: x,
                                                     register_schema=False, match_type=False)
        listener2 = self.dispatcher.register_handler(b"topic1", ZMQMessage, lambda *x: x,
                                                     register_schema=False, match_type=False)

        self.assertEqual({b"topic1"}, self.subscriptions)

        # listener 2 is still subscribed, topic should still be listed in subscriptions
        self.dispatcher.unregister_handler(listener1)
        self.assertEqual({b"topic1"}, self.subscriptions)

        # now no listener is subscribed anymore
        self.dispatcher.unregister_handler(listener2)
        self.assertEqual(set(), self.subscriptions)
