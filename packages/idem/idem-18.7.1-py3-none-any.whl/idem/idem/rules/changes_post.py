from typing import Any
from typing import Dict


def check(
    hub,
    name: str,
    ctx: Dict[str, Any],
    condition: Any,
    reqret: Dict[str, Any],
    chunk: Dict[str, Any],
) -> Dict[str, Any]:
    """
    If changes are made then run the configured post command
    """
    ret = {}
    if reqret["ret"]["changes"]:
        func = getattr(hub, f'states.{chunk["state"]}.{condition}')
        if func:
            ret["post"] = func
    return ret
