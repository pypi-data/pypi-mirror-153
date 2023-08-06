from typing import Any
from typing import Dict


async def run(
    hub,
    plugin: str = "none",
    pending_plugin: str = "default",
    name: str = None,
    apply_kwargs: Dict[str, Any] = None,
):
    if apply_kwargs is None:
        apply_kwargs = {}
    apply_kwargs["name"] = name
    ret = await hub.reconcile[plugin].loop(
        pending_plugin,
        name=name,
        apply_kwargs=apply_kwargs,
    )

    return ret
