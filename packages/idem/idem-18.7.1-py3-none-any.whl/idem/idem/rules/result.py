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
    if isinstance(condition, list):
        if reqret["ret"]["result"] in condition:
            return {}
    if reqret["ret"]["result"] is condition:
        return {}
    else:
        return {
            "errors": [
                f'Result of require {reqret["r_tag"]} is "{reqret["ret"]["result"]}", not "{condition}"'
            ]
        }
