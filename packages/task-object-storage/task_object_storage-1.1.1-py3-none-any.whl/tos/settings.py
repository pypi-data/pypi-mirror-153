"""Settings and variables for TOS."""
import os
import platform


DIRNAME = os.path.dirname(os.path.abspath(__file__))
PACKAGE_ROOT = os.path.abspath(os.path.join(DIRNAME, os.pardir))
PLATFORM = platform.system()

#:
DEFAULT_DB_ADDRESS = "mongodb://localhost:27017/"


class ErrorMessages():
    SEP_PAYLOADS_NOT_INITIALIZED = \
        "Operation not supported without separated payloads collection"
    OPERATION_NOT_SUPPORTED_WITH_SEP_PAYLOADS = \
        "Operation is not supported with separated payloads collection"
