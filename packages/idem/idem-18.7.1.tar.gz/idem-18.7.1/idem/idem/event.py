from typing import Any
from typing import Dict


async def put(
    hub,
    body: Any,
    profile: str = "default",
    tags: Dict[str, Any] = None,
):
    if tags is None:
        tags = {}

    await hub.evbus.broker.put(
        profile=profile, body=dict(tags=tags, message=body, run_name=hub.idem.RUN_NAME)
    )


def put_nowait(
    hub,
    body: Any,
    profile: str = "default",
    tags: Dict[str, Any] = None,
):
    if tags is None:
        tags = {}

    hub.evbus.broker.put_nowait(
        profile=profile, body=dict(tags=tags, message=body, run_name=hub.idem.RUN_NAME)
    )
