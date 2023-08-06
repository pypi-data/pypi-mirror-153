import logging
import sys

from phiterm.conf.constants import PHI_LOGGER_NAME, PHIDATA_LOGGER_NAME


def get_simple_logger(logger_name: str) -> logging.Logger:

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    simple_formatter = logging.Formatter(
        "%(lineno)d - %(filename)s - %(levelname)s - %(message)s"
    )
    # dttm_formatter = logging.Formatter(
    #     "%(asctime)s - %(lineno)d - %(filename)s - %(levelname)s - %(message)s",
    #     "%Y-%m-%d %H:%M",
    # )
    handler.setFormatter(simple_formatter)

    _logger = logging.getLogger(logger_name)
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)
    _logger.propagate = False
    return _logger


def get_rich_logger(logger_name: str) -> logging.Logger:

    from rich.logging import RichHandler

    # https://rich.readthedocs.io/en/latest/reference/logging.html#rich.logging.RichHandler
    # https://rich.readthedocs.io/en/latest/logging.html#handle-exceptions
    rich_handler = RichHandler(rich_tracebacks=False, show_time=False)
    rich_handler.setFormatter(
        logging.Formatter(
            fmt="%(message)s",
            datefmt="[%X]",
        )
    )

    _logger = logging.getLogger(logger_name)
    _logger.addHandler(rich_handler)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False
    return _logger


logger: logging.Logger = get_rich_logger(PHI_LOGGER_NAME)


def set_log_level_to_debug():
    phi_logger = logging.getLogger(PHI_LOGGER_NAME)
    phi_logger.setLevel(logging.DEBUG)
    phidata_logger = logging.getLogger(PHIDATA_LOGGER_NAME)
    phidata_logger.setLevel(logging.DEBUG)
