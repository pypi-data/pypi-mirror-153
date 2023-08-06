"""This module contains a set of utility functions for dictionaries."""
import collections.abc
from typing import Any, Dict, List, Union

import numpy as np

from . import LOG

Numeric = Union[
    bool,
    int,
    float,
    np.int16,
    np.int32,
    np.int64,
    np.float16,
    np.float32,
    np.float64,
    str,
]


def update(src: Dict[str, Any], upd: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive update of dictionaries.

    See stackoverflow:

        https://stackoverflow.com/questions/3232943/
        update-value-of-a-nested-dictionary-of-varying-depth

    """
    for key, val in upd.items():
        if isinstance(val, collections.abc.Mapping):
            src[key] = update(src.get(key, {}), val)
        else:
            src[key] = val
    return src


def convert(src: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive conversion to basic data types."""
    k2d = list()
    for key, val in src.items():
        nkey = convert_val(key)
        if type(nkey) != type(key):
            k2d.append(key)
        key = nkey
        if isinstance(val, collections.abc.Mapping):
            src[key] = convert(val)
        elif isinstance(val, (list, np.ndarray)):
            src[key] = convert_list(val)
        else:
            src[key] = convert_val(val)
    for key in k2d:
        src.pop(key)
    return src


def convert_list(old_list: List[Any]) -> List[Any]:
    new_list = list()
    for val in old_list:
        if isinstance(val, collections.abc.Mapping):
            new_list.append(convert(val))
        elif isinstance(val, (list, tuple, np.ndarray)):
            new_list.append(convert_list(val))
        else:
            new_list.append(convert_val(val))
    return new_list


def convert_val(val: Numeric) -> Union[bool, int, float, str]:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, np.int16, np.int32, np.int64)):
        return int(val)
    if isinstance(val, (float, np.float16, np.float32, np.float64)):
        return float(val)

    try:
        return strtobool(val)
    except (ValueError, TypeError, AttributeError):
        pass
    try:
        return int(val)
    except (ValueError, TypeError):
        pass
    try:
        return float(val)
    except (ValueError, TypeError):
        pass
    try:
        return str(val)
    except (ValueError, TypeError):
        LOG.info("Unable to convert value %s", val)

    return "MISSING_VALUE"


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true or false.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false
    values are 'n', 'no', 'f', 'false', 'off', and '0'. Raises
    ValueError if 'val' is anything else.

    This is mostly the implementation of the now deprecated
    distutils package. However, it is change in that regard that an
    actual bool type value is returned instead of 1 or 0.

    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {val}")


def tobool(val: Union[bool, int, float, str]) -> bool:
    """Convert any basic type representation to true or false"""

    if isinstance(val, bool):
        return val

    elif isinstance(val, int):
        return val != 0

    elif isinstance(val, float):
        return val != 0.0

    elif isinstance(val, str):
        return strtobool(val)

    else:
        raise ValueError(
            f"Cannot convert value {val} of type {type(val)} to bool."
        )
