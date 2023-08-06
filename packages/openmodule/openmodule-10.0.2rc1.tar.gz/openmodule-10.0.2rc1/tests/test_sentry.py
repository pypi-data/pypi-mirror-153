import logging
from unittest import TestCase

import sentry_sdk

from openmodule.core import init_openmodule, shutdown_openmodule
from openmodule.sentry import init_sentry, deinit_sentry
from openmodule_test.core import OpenModuleCoreTestMixin
from openmodule_test.zeromq import ZMQTestMixin


class SentryInitTestCase(ZMQTestMixin, TestCase):
    topics = ["sentry"]
    """
    checks if sentry is initialized based on the current environment
    """

    def assertSentryIsInitialized(self, is_initialized):
        sentry_sdk.capture_message("my message")

        if is_initialized:
            self.zmq_client.wait_for_message_on_topic(b"sentry")
        else:
            with self.assertRaises(TimeoutError):
                self.zmq_client.wait_for_message_on_topic(b"sentry")

    def test_init_during_debug_override(self):
        """
        sentry=True activates sentry, even in debug mode
        """

        # test b)
        config = self.zmq_config()
        config.DEBUG = True
        config.TESTING = False
        with self.assertLogs() as cm:
            init_openmodule(config, context=self.zmq_context(), sentry=True)
        self.assertNotIn("not activating sentry", str(cm.output))
        try:
            self.assertSentryIsInitialized(True)
        finally:
            shutdown_openmodule()

    def test_init_during_testing(self):
        """
        sentry=True activates sentry, even in test mode
        """

        # test a)
        config = self.zmq_config()
        config.DEBUG = False
        config.TESTING = True
        with self.assertLogs() as cm:
            init_openmodule(config, context=self.zmq_context(), sentry=True)
        self.assertNotIn("not activating sentry", str(cm.output))
        try:
            self.assertSentryIsInitialized(True)
        finally:
            shutdown_openmodule()

    def test_init_during_production(self):
        """
        sentry=None -> this is the default value, only activated if debug=False and testing=False
        """

        # test a)
        config = self.zmq_config()
        config.DEBUG = False
        config.TESTING = False
        with self.assertLogs() as cm:
            init_openmodule(config, context=self.zmq_context(), sentry=False)
        self.assertNotIn("not activating sentry", str(cm.output))  # explicitly setting false does not log this
        try:
            self.assertSentryIsInitialized(False)
        finally:
            shutdown_openmodule()

    def test_init_during_debug(self):
        """
        sentry=None -> this is the default value
          a) don't init during testing
          b) and don't init during debug
          + logs that it was not initialized
        """

        # test b)
        config = self.zmq_config()
        config.DEBUG = True
        config.TESTING = False
        with self.assertLogs() as cm:
            init_openmodule(config, context=self.zmq_context(), sentry=None)
        self.assertIn("not activating sentry", str(cm.output))
        try:
            self.assertSentryIsInitialized(False)
        finally:
            shutdown_openmodule()

    def test_init_during_testing(self):
        """
        sentry=None -> this is the default value
          a) don't init during testing
          b) and don't init during debug
          + logs that it was not initialized
        """

        # test a)
        config = self.zmq_config()
        config.DEBUG = False
        config.TESTING = True
        with self.assertLogs() as cm:
            init_openmodule(config, context=self.zmq_context(), sentry=None)
        self.assertIn("not activating sentry", str(cm.output))
        try:
            self.assertSentryIsInitialized(False)
        finally:
            shutdown_openmodule()

    def test_init_during_production(self):
        """
        sentry=None -> this is the default value, only activated if debug=False and testing=False
        """

        # test a)
        config = self.zmq_config()
        config.DEBUG = False
        config.TESTING = False
        with self.assertLogs() as cm:
            init_openmodule(config, context=self.zmq_context(), sentry=None)
        self.assertNotIn("not activating sentry", str(cm.output))
        try:
            self.assertSentryIsInitialized(True)
        finally:
            shutdown_openmodule()


class SentryTestCase(OpenModuleCoreTestMixin, TestCase):
    topics = ["sentry"]

    def tearDown(self):
        super().tearDown()
        deinit_sentry()

    def test_sentry_init(self):
        sentry_sdk.capture_message("test message")
        with self.assertRaises(TimeoutError):
            self.zmq_client.wait_for_message_on_topic(b"sentry")

        init_sentry(self.core)
        sentry_sdk.capture_message("test message")

        sentry_message = self.zmq_client.wait_for_message_on_topic(b"sentry")
        self.assertIn("event", sentry_message)

    def test_sentry_logging_integration(self):
        init_sentry(self.core)
        logging.error("Some error, please help!")

        sentry_message = self.zmq_client.wait_for_message_on_topic(b"sentry")
        self.assertIn("event", sentry_message)

    def test_extras_are_set(self):
        self.core.config.RESOURCE = "some-test-resource123"
        init_sentry(self.core, extras={"some-more-extras" + "123": True})

        logging.error("Some error, please help!", extra={"even-more-extras" + "123": "yes!"})
        sentry_message = self.zmq_client.wait_for_message_on_topic(b"sentry")

        # we dont know exactly where sentry puts its stuff, so simply check string contains
        event = str(sentry_message["event"])
        self.assertIn("some-test-resource123", event)
        self.assertIn("even-more-extras123", event)
        self.assertIn("some-more-extras123", event)

        # just to be sure, that sentry doesnt put the code here in its event, this would also cause all tests to succeed
        self.assertNotIn("wait_for_message_on_topic", event)
