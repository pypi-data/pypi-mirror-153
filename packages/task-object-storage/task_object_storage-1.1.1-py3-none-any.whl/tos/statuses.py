"""
Items are given "new" status when the producer creates them.
When the consumers check out the item, its status will
be set as "processing". When the consumer finishes, the
status will be set "pass" or "fail" depending on the outcome.
when case for manual intervention is detected, the status
will be set to "expected_fail".
"""

# TODO: rename this module to `status.py`


def _get_props(object):
    return [getattr(object, k) for k in dir(object) if not k.startswith("_")]


class FailStatus:
    FAIL = "fail"
    EXPECTED_FAIL = "expected_fail"  # business error


class SkipStatus:
    SKIP = "skip"  # e.g., when the input data is invalid


class Status(FailStatus, SkipStatus):
    NEW = "new"
    PROCESSING = "processing"
    PASS = "pass"


#:
FAIL_STATUSES = _get_props(FailStatus)
SKIP_STATUSES = _get_props(SkipStatus)
VALID_STATUSES = _get_props(Status)


def is_failure(status):
    return status in FAIL_STATUSES


def is_business_failure(status):
    return status == FailStatus.EXPECTED_FAIL


def is_skip(status):
    return status in SKIP_STATUSES
