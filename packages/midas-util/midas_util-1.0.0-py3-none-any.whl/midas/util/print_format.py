import pprint
from typing import Any

from .runtime_config import RuntimeConfig


def mformat(msg: Any) -> str:

    if RuntimeConfig().misc["use_pprint"]:
        return pprint.pformat(msg)
    else:
        return str(msg)
