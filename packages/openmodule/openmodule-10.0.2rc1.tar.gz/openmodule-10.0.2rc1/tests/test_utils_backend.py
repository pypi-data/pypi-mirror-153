import json
from datetime import datetime
from textwrap import dedent
from unittest import TestCase

from openmodule.models.backend import CountMessage, AccessRequest, Access, AccessCategory, check_recurrence, \
    SessionStartMessage, SessionFinishMessage
from openmodule.models.base import Gateway
from openmodule.rpc.server import RPCServer
from openmodule.utils.backend import Backend
from openmodule_test.backend import TestBackend, BackendTestMixin
from openmodule_test.eventlistener import MockEvent
from openmodule_test.rpc import RPCServerTestMixin


class ModelTest(TestCase):
    def test_count_message(self):
        messages = dedent("""  [{  "real": true,
                    "category": "permanent-employee",
                    "medium_type": "lpr",
                    "name": "count-test",
                    "zone": "zone1",
                    "timestamp": 1536154434.152993,
                    "count": 1,
                    "gateway": {
                        "gate": "gate1",
                        "direction": "in"
                    },
                    "user": "userprefix-asdf_GASDF1\u00dcSER",
                    "access_data": {
                        "on_presence_loop": true,
                        "has_presence_loop": false,
                        "decision": "accepted"
                    },
                    "type": "count",
                    "id": "GASD\u00c41",
                    "transaction_id": "dc4e4af3-5ff4-4258-a310-089701ef37e8" }, 
                    { "real": false,
                    "category": "permanent-employee",
                    "medium_type": "lpr",
                    "name": "count-test",
                    "zone": "zone1",
                    "timestamp": 1536154434.19146,
                    "count": 0,
                    "gateway": {
                        "gate": "automatically_deleted",
                        "direction": "out"
                    },
                    "user": "userprefix-asdf_GASDF1\u00dcSER",
                    "type": "count",
                    "id": "GASD\u00c41",
                    "transaction_id": "dc4e4af3-5ff4-4258-a310-089701ef37e8"},
                     {  "real": true,
                    "category": "permanent-employee",
                    "medium_type": "lpr",
                    "name": "count-test",
                    "zone": "zone1",
                    "previous_transaction_id": ["dc4e4af3-5ff4-4258-a310-089701ef37e8"],
                    "timestamp": 1536154434.192287,
                    "count": 1,
                    "gateway": {
                        "gate": "gate1",
                        "direction": "in"
                    },
                    "user": "userprefix-asdf_GASDF1\u00dcSER",
                    "error": "double_entry",
                    "access_data": {
                        "on_presence_loop": true,
                        "has_presence_loop": false,
                        "decision": "accepted"
                    },
                    "type": "count",
                    "id": "GASD\u00c41",
                    "transaction_id": "0337597c-f125-44e0-b38f-a6537e7d38d1" }]
                """).strip()
        messages = json.loads(messages)
        for message in messages:
            model = CountMessage(**message)
            self.assertTrue(bool(model.transaction_id))

    def test_access_recurrence(self):
        kwargs = dict(user="asdf", category="permanent-employee", start=3,
                      recurrence="DTSTART:20180702T123000\nFREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR")
        with self.assertRaises(ValueError) as e:
            Access(**kwargs)
        self.assertIn("set a duration", str(e.exception))

        kwargs["duration"] = 0
        with self.assertRaises(ValueError) as e:
            Access(**kwargs)
        self.assertIn("set a duration", str(e.exception))

        kwargs["duration"] = 1000
        access = Access(**kwargs)
        self.assertEqual(1000, access.duration)

        kwargs["recurrence"] = "asdf"
        with self.assertRaises(ValueError) as e:
            Access(**kwargs)
        self.assertIn("recurrence is not valid", str(e.exception))

    def test_check_recurrence_validator(self):
        cls = None

        # due to too much legacy data which contains "", we allow empty string, but it is converted to none internally
        check_recurrence(cls, "", {})
        access = Access(start=0, user="test", category=AccessCategory.permanent_digimon, recurrence="")
        self.assertIsNone(access.recurrence)

        with self.assertRaises(ValueError) as e:
            check_recurrence(cls, "DTSTART\n", {"duration": "100"})
        self.assertIn("recurrence is not valid", str(e.exception))

        with self.assertRaises(ValueError) as e:
            check_recurrence(cls, "\nRRULE:FREQ=WEEKLY;INTERVAL=1;WKST=MO", {"duration": 3600})
        self.assertIn("DTSTART", str(e.exception))

        with self.assertRaises(ValueError) as e:
            check_recurrence(cls, "DTSTART:20210304T161900Z;RRULE:FREQ=WEEKLY;INTERVAL=1;WKST=MO", {"duration": 3600})
        self.assertIn("separated by a newline", str(e.exception))

        check_recurrence(cls, None, {})
        check_recurrence(cls, "DTSTART:20210304T161900Z\nRRULE:FREQ=WEEKLY;INTERVAL=1;WKST=MO", {"duration": 3600})

    def test_category(self):
        with self.assertRaises(Exception) as e:
            AccessCategory("test_exception")
        self.assertIn("is not a valid accesscategory", str(e.exception).lower())

        with self.assertRaises(Exception) as e:
            Access(user="asdf", category="permanent_employee", start=3,
                   recurrence="DTSTART:20180702T123000\nFREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR")
        self.assertIn("not a valid enumeration", str(e.exception))


class NotImplementedTestCase(BackendTestMixin, TestCase):
    backend_class = Backend

    # noinspection PyTypeChecker
    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.backend.check_in(None)
        with self.assertRaises(NotImplementedError):
            self.backend.check_out(None)
        with self.assertRaises(NotImplementedError):
            self.backend.check_access(None)


class FunctionTest(BackendTestMixin, TestCase):
    backend_class = TestBackend

    def test_check_in(self):
        transaction_id = self.check_in()
        message = self.messages_by_transaction.get(transaction_id)
        self.assertEqual(None, message.error)

        transaction_id = self.check_in_double_entry(transaction_id)
        message = self.messages_by_transaction.get(transaction_id)
        self.assertEqual("double_entry", message.error)
        self.assertNotEqual(None, message.previous_transaction_id)

        with self.assertRaises(Exception) as e:
            self.check_in(gate="error")
        self.assertIn("test_exception", str(e.exception))

    def check_in_out(self):
        transaction_id = self.check_in()
        self.assertNotEqual(None, self.messages_by_transaction.get(transaction_id))

        self.check_out(transaction_id)
        self.assertEqual(None, self.messages_by_transaction.get(transaction_id))

    def test_check_out(self):
        with self.assertRaises(Exception) as e:
            self.check_out("asdf")
        self.assertIn("asdf", str(e.exception))

        transaction_id = self.check_in(send=False)
        self.messages_by_transaction[transaction_id].gateway.gate = "error"
        with self.assertRaises(Exception) as e:
            self.check_out(transaction_id)
        self.assertIn("test_exception", str(e.exception))

        transaction_id = self.check_in(send=False)
        message = self.check_out(transaction_id)
        self.assertEqual(None, self.messages_by_transaction.get(transaction_id))
        self.assertEqual(None, message.error)

        # category_changed
        transaction_id = self.check_in(send=False)
        message = self.check_out_category_changed(transaction_id)
        self.assertEqual(None, self.messages_by_transaction.get(transaction_id))
        self.assertEqual("category_changed", message.error)

        transaction_id = self.check_in(send=False)
        with self.assertRaises(Exception) as e:
            self.check_out_category_changed(transaction_id, category="permanent-employee")
        self.assertIn("category needs to change", str(e.exception))

        # medium_changed
        transaction_id = self.check_in(send=False)
        message = self.check_out_medium_changed(transaction_id)
        self.assertEqual(None, self.messages_by_transaction.get(transaction_id))
        self.assertEqual("medium_type_changed", message.error)
        self.assertNotEqual(None, message.previous_medium_id)
        self.assertNotEqual(None, message.previous_medium_type)

        transaction_id = self.check_in(send=False)
        with self.assertRaises(Exception) as e:
            self.check_out_medium_changed(transaction_id, medium="lpr")
        self.assertIn("medium needs to change", str(e.exception))

        # medium_id_changed
        transaction_id = self.check_in(send=False)
        message = self.check_out_medium_id_changed(transaction_id)
        self.assertEqual(None, self.messages_by_transaction.get(transaction_id))
        self.assertEqual("medium_id_changed", message.error)
        self.assertNotEqual(None, message.previous_medium_id)

        transaction_id = self.check_in(send=False)
        medium_id = self.messages_by_transaction[transaction_id].medium_id
        with self.assertRaises(Exception) as e:
            self.check_out_medium_id_changed(transaction_id, medium_id=medium_id)
        self.assertIn("medium_id needs to change", str(e.exception))

        # user_changed
        transaction_id = self.check_in(send=False)
        message = self.check_out_user_changed(transaction_id)
        self.assertEqual(None, self.messages_by_transaction.get(transaction_id))
        self.assertEqual("user_changed", message.error)
        self.assertNotEqual(None, message.previous_user)

        transaction_id = self.check_in(send=False)
        with self.assertRaises(Exception) as e:
            self.check_out_user_changed(transaction_id, user="api-backend_user")
        self.assertIn("user needs to change", str(e.exception))

    def test_access(self):
        result = self.check_auth(medium_id="GARIVO1", medium_type="lpr")
        self.assertEqual(True, result.success)
        self.assertNotEqual([], result.medium.accesses)

        result = self.check_auth(medium_id="GARIVO1", medium_type="lpr", gateway=Gateway(gate="empty", direction="in"))
        self.assertEqual(True, result.success)
        self.assertEqual([], result.medium.accesses)

        result = self.check_auth(medium_id="GARIVO1", medium_type="lpr", gateway=Gateway(gate="error", gateway="in"))
        self.assertEqual(False, result.success)


class RpcTest(BackendTestMixin, RPCServerTestMixin, TestCase):
    rpc_channels = ["backend"]
    topics = [b"backend", b"count", b"healthz"]
    backend_class = TestBackend

    def setUp(self):
        super().setUp()
        self.server = RPCServer(context=self.zmq_context())
        self.server.run_as_thread()
        self.backend.register_rpcs(self.server)
        self.wait_for_rpc_server(self.server)

    def tearDown(self):
        self.server.shutdown()
        super().tearDown()

    def test_access_rpc(self):
        # only test if rpc is passed on to function, function is tested in previous TestCase
        gateway = Gateway(gate="gate", direction="in")
        request = AccessRequest(gateway=gateway, name=self.core.config.NAME, medium_type="lpr", id="medium_id")
        response = self.rpc("backend", "auth", request=request.dict())
        self.assertRPCSuccess(response)
        self.assertIn(request.medium_id, self.backend.accessed)

    def send_count_message(self, gate="gate", direction="in"):
        transaction_id = self.create_count_message(direction=direction, gate=gate)
        self.zmq_client.send("count", **self.messages_by_transaction[transaction_id].dict())

    def send_session_start_message(self, gate="gate1", medium_id="GARIVO1", medium_type="lpr", zone_id="zone_1",
                                   user_id="user-1", timestamp=None, session_id="session-1"):
        entry_data = dict(used_medium=dict(id=medium_id, type=medium_type), gate=gate)

        message = SessionStartMessage(zone_id=zone_id, user_id=user_id, id=session_id, cost_table={}, serviceable=True,
                                       entry_time=timestamp or datetime.utcnow(), entry_data=entry_data)
        self.core.publish(message, b"session")

    def send_session_finish_message(self, gate="gate2", medium_id="GARIVO1", medium_type="lpr", zone_id="zone_1",
                                    user_id="user-1", timestamp=None, session_id="session-1"):
        exit_data = dict(used_medium=dict(id=medium_id, type=medium_type), gate=gate)
        message = SessionFinishMessage(zone_id=zone_id, user_id=user_id, id=session_id, cost_table={}, serviceable=True,
                                       exit_time=timestamp or datetime.utcnow(), exit_data=exit_data, entry_data={},
                                       entry_time=datetime.utcnow())

        self.core.publish(message, b"session")

    def test_registration(self):
        # auto register on start
        message = self.zmq_client.wait_for_message_on_topic(topic=b"backend", timeout=5)
        self.assertEqual("register", message["type"])

        self.zmq_client.send("backend", type="register_request")
        message = self.zmq_client.wait_for_message_on_topic(topic=b"backend", timeout=5)
        self.assertEqual("register_request", message["type"])

        message = self.zmq_client.wait_for_message_on_topic(topic=b"backend", timeout=5)
        self.assertEqual("register", message["type"])

    def test_check_in(self):
        self.send_count_message()
        self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)

        MockEvent.reset_all_mocks()
        with self.assertLogs() as cm:
            self.send_count_message(gate="error")
            self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)
        self.assertIn("error in check_in", cm.output[0])

    def test_check_out(self):
        self.send_count_message()
        self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)

        MockEvent.reset_all_mocks()
        with self.assertLogs() as cm:
            self.send_count_message(gate="error", direction="out")
            self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)
        self.assertIn("error in check_out", cm.output[0])

        MockEvent.reset_all_mocks()
        self.send_count_message(direction="out")
        self.backend.wait_for_message_process()
        self.assertEqual(0, self.backend.checked_in)

    def test_session_check_in(self):
        self.send_session_start_message()
        self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)

        MockEvent.reset_all_mocks()
        with self.assertLogs() as cm:
            self.send_session_start_message(gate="error")
            self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)
        self.assertIn("Error in session check in", cm.output[0])

    def test_session_check_out(self):
        self.send_session_finish_message()
        self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)

        MockEvent.reset_all_mocks()
        with self.assertLogs() as cm:
            self.send_session_finish_message(gate="error")
            self.backend.wait_for_message_process()
        self.assertEqual(1, self.backend.checked_in)
        self.assertIn("Error in session check out", cm.output[0])

    def test_datetime_is_converted_to_unix_timestamp(self):
        gateway = Gateway(gate="entry", direction="in")
        request = AccessRequest(gateway=gateway, name=self.core.config.NAME, medium_type="lpr", id="GTEST1")
        response = self.rpc("backend", "auth", request=request.dict())
        medium = response["response"]["medium"]
        self.assertTrue(isinstance(medium["accesses"][0]["start"], (int, float)))
        self.assertTrue(isinstance(medium["accesses"][0]["end"], (int, float)))
