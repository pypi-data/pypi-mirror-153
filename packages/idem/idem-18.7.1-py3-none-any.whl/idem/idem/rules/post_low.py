import copy
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
        id_ = f"{chunk['__id__']}_listen"
        post_chunk = copy.deepcopy(chunk)
        post_chunk["fun"] = condition
        post_chunk["__id__"] = id_
        post_chunk["name"] = id_
        post_chunk["order"] = -1
        hub.idem.RUNS[name]["post_low"].append(post_chunk)
    return ret
