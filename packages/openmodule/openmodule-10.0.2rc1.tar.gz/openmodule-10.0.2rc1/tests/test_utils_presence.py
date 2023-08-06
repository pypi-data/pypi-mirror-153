import time
from datetime import datetime
from functools import partial
from typing import Optional
from unittest import TestCase

import freezegun
import orjson

from openmodule.core import init_openmodule, shutdown_openmodule
from openmodule.dispatcher import MessageDispatcher
from openmodule.models.base import Direction, Gateway
from openmodule.models.presence import PresenceBaseMessage, PresenceRPCRequest, PresenceRPCResponse, PresenceBaseData, \
    PresenceMedia
from openmodule.models.vehicle import MakeModel, LPRMedium, PresenceAllIds, EnterDirection
from openmodule.rpc import RPCServer
from openmodule.utils.presence import PresenceListener
from openmodule_test.eventlistener import MockEvent
from openmodule_test.presence import PresenceSimulator
from openmodule_test.zeromq import ZMQTestMixin


class BasePresenceTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.dispatcher = MessageDispatcher()
        self.presence_sim = PresenceSimulator("gate_in", Direction.IN,
                                              lambda x: self.dispatcher.dispatch(b"presence", x))

        self.presence = PresenceListener(self.dispatcher)
        self.on_enter = MockEvent()
        self.on_forward = MockEvent()
        self.on_backward = MockEvent()
        self.on_change = MockEvent()
        self.on_leave = MockEvent()
        self.presence.on_enter.append(self.on_enter)
        self.presence.on_forward.append(self.on_forward)
        self.presence.on_backward.append(self.on_backward)
        self.presence.on_change.append(self.on_change)
        self.presence.on_leave.append(self.on_leave)


class PresenceTest(BasePresenceTest):
    def test_cannot_use_present_vehicle_without_gate(self):
        with self.assertRaises(AssertionError) as e:
            self.presence.present_vehicle.json()
        self.assertIn("please access the present vehicle per gate", str(e.exception))

        self.presence.gate = "test"
        val = self.presence.present_vehicle
        self.assertIsNone(val)

    def test_double_entry(self):
        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        MockEvent.reset_all_mocks()
        self.presence_sim.current_present = None
        with self.assertLogs() as cm:
            self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO2"))
            self.on_enter.wait_for_call()
            self.on_leave.wait_for_call()
        self.assertEqual("G ARIVO2", self.presence.present_vehicles["gate_in"].lpr.id)
        self.assertIn("A leave will be faked", str(cm))

    def test_faulty_exit(self):
        with self.assertLogs() as cm:
            self.presence_sim.current_present = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
            self.presence_sim.leave()
            time.sleep(1)
            self.assertEqual({}, self.presence.present_vehicles)
        self.assertIn("The leave will be ignored", str(cm))

        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        self.presence_sim.current_present = self.presence_sim.vehicle().lpr("A", "G ARIVO2")
        with self.assertLogs() as cm:
            self.presence_sim.leave()
            self.on_leave.wait_for_call()
            self.assertEqual({}, self.presence.present_vehicles)
        self.assertIn("We are fake-leaving the currently present vehicle", str(cm))

    def test_vehicle_id_change(self):
        vehicle_0 = self.presence_sim.vehicle()
        self.presence_sim.enter(vehicle_0)
        self.on_enter.wait_for_call()
        self.assertEqual(vehicle_0.vehicle_id, self.presence.present_vehicles["gate_in"].id)
        self.on_enter.reset_mock()

        vehicle_1 = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
        self.presence_sim.change_vehicle_and_id(vehicle_1)
        self.on_leave.wait_for_call()
        self.on_enter.wait_for_call()

        self.assertEqual(vehicle_1.vehicle_id, self.presence.present_vehicles["gate_in"].id)
        self.on_leave.reset_mock()

        self.presence_sim.leave()
        self.on_leave.wait_for_call()

        self.assertIsNone(self.presence.present_vehicles.get("gate_in"))

    def test_lpr_change(self):
        vehicle_0 = self.presence_sim.vehicle().lpr("A", "GARIVO1")
        self.presence_sim.enter(vehicle_0)
        self.on_enter.wait_for_call()
        self.assertEqual("GARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        vehicle_0.lpr("A", "GARIVO2")
        self.presence_sim.change(vehicle_0)
        self.on_change.wait_for_call()
        self.assertEqual("GARIVO2", self.presence.present_vehicles["gate_in"].lpr.id)

    def test_make_model_change(self):
        vehicle_0 = self.presence_sim.vehicle().lpr("A", "GARIVO1")
        self.presence_sim.enter(vehicle_0)
        self.on_enter.wait_for_call()
        self.assertEqual("GARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        vehicle_0.set_make_model(MakeModel(make="TESLA", make_confidence=0.7, model="UNKNOWN", model_confidence=-1.0))
        self.presence_sim.change(vehicle_0)
        self.on_change.wait_for_call()
        self.assertEqual("TESLA", self.presence.present_vehicles["gate_in"].make_model.make)

    def test_normal(self):
        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        self.presence_sim.leave()
        self.on_leave.wait_for_call()
        self.assertEqual({}, self.presence.present_vehicles)

    def test_other_calls(self):
        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1")

        self.presence_sim.forward(vehicle)
        self.on_forward.wait_for_call()

        self.presence_sim.backward(vehicle)
        self.on_backward.wait_for_call()

        self.presence_sim.enter(vehicle)
        self.on_enter.wait_for_call()

        vehicle_changed = vehicle.nfc("asdf")
        self.presence_sim.change(vehicle_changed)
        self.on_change.wait_for_call()
        self.on_change.reset_mock()

    def test_missed_enter_before_change(self):
        self.presence_sim.change_before_enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_enter.wait_for_call()
        self.assertEqual("G ARIVO1", self.presence.present_vehicles["gate_in"].lpr.id)

        self.presence_sim.leave()
        self.on_leave.wait_for_call()
        self.assertEqual({}, self.presence.present_vehicles)

    def test_enter_direction(self):
        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
        self.presence_sim.enter(vehicle)
        self.on_enter.wait_for_call()
        self.assertEqual(EnterDirection.unknown, self.presence.present_vehicles["gate_in"].enter_direction)

        vehicle.set_enter_direction(EnterDirection.forward)
        self.presence_sim.change(vehicle)
        self.on_change.wait_for_call()
        self.assertEqual(EnterDirection.forward, self.presence.present_vehicles["gate_in"].enter_direction)

        self.presence_sim.leave()
        self.on_leave.wait_for_call()

        self.on_enter.reset_mock()
        self.on_change.reset_mock()
        self.on_leave.reset_mock()

        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1").set_enter_direction(EnterDirection.backward)
        self.presence_sim.enter(vehicle)
        self.on_enter.wait_for_call()
        self.assertEqual(EnterDirection.backward, self.presence.present_vehicles["gate_in"].enter_direction)

        self.presence_sim.leave()
        self.on_leave.wait_for_call()
        self.assertEqual({}, self.presence.present_vehicles)

        self.on_enter.reset_mock()
        self.on_change.reset_mock()
        self.on_leave.reset_mock()

        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
        self.presence_sim.enter(vehicle)
        self.on_enter.wait_for_call()
        self.assertEqual(EnterDirection.unknown, self.presence.present_vehicles["gate_in"].enter_direction)

        # no change is sent when enter direction changes, so change can also happen on forward / backward / leave
        vehicle.set_enter_direction(EnterDirection.backward)
        self.presence_sim.leave()
        self.on_leave.wait_for_call()
        self.presence_sim.forward(vehicle)
        self.on_forward.wait_for_call()
        self.assertEqual(EnterDirection.backward, self.on_forward.call_args[0][0].enter_direction)


class PresenceTestUtilsTest(BasePresenceTest):
    def test_vehicle_id_change_is_enforced(self):
        vehicle = self.presence_sim.vehicle().lpr("A", "G ARIVO1")
        self.presence_sim.enter(vehicle)

        with self.assertRaises(AssertionError) as e:
            self.presence_sim.change_vehicle_and_id(vehicle)
        self.assertIn("vehicle id must change", str(e.exception))

        self.on_enter.reset_mock()
        self.presence_sim.change_vehicle_and_id(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))
        self.on_leave.wait_for_call()
        self.on_enter.wait_for_call()


class GateFilterTest(BasePresenceTest):
    def setUp(self) -> None:
        super().setUp()
        self.presence2 = PresenceListener(self.dispatcher, "gate_in")
        self.on_enter2 = MockEvent()
        self.presence2.on_enter.append(self.on_enter2)

    def tearDown(self):
        super().tearDown()

    def test_gate_filter(self):
        self.presence_sim.enter(self.presence_sim.vehicle().lpr("A", "G ARIVO1"))

        self.on_enter.wait_for_call()
        self.assertIn("gate_in", self.presence.present_vehicles.keys())
        self.presence.present_vehicles = {}
        self.on_enter2.wait_for_call()
        self.assertIn("gate_in", self.presence2.present_vehicles.keys())
        self.presence2.present_vehicles = {}

        MockEvent.reset_all_mocks()

        sim_out = PresenceSimulator("gate_out", Direction.OUT, lambda x: self.dispatcher.dispatch(b"presence", x))
        sim_out.enter(sim_out.vehicle().lpr("A", "G ARIVO2"))
        self.on_enter.wait_for_call()

        self.assertIn("gate_out", self.presence.present_vehicles.keys())
        with self.assertRaises(TimeoutError):
            self.on_enter2.wait_for_call()

        self.assertEqual({}, self.presence2.present_vehicles)


class PresenceSimulatorTest(TestCase):
    message: Optional[PresenceBaseMessage] = None

    def setUp(self) -> None:
        super().setUp()
        self.message = None

    def test_presence_alias_fields_serialization(self):
        sim = PresenceSimulator("gate1", Direction.IN, partial(setattr, self, "message"))
        sim.enter(sim.vehicle().qr("test"))
        sim.forward()
        message = orjson.loads(self.message.json_bytes())
        self.assertIn("leave-time", message)


class PresenceRPCTest(ZMQTestMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.core = init_openmodule(self.zmq_config(), context=self.zmq_context())
        self.wait_for_dispatcher(self.core.messages)
        self.presence_sim = PresenceSimulator("gate_in", Direction.IN, lambda x: self.zmq_client.send(b"presence", x))
        self.rpc_server = RPCServer(context=self.core.context)
        self.rpc_server.register_handler("tracking", "get-present", PresenceRPCRequest, PresenceRPCResponse,
                                         self.on_reply)
        self.rpc_server.run_as_thread()
        self.present = False

    def tearDown(self):
        self.rpc_server.shutdown()
        shutdown_openmodule()
        super().tearDown()

    def on_reply(self, request: PresenceRPCRequest, _) -> PresenceRPCResponse:
        """
        Emulates Trackings Presence RPC
        """
        if self.present:
            return PresenceRPCResponse(presents=[
                PresenceBaseData(vehicle_id=1, source="gate_in", present_area_name="gate_in",
                                 last_update=datetime.utcnow(), gateway=Gateway(gate="gate_in", direction="in"),
                                 medium=PresenceMedia(lpr=LPRMedium(id="T EST 1")), all_ids=PresenceAllIds())])
        else:
            return PresenceRPCResponse(presents=[])

    def test_presence_rpc_plate(self):
        self.present = True
        self.presence = PresenceListener(self.core.messages, gate="gate_in")
        self.presence.init_present_vehicles()
        self.assertNotEqual({}, self.presence.present_vehicles)

    def test_presence_rpc_no_plate(self):
        self.present = False
        self.presence = PresenceListener(self.core.messages, gate="gate_in")
        self.presence.init_present_vehicles()
        self.assertEqual({}, self.presence.present_vehicles)

    def test_presence_rpc_only_allowed_for_gates(self):
        self.presence = PresenceListener(self.core.messages)
        with self.assertRaises(AssertionError) as e:
            self.presence.init_present_vehicles()
        self.assertIn("if the gate is set", str(e.exception))

    def test_presence_rpc_timeout(self):
        self.rpc_server.shutdown()
        self.presence = PresenceListener(self.core.messages, gate="gate_in")
        self.core.rpc_client.default_timeout = 1
        self.presence.init_present_vehicles()


class MultiCameraTest(BasePresenceTest):
    def setUp(self) -> None:
        super().setUp()
        self.presence_sim2 = PresenceSimulator("gate_in", Direction.IN,
                                               lambda x: self.dispatcher.dispatch(b"presence", x),
                                               "gate_in-presence2")

    def test_empty_plates_interleaved(self):
        """
        Test enter1, enter2, leave1, forward1, leave2, forward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle()
        vehicle2 = self.presence_sim.vehicle()

        self.presence_sim.enter(vehicle1)
        self.presence_sim2.enter(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_forward.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_forward.call_args[0][0].id)

    def test_instant_plates_interleaved(self):
        """
        Test enter1, enter2, leave1, forward1, leave2, forward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        vehicle2 = self.presence_sim.vehicle().lpr("A", "T EST 2")

        self.presence_sim.enter(vehicle1)
        self.presence_sim2.enter(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_forward.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_forward.call_args[0][0].id)

    def test_interleaved_delayed_plates(self):
        """
        Test enter1 (no plate), enter2 (no plate), change1, change2, leave1, backward1, leave2, backward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle()
        vehicle2 = self.presence_sim.vehicle()

        self.presence_sim.enter(vehicle1)
        self.presence_sim2.enter(vehicle2)
        vehicle1.lpr("A", "T EST 1")
        self.presence_sim.change(vehicle1)
        vehicle2.lpr("A", "T EST 2")
        self.presence_sim2.change(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.backward(vehicle1)
        self.presence_sim2.leave()
        self.presence_sim2.backward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_change.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_backward.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_change.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_backward.call_args[0][0].id)

    def test_interleaved_second_has_first_plates(self):
        """
        Test enter1 (no plate), enter2 (no plate), change2, change1, leave2, forward2, leave1, forward1
        There should be an enter and a leave from 1 followed by enter+leave+forward from 2
        """
        vehicle1 = self.presence_sim.vehicle()
        vehicle2 = self.presence_sim.vehicle()

        self.presence_sim.enter(vehicle1)
        self.presence_sim2.enter(vehicle2)
        vehicle2.lpr("A", "T EST 2")
        self.presence_sim2.change(vehicle2)
        self.on_leave.wait_for_call(minimum_call_count=1)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.on_leave.reset_mock()
        vehicle1.lpr("A", "T EST 1")
        self.presence_sim.change(vehicle1)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(0, self.on_change.call_count)
        self.assertEqual(1, self.on_leave.call_count)  # one leave was already processed
        self.assertEqual(1, self.on_forward.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args_list[0][0][0].id)
        self.assertEqual(vehicle2.vehicle().id, self.on_enter.call_args_list[1][0][0].id)
        self.assertEqual(vehicle2.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle2.vehicle().id, self.on_forward.call_args[0][0].id)

    def test_first_changed_after_second_leave(self):
        """
        Test enter1 (no plate), enter2 (no plate), change2, change2, leave2, forward2, change1, leave1, forward1
        There should be an enter and a leave from 1 followed by enter+change+leave+forward from 2
        """
        vehicle1 = self.presence_sim.vehicle()
        vehicle2 = self.presence_sim.vehicle()

        self.presence_sim.enter(vehicle1)
        self.on_enter.wait_for_call(minimum_call_count=1)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args[0][0].id)
        self.on_enter.reset_mock()
        self.presence_sim2.enter(vehicle2)
        vehicle2.lpr("A", "T EST 2")
        self.presence_sim2.change(vehicle2)
        self.on_leave.wait_for_call(minimum_call_count=1)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.on_leave.reset_mock()
        vehicle2.lpr("A", "T EST 3")
        self.presence_sim2.change(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)
        vehicle1.lpr("A", "T EST 1")
        self.presence_sim.change(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_change.call_count)
        self.assertEqual(1, self.on_leave.call_count)  # one leave was already processed
        self.assertEqual(1, self.on_forward.call_count)
        self.assertEqual(vehicle2.vehicle().id, self.on_enter.call_args[0][0].id)
        self.assertEqual(vehicle2.vehicle().id, self.on_change.call_args[0][0].id)
        self.assertEqual(vehicle2.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle2.vehicle().id, self.on_forward.call_args[0][0].id)

    def test_interleaved_delayed_mediums(self):
        """
        Test enter1 (no plate), enter2 (no plate), change1, change2, leave1, backward1, leave2, backward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle()
        vehicle2 = self.presence_sim.vehicle()

        self.presence_sim.enter(vehicle1)
        self.presence_sim2.enter(vehicle2)
        vehicle1.qr("QR1")
        self.presence_sim.change(vehicle1)
        vehicle2.lpr("A", "T EST 2")
        self.presence_sim2.change(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.backward(vehicle1)
        self.presence_sim2.leave()
        self.presence_sim2.backward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_change.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_backward.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_change.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_backward.call_args[0][0].id)

    def test_interleaved_delayed_mediums(self):
        """
        Test enter1 (no plate), enter2 (no plate), change1, change2, leave1, backward1, leave2, backward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle()
        vehicle2 = self.presence_sim.vehicle()

        self.presence_sim.enter(vehicle1)
        self.presence_sim2.enter(vehicle2)
        vehicle1.qr("QR1")
        self.presence_sim.change(vehicle1)
        vehicle2.lpr("A", "T EST 2")
        self.presence_sim2.change(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.backward(vehicle1)
        self.presence_sim2.leave()
        self.presence_sim2.backward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_change.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_backward.call_count)
        self.assertEqual(vehicle1.vehicle().id, self.on_enter.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_change.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_leave.call_args[0][0].id)
        self.assertEqual(vehicle1.vehicle().id, self.on_backward.call_args[0][0].id)


class MultiCameraDeduplicationTest(BasePresenceTest):
    def setUp(self) -> None:
        super().setUp()
        self.presence_sim2 = PresenceSimulator("gate_in", Direction.IN,
                                               lambda x: self.dispatcher.dispatch(b"presence", x),
                                               "gate_in-presence2")

    def test_reenter_same_present_area(self):
        """
        Test enter1, leave1, forward1, enter1 (no plate), change1, leave1, forward1
        No event should be dropped
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim.vehicle()
        self.presence_sim.enter(vehicle2)
        vehicle2.lpr("A", "T EST 1")
        self.presence_sim.change(vehicle2)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle2)

        self.on_forward.wait_for_call(minimum_call_count=2)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(1, self.on_change.call_count)
        self.assertEqual(2, self.on_leave.call_count)
        self.assertEqual(2, self.on_forward.call_count)

    def test_duplicate_no_plate(self):
        """
        Test enter1, leave1, forward1, enter2 (no plate), leave2, forward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle()
        self.presence_sim2.enter(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_forward.call_count)

    def test_duplicate_same_plate(self):
        """
        Test enter1, leave1, forward1, enter2, leave2, forward2
        There should only be events from 1
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T ESTÖQ 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle().lpr("A", "T ESTO01")
        self.presence_sim2.enter(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.assertEqual(1, self.on_enter.call_count)
        self.assertEqual(1, self.on_leave.call_count)
        self.assertEqual(1, self.on_forward.call_count)

    def test_duplicate_different_plate(self):
        """
        Test enter1, leave1, forward1, enter2, leave2, forward2
        No events should be dropped because of different plates
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 2")
        self.presence_sim2.enter(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.on_forward.wait_for_call(minimum_call_count=2)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(2, self.on_leave.call_count)
        self.assertEqual(2, self.on_forward.call_count)

    def test_duplicate_change_to_different_plate(self):
        """
        Test enter1, leave1, forward1, enter2 (no plate), change2, leave2, forward2
        Enter2 should be dropped the rest should not be dropped because of different plates
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle()
        self.presence_sim2.enter(vehicle2)
        vehicle2.lpr("A", "T EST 2")
        self.presence_sim2.change(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.on_forward.wait_for_call(minimum_call_count=2)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(0, self.on_change.call_count)
        self.assertEqual(2, self.on_leave.call_count)
        self.assertEqual(2, self.on_forward.call_count)

    def test_duplicate_change_to_same_plate(self):
        """
        Test enter1, leave1, forward1, enter2 (different plate), change2 (same plate), leave2, forward2
        No event should be dropped as we need corresponding events for second enter, even if plate changed to the same
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 2")
        self.presence_sim2.enter(vehicle2)
        vehicle2.lpr("A", "T EST 1")
        self.presence_sim2.change(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.on_forward.wait_for_call(minimum_call_count=2)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(1, self.on_change.call_count)
        self.assertEqual(2, self.on_leave.call_count)
        self.assertEqual(2, self.on_forward.call_count)

    def test_duplicate_same_plate_with_additional(self):
        """
        Test enter1, leave1, forward1, enter1, leave1, forward1, enter2, leave2, forward2
        Events from 2 should be dropped
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 2")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 1")
        self.presence_sim2.enter(vehicle2)
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(2, self.on_leave.call_count)
        self.assertEqual(2, self.on_forward.call_count)

    def test_duplicate_afterwards_with_qr(self):
        """
        Test enter1, leave1, forward1, enter2, leave2, forward2
        Events from 2 should be dropped
        """
        vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
        self.presence_sim.enter(vehicle1)
        self.presence_sim.leave()
        self.presence_sim.forward(vehicle1)

        vehicle2 = self.presence_sim2.vehicle().qr("QR1")
        self.presence_sim2.enter(vehicle2)
        vehicle2.lpr("A", "T EST 1")
        self.presence_sim2.change(vehicle2)  # this is not possible for Tracking at the moment but should be no problem
        self.presence_sim2.leave()
        self.presence_sim2.forward(vehicle2)

        self.assertEqual(2, self.on_enter.call_count)
        self.assertEqual(2, self.on_leave.call_count)
        self.assertEqual(2, self.on_forward.call_count)

    def test_duplicate_after_timeout(self):
        """
        Test enter1, leave1, forward1, wait, enter2, leave2, forward2
        No events should be dropped as time between is long enough
        """
        with freezegun.freeze_time("2020-01-01 00:00"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)

            self.on_forward.wait_for_call(minimum_call_count=1)
            self.assertEqual(1, self.on_enter.call_count)
            self.assertEqual(1, self.on_leave.call_count)
            self.assertEqual(1, self.on_forward.call_count)

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        with freezegun.freeze_time("2020-01-01 00:01"):
            vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 1")
            self.presence_sim2.enter(vehicle2)
            self.presence_sim2.leave()
            self.presence_sim2.forward(vehicle2)

            self.on_forward.wait_for_call(minimum_call_count=1)
            self.assertEqual(1, self.on_enter.call_count)
            self.assertEqual(1, self.on_leave.call_count)
            self.assertEqual(1, self.on_forward.call_count)

    def test_duplicate_timeout_before_leave(self):
        """
        Test enter1, leave1, forward1, enter2, wait, leave2, forward2
        Events of 2 should be dropped as enter2 was within timeout and all events of the vehicle should be dropped
        """
        with freezegun.freeze_time("2020-01-01 00:00"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 1")
            self.presence_sim2.enter(vehicle2)

            self.assertEqual(1, self.on_enter.call_count)
            self.assertEqual(1, self.on_leave.call_count)
            self.assertEqual(1, self.on_forward.call_count)

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        with freezegun.freeze_time("2020-01-01 00:01"):
            self.presence_sim2.leave()
            self.presence_sim2.forward(vehicle2)

            self.assertEqual(0, self.on_enter.call_count)
            self.assertEqual(0, self.on_leave.call_count)
            self.assertEqual(0, self.on_forward.call_count)

    def test_duplicate_change_after_timeout(self):
        """
        Test enter1, leave1, forward1, enter2, wait, change2, leave2, forward2
        Enter2 should be dropped however the is a change2 after the timeout so change2, leave2, forward2 are not dropped
        """
        with freezegun.freeze_time("2020-01-01 00:00"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 1")
            self.presence_sim2.enter(vehicle2)

            self.assertEqual(1, self.on_enter.call_count)
            self.assertEqual(1, self.on_leave.call_count)
            self.assertEqual(1, self.on_forward.call_count)

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        with freezegun.freeze_time("2020-01-01 00:01"):
            vehicle2.lpr("A", "T EST 2")
            self.presence_sim2.change(vehicle2)
            self.presence_sim2.leave()
            self.presence_sim2.forward(vehicle2)

            self.on_forward.wait_for_call(minimum_call_count=1)

            self.assertEqual(1, self.on_enter.call_count)
            self.assertEqual(0, self.on_change.call_count)
            self.assertEqual(1, self.on_leave.call_count)
            self.assertEqual(1, self.on_forward.call_count)

    def test_last_vehicle_data_cleanup(self):
        """
        Test if cleanup of last_vehicle_data works
        """
        with freezegun.freeze_time("2020-01-01 00:00"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            self.on_forward.wait_for_call(minimum_call_count=1)

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        with freezegun.freeze_time("2020-01-01 00:59"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 2")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            self.on_forward.wait_for_call(minimum_call_count=1)

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        self.assertEqual(2, len(self.presence.last_vehicle_data[self.presence_sim.gateway.gate]))

        with freezegun.freeze_time("2020-01-01 01:01"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 3")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            self.on_forward.wait_for_call(minimum_call_count=1)

        self.assertEqual(2, len(self.presence.last_vehicle_data[self.presence_sim.gateway.gate]))

    def test_drop_list_cleanup(self):
        """
        Test if cleanup of drop_list works
        """
        with freezegun.freeze_time("2020-01-01 00:00"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 1")
            self.presence_sim.enter(vehicle1)
        with freezegun.freeze_time("2020-01-01 00:00:01"):
            vehicle2 = self.presence_sim2.vehicle().lpr("A", "T EST 1")
            self.presence_sim2.enter(vehicle2)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            self.on_forward.wait_for_call(minimum_call_count=1)

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        with freezegun.freeze_time("2020-01-01 00:59"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 2")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            self.on_forward.wait_for_call(minimum_call_count=1)
            # no cleanup of vehicle without leave yet
            self.assertEqual(1, len(self.presence.drop_list))

        self.on_enter.reset_mock()
        self.on_leave.reset_mock()
        self.on_forward.reset_mock()

        with freezegun.freeze_time("2020-01-01 01:01"):
            vehicle1 = self.presence_sim.vehicle().lpr("A", "T EST 2")
            self.presence_sim.enter(vehicle1)
            self.presence_sim.leave()
            self.presence_sim.forward(vehicle1)
            self.on_forward.wait_for_call(minimum_call_count=1)
            # now cleanup of vehicle without leave should be done
            self.assertEqual(0, len(self.presence.drop_list))
