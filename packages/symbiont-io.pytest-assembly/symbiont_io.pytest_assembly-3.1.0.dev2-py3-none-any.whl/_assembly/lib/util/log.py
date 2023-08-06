# import queue
import sys
import time
import traceback
import inspect
import json
import logging

from collections import OrderedDict
from datetime import datetime
from dateutil.tz import tzlocal

logger = logging.getLogger(__name__)

TRACE = 5
# re-exporting the below so there is a consistent place to get these by consumer libraries
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
error = logging.error
FATAL = logging.FATAL


class InvalidLogMessageError(Exception):
    pass


class LogJsonFormatter(logging.Formatter):
    def __init__(self, component, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def _default_json_parser(obj):
            if inspect.istraceback(obj):
                tb = "".join(traceback.format_tb(obj))
                return tb.strip()
            elif isinstance(obj, Exception):
                return "Exception: %s" % str(obj)
            return str(obj)

        self._default_json_parser = _default_json_parser
        self.component = component
        # Filter out useless Python log fields
        self.ignore_fields = (
            "msg",
            "args",
            "span",
            "event",
            "msecs",
            "process",
            "levelno",
            "tracer",
            "funcName",
            "processName",
            "created",
            "relativeCreated",
            "name",
            "stack_info",
            "threadName",
        )

    def format(self, record):
        record_dict = OrderedDict(record.__dict__)
        record_dict["component"] = self.component
        record_dict["node_time"] = isodt(record.created)

        record_dict["message"] = record.getMessage()
        record_dict["line_number"] = record_dict["lineno"]
        record_dict["level_name"] = record_dict["levelname"]

        del record_dict["lineno"]
        del record_dict["levelname"]

        record_dict["private"] = True

        for key in self.ignore_fields:
            if key in record_dict:
                del record_dict[key]

        return json.dumps(record_dict, default=self._default_json_parser)

    def formatTime(self, record):
        return record.created


def set_up(logger, component, log_level, console=True, file=None):

    logger.handlers = []

    logging.addLevelName(TRACE, "TRACE")

    logger.setLevel(log_level)

    formatter = LogJsonFormatter(component="symbiont.{}".format(str(component).lower()))

    handlers = []

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    if file:
        file_handler = logging.FileHandler(file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    for handler in handlers:
        logger.addHandler(handler)

    # Quieten noisy libraries.
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(log_level)
    requests_log.propagate = False
    urllib3_log = logging.getLogger("urllib3")
    urllib3_log.setLevel(log_level)
    urllib3_log.propagate = False
    amqpstorm_log = logging.getLogger("amqpstorm")
    amqpstorm_log.setLevel(logging.WARNING)

    # Disable InsecureRequestWarning
    try:
        from requests.packages import urllib3 as requests_urllib3

        requests_urllib3.disable_warnings()
    except ImportError:
        pass

    # Log unhandled errors.
    def handle_exception(exc_type, exc_value, exc_traceback):
        logger.error(
            "Unhandled Exception: {}".format(str(exc_value)),
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception


def curr_time():
    return int(time.time())


def isodt(epoch_time):
    try:
        isodt = datetime.fromtimestamp(epoch_time, tzlocal()).isoformat()
        return isodt

    except OSError:
        return epoch_time


def setup_logging(component, log_level):
    root_logger = logging.getLogger()
    set_up(root_logger, component, log_level.upper())
    logger.log(TRACE, "initialized trace logging")
    logger.debug("initialized debug logging")
    logger.info("initialized info logging")


def setup_sdk_logging(component, log_level, filename):
    root_logger = logging.getLogger()
    set_up(root_logger, component, log_level.upper(), console=False, file=filename)
    logger.log(TRACE, "initialized trace logging")
    logger.debug("initialized debug logging")
    logger.info("initialized info logging")
