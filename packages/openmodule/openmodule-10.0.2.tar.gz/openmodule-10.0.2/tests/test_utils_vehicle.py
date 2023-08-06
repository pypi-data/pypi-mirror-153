from unittest import TestCase

import orjson
from pydantic import ValidationError

from openmodule.models.presence import PresenceForwardMessage
from openmodule.models.vehicle import Vehicle


class VehicleTestCase(TestCase):
    def test_vehicle_str(self):
        # just checks that the relevant info is
        vehicle = Vehicle(id=1613386532124866889,
                          qr={"id": "someverylongqrcodeitisreallylongohyeah", "type": "qr"},
                          lpr={"id": "test", "type": "lpr", "country": {"code": "D"}},
                          all_ids={"lpr": [{"id": "test", "type": "lpr", "country": {"code": "D"}}],
                                   "qr": [{"id": "someverylongqrcodeitisreallylongohyeah", "type": "qr"}]})

        vehicle_str = str(vehicle)

        self.assertIn("id:4866889", vehicle_str)  # only the last 7 digits are printed because they are random enough
        self.assertIn("somevery", vehicle_str)
        self.assertIn("...", vehicle_str)  # long medium id's are truncated
        self.assertIn("test", vehicle_str)

        # another check with make_model
        vehicle = Vehicle(id=1613386532124866889,
                          qr={"id": "someverylongqrcodeitisreallylongohyeah", "type": "qr"},
                          lpr={"id": "test", "type": "lpr", "country": {"code": "D"}},
                          all_ids={"lpr": [{"id": "test", "type": "lpr", "country": {"code": "D"}}],
                                   "qr": [{"id": "someverylongqrcodeitisreallylongohyeah", "type": "qr"}]},
                          make_model={"make": "TESLA", "make_confidence": 0.7,
                                      "model": "UNKNOWN", "model_confidence": -1.0})

        vehicle_str = str(vehicle)

        self.assertIn("id:4866889", vehicle_str)  # only the last 7 digits are printed because they are random enough
        self.assertIn("somevery", vehicle_str)
        self.assertIn("...", vehicle_str)  # long medium id's are truncated
        self.assertIn("test", vehicle_str)
        self.assertIn("TESLA", vehicle_str)

        # test parse
        try:
            message = """{"all_ids":{"lpr":[{"alternatives":[{"confidence":3.4705942967674654e-18,"plate":"ZH 614198"},
            {"confidence":1.419478673564383e-18,"plate":"ZH-614198"},{"confidence":1.3708385600851932e-18,"plate":
            "ZH 614198E"},{"confidence":1.3708385600851932e-18,"plate":"ZEH 614198"},{"confidence":
            1.3708385600851932e-18,"plate":"ZHE 614198"},{"confidence":1.3708385600851932e-18,"plate":"EZH 614198"},
            {"confidence":1.3708385600851932e-18,"plate":"ZH 61419E8"},{"confidence":1.3708385600851932e-18,"plate":
            "ZH 6141E98"},{"confidence":1.3708385600851932e-18,"plate":"ZH 614E198"},{"confidence":
            1.3708385600851932e-18,"plate":"ZH 61E4198"}],"confidence":3.4705942967674654e-18,"country":{"code":"CH",
            "confidence":1.0,"state":"ZH"},"id":"ZH 614198","no_countrylogic_id":"ZH 614198","track_id":
            1638169339870027893,"type":"lpr"}]},"gateway":{"direction":"in","gate":"einfahrt-garage"},"last_update":
            1638169344.854489,"leave-time":1638169347.330894,"make_model":{"make":"TESLA","make_confidence":
            0.8966485167223603,"model":"UNKNOWN","model_confidence":-1.0},"medium":{"lpr":{"alternatives":
            [{"confidence":3.4705942967674654e-18,"plate":"ZH 614198"},{"confidence":1.419478673564383e-18,
            "plate":"ZH-614198"},{"confidence":1.3708385600851932e-18,"plate":"ZH 614198E"},{"confidence":
            1.3708385600851932e-18,"plate":"ZEH 614198"},{"confidence":1.3708385600851932e-18,"plate":"ZHE 614198"},
            {"confidence":1.3708385600851932e-18,"plate":"EZH 614198"},{"confidence":1.3708385600851932e-18,"plate":
            "ZH 61419E8"},{"confidence":1.3708385600851932e-18,"plate":"ZH 6141E98"},{"confidence":
            1.3708385600851932e-18,"plate":"ZH 614E198"},{"confidence":1.3708385600851932e-18,"plate":"ZH 61E4198"}],
            "changed":false,"confidence":3.4705942967674654e-18,"country":{"code":"CH","confidence":1.0,"state":"ZH"},
            "id":"ZH 614198","no_countrylogic_id":"ZH 614198","track_id":1638169339870027893,"type":"lpr"}},"name":
            "forward-om_alpr_tracking_3","present-area-name":"einfahrt-garage","source":"einfahrt-garage",
            "timestamp":1638169352.606454,"type":"forward","unsure":false,"vehicle_id":1638169340812374101}"""
            parsed_message = PresenceForwardMessage(**orjson.loads(message))
        except ValidationError as e:
            assert False, "Parsing Presence Message failed"
