from typing import Any
from typing import Dict


def define(hub) -> Dict[str, Any]:
    """
    Return the definition used by the runtime to insert the conditions of the
    given requisite
    """
    return {
        "result": [True, None],
    }
