import logging
import os
import time
from multiprocessing import Process, Event
from signal import SIGINT, SIGKILL
from typing import Callable, Union, Type, Optional
from unittest import TestCase

import multiprocessing_logging

from openmodule.core import shutdown_openmodule
from openmodule.utils.schema import Schema
from openmodule_test.health import HealthTestMixin


class ExceptionProcess(Process):
    def __init__(self, *args, **kwargs):
        is_finished = Event()
        super().__init__(*args, **kwargs)
        self.is_finished = is_finished

    def run(self):
        try:
            super().run()
            self.is_finished.set()
        except Exception as e:
            logging.exception(e)


class InterruptTestMixin(TestCase):
    """
    Helper class for testing interrupts and exceptions in code
    for usage, look at file tests/test_interrupt
    """

    process: Optional[ExceptionProcess] = None

    def _kill_process(self):
        # this is called in tear down and as a cleanup to make sure that under any circumstances the process is killed
        # otherwise you have processes lingering around, potentially blocking ports which is quite annoying
        if self.process and self.process.is_alive():
            os.kill(self.process.pid, SIGKILL)

    def setUp(self) -> None:
        self.addCleanup(self._kill_process)
        super().setUp()

    def tearDown(self):
        super().tearDown()
        Schema.to_file()
        self._kill_process()

    def wait_for_setup(self):
        pass

    def _wait_for_and_uninstall_mp_handler(self, logger=None):
        """
        waits until the multiprocessing logging handler has finished
        """
        if logger is None:
            logger = logging.getLogger()

        for handler in logger.handlers:
            if isinstance(handler, multiprocessing_logging.MultiProcessingHandler):
                handler.close()

        multiprocessing_logging.uninstall_mp_handler(logger)

    def start_process(self, f: Callable):
        """
        starts the process and waits until it is responsive by calling calls wait_for_setup()
        """
        multiprocessing_logging.install_mp_handler()
        self.process = ExceptionProcess(target=f)
        self.process.start()
        return self.process

    def assertCleanShutdown(self, process, shutdown_timeout: float = 3.0):
        """
        asserts that the process shuts down cleanly
        """
        if process.is_finished.wait(timeout=shutdown_timeout):
            self._wait_for_and_uninstall_mp_handler()
            return
        else:
            if process.is_alive():
                os.kill(process.pid, SIGKILL)
                raise TimeoutError("Process took to long for shutdown")
            else:
                raise AssertionError("Process did not finish gracefully")

    def send_signal_to_process(self, process: ExceptionProcess, signal: Union[Type[KeyboardInterrupt], int]):
        self.assertFalse(process.is_finished.is_set())
        if signal == KeyboardInterrupt:
            signal = SIGINT
        os.kill(process.pid, signal)

    def signal_in_function(self, f: Callable, signal: Union[Type[KeyboardInterrupt], int], *,
                           raise_exception_after: float = 3.0, shutdown_timeout: float = 3.0):
        """
        wraps the helper functions into a single function because apparently everybody likes
        to write framework functions which are hard to adopt and do one single thing and nothing
        else. mostly here for backwards compatibility and reference how to use the testcase
        """
        process = self.start_process(f)
        self.wait_for_setup()
        time.sleep(raise_exception_after)
        self.send_signal_to_process(process, signal)
        self.assertCleanShutdown(process, shutdown_timeout)


class MainTestMixin(HealthTestMixin, InterruptTestMixin):
    topics = ["healthz"]
    protocol = "tcp://"

    def wait_for_setup(self):
        self.wait_for_health()

    def tearDown(self):
        try:
            shutdown_openmodule()
        except AssertionError:
            pass
        super().tearDown()
