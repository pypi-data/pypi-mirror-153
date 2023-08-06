"""Utility functions for TOS."""
import functools
import os
import tempfile
from bson.objectid import ObjectId


def accept_string_object_ids(func):
    """Convert first function argument to ObjectId.

    Decorator for converting possible ``str``
    type object ids to ``ObjectId`` type.
    Assume the object id is the first argument passed
    to ``func``.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args = list(args)
        if isinstance(args[1], str):
            args[1] = ObjectId(args[1])  # assuming it's the second
        elif isinstance(args[1], ObjectId):
            pass
        else:
            raise ValueError("Second argument should be object id as string or ObjectId")
        value = func(*args, **kwargs)
        return value
    return wrapper


def get_temporary_file(prefix="tmp_", suffix="", directory=None):
    """Generate a safe and closed filepath."""
    f, filepath = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=directory)
    os.close(f)

    return filepath
