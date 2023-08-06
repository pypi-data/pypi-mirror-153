from typing import Any
from typing import Dict


def define(hub) -> Dict[str, Any]:
    """
    Define how the onchanges requisite should run
    """
    return {
        "result": True,
        "changes": True,
    }
