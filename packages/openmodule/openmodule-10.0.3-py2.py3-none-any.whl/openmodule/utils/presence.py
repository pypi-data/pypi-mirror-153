import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple, Set, List

from openmodule.core import core
from openmodule.dispatcher import EventListener, MessageDispatcher
from openmodule.models.base import Gateway
from openmodule.models.presence import PresenceBaseMessage, PresenceBackwardMessage, PresenceForwardMessage, \
    PresenceChangeMessage, PresenceLeaveMessage, PresenceEnterMessage, PresenceRPCRequest, PresenceRPCResponse
from openmodule.models.vehicle import Vehicle
from openmodule.utils.charset import CharsetConverter, legacy_lpr_charset


def vehicle_from_presence_message(message: PresenceBaseMessage):
    return Vehicle(
        id=message.vehicle_id,
        lpr=message.medium.lpr,
        qr=message.medium.qr,
        nfc=message.medium.nfc,
        pin=message.medium.pin,
        make_model=message.make_model,
        all_ids=message.all_ids,
        enter_direction=message.enter_direction
    )


class VehicleDeduplicationData:
    lp_converter = CharsetConverter(legacy_lpr_charset)

    def __init__(self, vehicle: Vehicle, present_area_name: str, timeout: datetime):
        self.plate = VehicleDeduplicationData.lp_converter.clean(vehicle.lpr.id or "")
        self.present_area_name = present_area_name
        self.timeout = timeout
        self.drop_list = set()  # store here which vehicles should be dropped even after timeout
        self.dont_drop_list = set()  # store here which vehicles already caused message and thus should not be dropped

    def update_drop_list(self, message: PresenceBaseMessage, vehicle: Vehicle):
        not_in_drop_list = vehicle.id not in self.dont_drop_list
        within_timeout = datetime.utcnow() < self.timeout
        vehicle_has_no_media_or_has_same_plate = \
            not vehicle.has_media() or (vehicle.lpr and self.plate == self.lp_converter.clean(vehicle.lpr.id or ""))
        from_different_present_area = message.present_area_name != self.present_area_name
        drop = not_in_drop_list and within_timeout and self.plate and vehicle_has_no_media_or_has_same_plate and \
               from_different_present_area
        if drop:
            self.drop_list.add(vehicle.id)
        elif not vehicle_has_no_media_or_has_same_plate:
            self.dont_drop_list.add(vehicle.id)
            # only relevant on change as vehicle cannot already be on drop list on enter
            # and we should not undrop on leave/forward/backward
            if message.type == "change":
                self.drop_list.discard(vehicle.id)

    def should_deduplicate(self, vehicle: Vehicle):
        return vehicle.id in self.drop_list

    def should_cleanup(self):
        return self.timeout + timedelta(hours=1) < datetime.utcnow()


class PresenceListener:
    on_forward: EventListener[Tuple[Vehicle, Gateway]]
    on_backward: EventListener[Tuple[Vehicle, Gateway]]
    on_enter: EventListener[Tuple[Vehicle, Gateway]]
    on_leave: EventListener[Tuple[Vehicle, Gateway]]
    on_change: EventListener[Tuple[Vehicle, Gateway]]

    present_vehicles: Dict[str, Vehicle]
    drop_list: Set[int]  # can be shared over all gates (if there are multiple gates) as vehicle id is unique
    area_name_of_present: Dict[str, str]
    # List because there can be a new one before we are allowed to remove the old one
    last_vehicle_data: Dict[str, List[VehicleDeduplicationData]]

    @property
    def present_vehicle(self) -> Optional[Vehicle]:
        assert self.gate is not None, (
            "`.present_vehicle` may only be used when listening for a specific gate, this presence listener"
            "listens to all gates, please access the present vehicle per gate via `.present_vehicles[gate]`"
        )
        return self.present_vehicles.get(self.gate)

    def __init__(self, dispatcher: MessageDispatcher, gate: Optional[str] = None,
                 deduplication_timeout: timedelta = timedelta(seconds=10)):
        assert not dispatcher.is_multi_threaded, (
            "you cannot use a multithreaded message dispatcher for the presence listener. It is highly reliant "
            "on receiving messages in the correct order!"
        )
        self.log = logging.getLogger(self.__class__.__name__ + (" " + gate if gate else ""))
        self.on_forward = EventListener(log=self.log)
        self.on_backward = EventListener(log=self.log)
        self.on_enter = EventListener(log=self.log)
        self.on_change = EventListener(log=self.log)
        self.on_leave = EventListener(log=self.log)
        self.present_vehicles = dict()
        self.drop_list = set()
        self.area_name_of_present = dict()
        self.last_vehicle_data = dict()
        self.deduplication_timeout = deduplication_timeout
        self.gate = gate

        dispatcher.register_handler(b"presence", PresenceBackwardMessage, self._on_backward)
        dispatcher.register_handler(b"presence", PresenceForwardMessage, self._on_forward)
        dispatcher.register_handler(b"presence", PresenceChangeMessage, self._on_change)
        dispatcher.register_handler(b"presence", PresenceLeaveMessage, self._on_leave)
        dispatcher.register_handler(b"presence", PresenceEnterMessage, self._on_enter)

    def init_present_vehicles(self):
        assert self.gate, "init present vehicles is only possible if the gate is set, otherwise we do not know" \
                          "how many results to expect"
        try:
            result = core().rpc_client.rpc(b"tracking", "get-present", PresenceRPCRequest(gate=self.gate))
            if result.status == "ok" and result.response:
                response = PresenceRPCResponse(**result.response)
                if response.presents:
                    self._on_enter(response.presents[0])
        except TimeoutError:
            self.log.error(f"get-present RPC timeout", extra={"gate": self.gate})

    def _gate_matches(self, message: PresenceBaseMessage):
        return (self.gate is None) or (message.gateway.gate == self.gate)

    def _drop_check(self, message: PresenceBaseMessage, vehicle: Vehicle):
        gate = message.gateway.gate
        # execute this on every presence message
        for x in self.last_vehicle_data.get(gate, []):
            x.update_drop_list(message, vehicle)
        present_vehicle = self.present_vehicles.get(gate)

        # only don't drop when in drop list if there is an empty vehicle present and new vehicle has medium
        # (no present means old present was completely processed)
        # also no present_area_name check as vehicle cannot be on drop list if its from the same present area
        if vehicle.id in self.drop_list and \
                (present_vehicle is None or present_vehicle.has_media() or not vehicle.has_media()):
            self.drop_list.add(vehicle.id)
            return True
        elif present_vehicle:
            # some present area -> no drop, use old behavior (simulate leave for enter messages, otherwise just replace)
            if self.area_name_of_present.get(gate, "") == message.present_area_name:
                return False
            # new vehicle is better, simulate leave for old vehicle and remove new vehicle from drop list and add old
            elif not present_vehicle.has_media() and vehicle.has_media():
                self.log.warning("Got better vehicle from another present area. A leave will be faked for the old "
                                 "vehicle to get a consistent setup for the new vehicle.",
                                 extra={"present_vehicle": str(present_vehicle),
                                        "new_vehicle": str(vehicle)})
                self.drop_list.discard(vehicle.id)  # discard because vehicle might be in drop list
                self.drop_list.add(present_vehicle.id)
                self.present_vehicles.pop(gate, None)
                self.on_leave(present_vehicle, message.gateway)
                return False
            # different present area and new vehicle is not better -> drop
            else:
                self.drop_list.add(vehicle.id)
                return True
        # here we handle case that same vehicle is first seen by camera 1 and after leave seen by camera 2
        elif any([x.should_deduplicate(vehicle) for x in self.last_vehicle_data.get(gate, [])]):
            return True
        else:
            return False

    def _cleanup_drop_list(self):
        # this assumes vehicle id is UTC timestamp in nanoseconds (which is the case unless someone changes Tracking)
        self.drop_list = {x for x in self.drop_list if x / 1e9 > time.time() - 3600}

    def _on_backward(self, message: PresenceBackwardMessage):
        """
        This handler forwards presence backward  messages to the registered calls in the presence listener
        """

        if not self._gate_matches(message):
            return
        vehicle = vehicle_from_presence_message(message)
        drop_message = self._drop_check(message, vehicle)
        self.drop_list.discard(vehicle.id)
        if drop_message:
            return

        if self.present_vehicles.get(message.gateway.gate):
            self.log.error("Got backward without a leave. We generate a leave ourself.")
            self._on_leave(PresenceLeaveMessage(**message.dict()))

        self.log.debug("presence backward: %s", vehicle)
        self.on_backward(vehicle, message.gateway)

    def _on_forward(self, message: PresenceForwardMessage):
        """
        This handler forwards presence forward messages to the registered calls in the presence listener
        """
        if not self._gate_matches(message):
            return
        vehicle = vehicle_from_presence_message(message)
        drop_message = self._drop_check(message, vehicle)
        self.drop_list.discard(vehicle.id)
        if drop_message:
            return

        if self.present_vehicles.get(message.gateway.gate):
            self.log.error("Got forward without a leave. We generate a leave ourself.")
            self._on_leave(PresenceLeaveMessage(**message.dict()))

        self.log.debug("presence forward: %s", vehicle)
        self.on_forward(vehicle, message.gateway)

    def _on_leave(self, message: PresenceLeaveMessage):
        """
        This handler forwards presence leave messages to the registered calls in the presence listener
        and clears the present vehicle
        """

        if not self._gate_matches(message):
            return
        leaving_vehicle = vehicle_from_presence_message(message)
        if self._drop_check(message, leaving_vehicle):
            return

        self.log.debug("presence leave: %s", leaving_vehicle)
        present_vehicle = self.present_vehicles.get(message.gateway.gate)
        if present_vehicle:
            if present_vehicle.id != leaving_vehicle.id:
                self.log.error("A vehicle left with a different vehicle id than the present one. Tracking is "
                               "inconsistent. We are fake-leaving the currently present vehicle, to ensure consistent "
                               "states.", extra={"present_vehicle": str(present_vehicle),
                                                 "leaving_vehicle": str(leaving_vehicle)})
            self.present_vehicles.pop(message.gateway.gate, None)
            self.area_name_of_present.pop(message.gateway.gate, None)
            self.on_leave(leaving_vehicle, message.gateway)

            # cleanup last_vehicle_data and drop list
            self.last_vehicle_data[message.gateway.gate] = \
                [x for x in self.last_vehicle_data.get(message.gateway.gate, []) if not x.should_cleanup()]
            self._cleanup_drop_list()

            if leaving_vehicle.lpr:
                self.last_vehicle_data[message.gateway.gate].append(
                    VehicleDeduplicationData(leaving_vehicle, message.present_area_name,
                                             datetime.utcnow() + self.deduplication_timeout))
        else:
            self.log.error("A vehicle left while non was previously present. Tracking is inconsistent. "
                           "The leave will be ignored, to ensure consistent states.",
                           extra={"leaving_vehicle": str(leaving_vehicle)})

    def _on_enter(self, message: PresenceEnterMessage):
        """
        This handler forwards presence enter messages to the registered calls in the presence listener
        and sets the present vehicle
        """

        if not self._gate_matches(message):
            return
        new_vehicle = vehicle_from_presence_message(message)
        if self._drop_check(message, new_vehicle):
            return

        self.log.debug("presence enter: %s", new_vehicle)
        present_vehicle = self.present_vehicles.get(message.gateway.gate)
        if present_vehicle:
            self.log.error("A new vehicle entered while one was still present. Tracking is inconsistent. "
                           "A leave will be faked, to ensure consistent states.",
                           extra={"present_vehicle": str(present_vehicle),
                                  "new_vehicle": str(new_vehicle)})
            self.on_leave(present_vehicle, message.gateway)

        self.present_vehicles[message.gateway.gate] = new_vehicle
        self.area_name_of_present[message.gateway.gate] = message.present_area_name
        self.on_enter(new_vehicle, message.gateway)

    def _on_change(self, message: PresenceChangeMessage):
        """
        This handler forwards presence change messages to the registered calls in the presence listener
        and changes the present vehicle
        """

        if not self._gate_matches(message):
            return
        vehicle = vehicle_from_presence_message(message)
        if self._drop_check(message, vehicle):
            return

        change_with_vehicle_present = message.gateway.gate in self.present_vehicles
        if change_with_vehicle_present and self.present_vehicles[message.gateway.gate].id != vehicle.id:
            self.log.debug("vehicle_id changed in presence change: %s. "
                           "Faking leave and triggering presence enter!", vehicle)
            self.on_leave(self.present_vehicles[message.gateway.gate], message.gateway)
            change_with_vehicle_present = False

        self.present_vehicles[message.gateway.gate] = vehicle
        self.area_name_of_present[message.gateway.gate] = message.present_area_name
        if change_with_vehicle_present:
            self.log.debug("presence change: %s", vehicle)
            self.on_change(vehicle, message.gateway)
        else:
            self.log.warning("presence enter triggered by change: %s", vehicle)
            self.on_enter(vehicle, message.gateway)
