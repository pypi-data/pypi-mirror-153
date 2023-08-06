import time
from datetime import datetime
from unittest import TestCase

from openmodule.models.base import Gateway, ZMQMessage
from openmodule.utils.io import IoListener
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.eventlistener import MockEvent
from openmodule_test.io_simulator import IoSimulator, generate_example_states


class IoTest(OpenModuleCoreTestMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.io = IoListener(self.core.messages)
        io_init_event = MockEvent()
        self.core.messages.register_handler(b"io", ZMQMessage, handler=io_init_event, match_type=False)
        self.wait_for_dispatcher(self.core.messages)

        self.io_sim = IoSimulator(generate_example_states(count=18), emit=lambda x: self.zmq_client.send(b"io", x))

        # we have to wait here for the initial io states to settle
        # IMO we should move this into the simulator itself, or construct the testcases
        # in a way to not depend on this.
        io_init_event.wait_for_call(minimum_call_count=18)

    def tearDown(self):
        super().tearDown()

    def test_on_change_simple(self):
        on_any_edge = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_any(listen_to=pin, callback=on_any_edge)
        self.io_sim.change_pin_sate(pin)
        on_any_edge.wait_for_call()

    def test_on_no_change_simple(self):
        on_no_edge = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_none(listen_to=pin, callback=on_no_edge)
        self.io_sim.emit_current_pin_state(pin)
        on_no_edge.wait_for_call()
        on_no_edge.reset_all_mocks()
        self.io_sim.change_pin_sate(pin)
        with self.assertRaises(TimeoutError):
            on_no_edge.wait_for_call(timeout=1)

    def test_receive_all_messages_of_pin(self):
        on_all_messages = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_any(listen_to=pin, callback=on_all_messages)
        self.io.add_listener_edge_none(listen_to=pin, callback=on_all_messages)
        self.io_sim.change_pin_sate(pin)
        on_all_messages.wait_for_call()
        on_all_messages.reset_all_mocks()
        self.io_sim.change_pin_sate(pin)
        on_all_messages.wait_for_call()
        on_all_messages.reset_all_mocks()
        self.io_sim.emit_current_pin_state(pin)
        on_all_messages.wait_for_call()

    def test_receive_only_changes(self):
        on_any_edge = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_any(listen_to=pin, callback=on_any_edge)
        self.io_sim.change_pin_sate(pin)
        on_any_edge.wait_for_call()
        on_any_edge.reset_all_mocks()
        self.io_sim.emit_current_pin_state(pin)
        with self.assertRaises(TimeoutError):
            on_any_edge.wait_for_call(timeout=1)

    def test_missed_edge(self):
        on_any_edge = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_any(listen_to=pin, callback=on_any_edge)
        self.io_sim.emit_custom_io_message(pin=pin, value=1, edge=0)
        on_any_edge.wait_for_call()

    def test_on_open(self):
        on_rising_edge = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_rising(listen_to=pin, callback=on_rising_edge)
        self.io_sim.set_pin_high(pin)
        on_rising_edge.wait_for_call()
        on_rising_edge.reset_all_mocks()
        self.io_sim.set_pin_low(pin)
        with self.assertRaises(TimeoutError):
            on_rising_edge.wait_for_call(timeout=1)

    def test_on_close(self):
        on_falling_edge = MockEvent()
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io.add_listener_edge_falling(listen_to=pin, callback=on_falling_edge)
        self.io_sim.set_pin_high(pin)
        with self.assertRaises(TimeoutError):
            on_falling_edge.wait_for_call(timeout=1)
        on_falling_edge.reset_all_mocks()
        self.io_sim.set_pin_low(pin)
        on_falling_edge.wait_for_call()

    def test_listen_to_gateway(self):
        on_any_edge = MockEvent()
        gw = list(self.io_sim.get_pin_states().values())[0].gateway

        # check that the gateway direction does not matter for the filter
        # by explicitly setting sthe wrong direction
        self.assertEqual(gw.direction, "in")
        gateway = Gateway(gate=gw.gate, direction="out")

        self.io.add_listener_edge_any(listen_to=gateway, callback=on_any_edge)
        self.io_sim.set_pin_high(list(self.io_sim.get_pin_states().keys())[0])
        on_any_edge.wait_for_call()
        on_any_edge.reset_all_mocks()
        self.io_sim.set_pin_high(list(self.io_sim.get_pin_states().keys())[1])
        on_any_edge.wait_for_call()
        on_any_edge.reset_all_mocks()
        self.io_sim.set_pin_high(list(self.io_sim.get_pin_states().keys())[5])
        with self.assertRaises(TimeoutError):
            on_any_edge.wait_for_call(timeout=1)

    def test_is_pin_valid(self):
        pin = list(self.io_sim.get_pin_states().keys())[0]
        self.io_sim.emit_current_pin_state(pin)
        self.assertTrue(self.io.is_pin_valid(pin))
        time.sleep(2)
        self.assertFalse(self.io.is_pin_valid(pin=pin, timeout=1))

    def test_unknown_pin(self):
        pin = "pin_does_not_exist"
        self.assertFalse(self.io.is_pin_valid(pin=pin))
        state = self.io.get_pin_state(pin=pin)
        self.assertEqual(state.value, 0)
        self.assertEqual(state.gateway, Gateway(gate="", direction=""))
        self.assertEqual(state.pin, "")
        self.assertEqual(state.physical, 0)
        self.assertEqual(state.inverted, False)
        self.assertEqual(state.last_timestamp, datetime.fromtimestamp(0))

    def test_is_gateway_valid(self):
        pin = list(self.io_sim.get_pin_states().keys())[0]
        gateway = self.io_sim.get_pin_states()[pin].gateway
        self.io_sim.emit_current_pin_state(pin)
        self.assertTrue(self.io.is_gateway_valid(gateway))
        time.sleep(2)
        self.assertFalse(self.io.is_gateway_valid(gateway=gateway, timeout=1))

    def test_get_gateway_states(self):
        gateway = list(self.io_sim.get_pin_states().values())[0].gateway
        states = self.io.get_gateway_states(gateway)
        self.assertEqual(len(states), 4)
        for i in range(4):
            self.assertEqual(states[i].pin, list(self.io_sim.get_pin_states().values())[i].pin)
            self.assertEqual(states[i].value, list(self.io_sim.get_pin_states().values())[i].value)
            self.assertEqual(states[i].physical, list(self.io_sim.get_pin_states().values())[i].physical)

    def test_unknown_gateway(self):
        gateway = Gateway(gate="gate_does_not_exist", direction="in")
        self.assertFalse(self.io.is_gateway_valid(gateway=gateway))
        state = self.io.get_gateway_states(gateway=gateway)
        self.assertEqual(state[0].value, 0)
        self.assertEqual(state[0].gateway, Gateway(gate="", direction=""))
        self.assertEqual(state[0].pin, "")
        self.assertEqual(state[0].physical, 0)
        self.assertEqual(state[0].inverted, False)
        self.assertEqual(state[0].last_timestamp, datetime.fromtimestamp(0))
