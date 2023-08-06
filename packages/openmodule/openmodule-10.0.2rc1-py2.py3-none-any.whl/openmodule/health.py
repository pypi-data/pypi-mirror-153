import logging
import time
from collections import namedtuple
from enum import Enum
from typing import Optional, Dict, Callable, Any

from openmodule.models.base import ZMQMessage, OpenModuleModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from openmodule.core import OpenModuleCore


class HealthzStatus(str, Enum):
    ok = "ok"
    error = "error"


class HealthPongPayload(OpenModuleModel):
    status: HealthzStatus
    meta: Dict
    version: str
    name: str
    startup: float
    message: Optional[str]


class HealthPongMessage(ZMQMessage):
    type: str = "healthz"
    pong: HealthPongPayload


class HealthPingMessage(ZMQMessage):
    type: str = "ping"


startup = time.time()

HealthResult = namedtuple("HealthResult", "status,message,meta")


def health_ok(meta=None) -> HealthResult:
    return HealthResult(HealthzStatus.ok, None, meta)


def health_error(message, meta=None) -> HealthResult:
    return HealthResult(HealthzStatus.error, message, meta)


HealthHandlerType = Callable[[], HealthResult]


class Healthz:
    health_handler: HealthHandlerType

    def __init__(self, core: 'OpenModuleCore', health_handler: Optional[HealthHandlerType] = None):
        self.health_handler = health_handler or health_ok
        self.core = core
        self.log = logging.getLogger(self.__class__.__name__)

    def process_message(self, _: HealthPingMessage):
        try:
            result = self.health_handler()
        except Exception as e:
            self.log.exception(e)
            result = health_error("internal error in health routine")

        if not isinstance(result, HealthResult):
            self.log.error(f"invalid return type '{type(result)}' from health handler, "
                           f"expected HealthResult")
            result = health_error("internal error in health routine")

        response = HealthPongMessage(
            name=self.core.config.NAME,
            pong=dict(
                status=result.status,
                message=result.message,
                version=self.core.config.VERSION,
                name=self.core.config.NAME,
                startup=startup,
                meta=result.meta or {}))
        self.core.publish(response, b"healthz")
