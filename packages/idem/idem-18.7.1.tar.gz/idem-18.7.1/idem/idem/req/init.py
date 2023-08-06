from typing import Any
from typing import Dict


def define(hub) -> Dict[str, Any]:
    """
    Gather the requisite restrictions and populate the requisite behavior map
    """
    rmap = {}
    for mod in hub.idem.req._loaded:
        if mod == "init":
            continue
        rmap[mod] = hub.idem.req[mod].define()
    return rmap
