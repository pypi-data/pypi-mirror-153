from typing import Any
from typing import Dict


async def modify(hub, name: str, chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add the 'old_state' from a previous run to the ctx from the enforced state management
    """
    managed_state = hub.idem.RUNS[name]["managed_state"]

    if managed_state:
        tag = hub.idem.managed.gen_tag(chunk)
        chunk["ctx"]["old_state"] = managed_state.get(tag, None)
    else:
        chunk["ctx"]["old_state"] = None

    return chunk
