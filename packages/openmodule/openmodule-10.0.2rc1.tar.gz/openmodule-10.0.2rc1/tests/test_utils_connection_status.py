from unittest import TestCase, mock

from openmodule.core import init_openmodule, OpenModuleCore, shutdown_openmodule
from openmodule.dispatcher import MessageDispatcher
from openmodule.utils.connection_status import ConnectionStatusListener, ConnectionStatusMessage
from openmodule_test.eventlistener import MockEvent
from openmodule_test.health import HealthTestMixin
from openmodule_test.zeromq import ZMQTestMixin


class ConnectionStatusTestCase(TestCase):
    on_connect: mock.Mock
    on_disconnect: mock.Mock
    connection_status: ConnectionStatusListener

    def setUp(self):
        self.dispatcher = MessageDispatcher()
        self.connection_status = ConnectionStatusListener(self.dispatcher)

        self.on_connect = mock.Mock(name="on_connect")
        self.on_disconnect = mock.Mock(name="on_disconnect")
        self.connection_status.on_connect.append(self.on_connect)
        self.connection_status.on_disconnect.append(self.on_disconnect)

    def dispatch_status(self, connected: bool):
        self.dispatcher.dispatch(b"connection_status", ConnectionStatusMessage(name="dummy", connected=connected))

    def test_initial_status_is_connected(self):
        self.assertTrue(self.connection_status.connected)

    def test_first_connected_is_always_sent(self):
        # the first on_connect is always sent, because we could startup, not knowing that we are actually disconnected
        self.assertTrue(self.connection_status.connected)
        self.dispatch_status(True)
        self.on_connect.assert_called_once()

        # second on_connect is not sent
        self.dispatch_status(True)
        self.on_connect.assert_called_once()

    def test_event_listener_is_called_once(self):
        self.dispatch_status(False)
        self.on_disconnect.assert_called_once()

        # two connect events, on_connect should only be called once
        self.dispatch_status(True)
        self.dispatch_status(True)
        self.on_connect.assert_called_once()

        # two disconnect events, still on_disconnect should be called once more
        self.dispatch_status(False)
        self.dispatch_status(False)
        self.on_connect.assert_called_once()
        self.assertEqual(self.on_disconnect.call_count, 2)

    def test_connected_member_is_changed(self):
        self.assertTrue(self.connection_status.connected)

        self.dispatch_status(False)
        self.assertFalse(self.connection_status.connected)
        self.on_connect.assert_not_called()
        self.on_disconnect.assert_called_once()

        self.dispatch_status(True)
        self.assertTrue(self.connection_status.connected)
        self.on_connect.assert_called_once()
        self.on_disconnect.assert_called_once()


class ConnectionStatusWithCoreTestCase(HealthTestMixin, ZMQTestMixin, TestCase):
    topics = ["healthz"]
    core: OpenModuleCore

    def setUp(self):
        super().setUp()
        self.core = init_openmodule(self.zmq_config(), context=self.zmq_context())
        self.connection_status = ConnectionStatusListener(self.core.messages)
        self.on_connect = MockEvent(name="on_connect")
        self.on_disconnect = MockEvent(name="on_disconnect")
        self.connection_status.on_connect.append(self.on_connect)
        self.connection_status.on_disconnect.append(self.on_disconnect)
        self.wait_for_dispatcher(self.core.messages)

    def tearDown(self):
        shutdown_openmodule()
        super().tearDown()

    def send_status(self, connected: bool):
        self.zmq_client.send(b"connection_status", ConnectionStatusMessage(connected=connected, name="testclient"))

    def test_connected_member_is_changed(self):
        self.assertTrue(self.connection_status.connected)

        # simulate a disconnect event
        self.on_disconnect.assert_not_called()
        self.send_status(False)
        self.on_disconnect.wait_for_call()
        self.on_connect.assert_not_called()
        self.assertFalse(self.connection_status.connected)

        # simulate a connect event
        MockEvent.reset_all_mocks()
        self.send_status(True)
        self.on_connect.wait_for_call()
        self.assertTrue(self.connection_status.connected)
        self.on_disconnect.assert_not_called()
