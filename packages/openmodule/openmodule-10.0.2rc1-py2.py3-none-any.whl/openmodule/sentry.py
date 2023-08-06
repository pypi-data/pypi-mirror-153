import logging
from socket import gethostname
from typing import Optional, Dict, Any
from typing import TYPE_CHECKING

import sentry_sdk
from sentry_sdk.transport import Transport

from openmodule.models.base import ZMQMessage

if TYPE_CHECKING:  # pragma: no cover
    from openmodule.core import OpenModuleCore


class SentryEvent(ZMQMessage):
    type: str = "sentry"
    event: Any


class ZeroMQTransport(Transport):
    def __init__(self, core, options: Optional[Dict[str, Any]] = None):
        self.core = core
        super(ZeroMQTransport, self).__init__(options)

    def capture_event(self, event):
        message = SentryEvent(name=self.core.config.NAME, event=event)
        self.core.publish(message, b"sentry")

    def capture_envelope(self, envelope):
        raise NotImplementedError()

    def flush(self, timeout, callback=None):
        pass

    def kill(self):
        pass


def init_sentry(core: 'OpenModuleCore', extras=None, **kwargs):
    """
    This function initializes Sentry with our predefined values. This function also check if Sentry should be
    initialized.

    :param core: openmodule core instance
    :param extras: global extras that should be added to message
    :param kwargs: client supported **kwargs see ClientOptions
    """
    zmq_transport = ZeroMQTransport(core)
    environment = environment_from_config(core.config)
    server_name = core.config.RESOURCE
    if not server_name:
        core.log.warning("resource not available using hostname instead for sentry tag")
        server_name = gethostname()
    sentry_sdk.init(
        dsn=None, release=core.config.VERSION, server_name=server_name, environment=environment,
        transport=zmq_transport, **kwargs
    )

    extras = extras or {}
    extras.update(extra_from_config(core.config))
    with sentry_sdk.configure_scope() as scope:
        for key, value in extras.items():
            scope.set_extra(key, value)


def deinit_sentry():
    sentry_sdk.init(dsn=None)


def should_activate_sentry(config) -> bool:
    """
    This function checks if for the given config Sentry should be activated or not.
    This is only false for debug mode. During testing we do not have a sentry-sender
    running anyways.

    :param config: current configuration
    :return: bool
    """
    if config.DEBUG or config.TESTING:
        return False
    else:
        return True


def environment_from_config(config) -> str:
    """
    This functions returns either the environment of the current configuration.

    :param config: current configuration
    :return: 'staging' or 'production'
    """
    if hasattr(config, "DEVICE_HOST") and ("test" in config.DEVICE_HOST):
        return "staging"
    else:
        return "production"


def extra_from_config(config):
    extra = {
        "name": config.NAME,
    }
    if hasattr(config, "GATE"):
        extra["gate"] = config.GATE
    return extra
