from typing import Any
from typing import Dict


def define(hub) -> Dict[str, Any]:
    """
    Define how the watch requisite should behave
    """
    return {
        "result": True,
        "changes_post": "mod_watch",
    }
