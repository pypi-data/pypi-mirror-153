from typing import Any
from typing import Dict


async def modify(hub, name: str, chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Take the given run name and low chunk, and allow state plugins to modify
    the low chunk
    """
    for mod in hub.idem.mod:
        if mod.__name__ == "init":
            continue
        if hasattr(mod, "modify"):
            chunk = mod.modify(name, chunk)
            chunk = await hub.pop.loop.unwrap(chunk)
    return chunk
