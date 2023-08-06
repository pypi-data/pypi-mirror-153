import asyncio
import copy


def sig(hub, ctx, name, *args, **kwargs):
    ...


def pre(hub, ctx):
    """
    Before every state, fire an event with the ref and sanitized parameters
    """
    raw_kwargs = ctx.get_arguments()
    # Fire an event with kwargs without actually modifying kwargs
    # Copying the hub will cause a recursion error
    kwargs = {k: copy.copy(v) for k, v in raw_kwargs.items() if k != "hub"}
    name = kwargs.get("name", None)

    # Don't include credentials in the fired event
    kwargs.get("ctx", {}).pop("acct", None)

    hub.idem.event.put_nowait(
        profile="idem-state",
        # Remove 'states.' from the ref so that it looks like the sls file
        body={name: {f"{ctx.ref[7:]}.{ctx.func.__name__}": kwargs}},
        tags={"ref": f"{ctx.ref}.{ctx.func.__name__}", "type": "state-pre"},
    )


async def _return_coro(hub, ctx):
    ret = await hub.pop.loop.unwrap(ctx.ret)
    await hub.idem.event.put(
        profile="idem-state",
        body=ret,
        tags={"ref": f"{ctx.ref}", "type": "state-post"},
    )
    return ret


def post(hub, ctx):
    """
    Fire an event at the end of every state
    """
    if asyncio.iscoroutine(ctx.ret):
        return _return_coro(hub, ctx)
    else:
        hub.idem.event.put_nowait(
            body=ctx.ret,
            profile="idem-state",
            tags={"ref": f"{ctx.ref}.{ctx.func.__name__}", "type": "state-post"},
        )
        return ctx.ret
