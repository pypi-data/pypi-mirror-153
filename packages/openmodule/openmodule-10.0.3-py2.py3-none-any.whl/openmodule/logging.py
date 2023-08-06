import logging


def init_logging(core):
    assert hasattr(core.config, "LOG_LEVEL"), (
        "LOG_LEVLE setting not found in your config. In order to use logging please add \n"
        "> LOG_LEVEL = config.log_level()\n"
        "to your config.py"
    )
    logging.basicConfig(level=core.config.LOG_LEVEL)
    logging.captureWarnings(True)
