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
    Check to see if the result is True
    """
    if isinstance(condition, bool):
        if bool(reqret["ret"]["changes"]) is condition:
            return {}
    # TODO: Add the ability to make more granular changes condition definitions
    elif reqret["ret"]["changes"] == condition:
        return {}
    return {
        "errors": [
            f'Changes from {reqret["r_tag"]} is "{reqret["ret"]["result"]}", not "{condition}"'
        ]
    }
