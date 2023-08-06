"""
Plugin to skip state management
"""
from typing import Any
from typing import Dict


async def get_state(hub, ctx) -> Dict[str, Any]:
    return {}


async def set_state(hub, ctx, state: Dict[str, Any]):
    ...


async def enter(hub, ctx):
    ...


async def exit_(hub, ctx, handle, exception: Exception):
    ...
