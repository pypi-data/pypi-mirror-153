import asyncio
from typing import Awaitable

from idem.exec.init import ExecReturn


def _create_exec_return(hub, ret, ref: str):
    if isinstance(ret, ExecReturn):
        return ret
    hub.idem.event.put_nowait(
        body=ret,
        profile="idem-exec",
        tags={"ref": ref, "type": "exec-post"},
    )
    try:
        return ExecReturn(
            **ret,
            ref=ref,
        )
    except TypeError:
        raise TypeError(
            f"Exec module '{ref}' did not return a dictionary: "
            "\n{'result': True|False, 'comment': Any, 'ret': Any}"
        )


async def _create_exec_return_coro(hub, ret: Awaitable, ref: str):
    ret = await hub.pop.loop.unwrap(ret)
    return _create_exec_return(hub, ret, ref)


def post(hub, ctx):
    """
    Convert the dict return to an immutable namespace addressable format
    """
    ref = f"{ctx.ref}.{ctx.func.__name__}"
    if asyncio.iscoroutine(ctx.ret):
        return _create_exec_return_coro(hub, ctx.ret, ref)
    else:
        return _create_exec_return(hub, ctx.ret, ref)
