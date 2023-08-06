import traceback

import os
import sys
from functools import partial

import logging
import time
from zmq import ContextTerminated
from openmodule.config import settings


def _thread_wrapper(*args, _run_function, _return_code, **kwargs):
    try:
        _run_function(*args, **kwargs)
    except (KeyboardInterrupt, ContextTerminated):  # pragma: no cover
        pass
    except Exception as e:  # pragma: no cover
        # during testing we capture the exceptions in a file, because python testing utils are capturing the
        # stdout/stderr and do not print output if we exit with os._exit()
        if settings.TESTING:
            with open("thread_wrapper_error.log", "w") as f:
                f.write("\n".join([str(e), traceback.format_exc()]))
        else:
            # not using logging here because it may invoke sentry and the zmq publisher
            # we just want to die as reliabl possible here, something terrible has already happened
            sys.stderr.write(traceback.format_exc())
            sys.stderr.write("\n")
            sys.stderr.flush()
        time.sleep(1)
        os._exit(_return_code)


def get_thread_wrapper(function, return_code=10):
    return partial(_thread_wrapper, _run_function=function, _return_code=return_code)

