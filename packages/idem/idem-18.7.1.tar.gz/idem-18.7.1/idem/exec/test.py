from typing import Any
from typing import Dict

__func_alias__ = {"ctx_": "ctx"}
__contracts__ = ["returns", "soft_fail"]


def __init__(hub):
    hub.exec.test.ITEMS = {}
    hub.exec.test.ACCT = ["test"]


def ping(hub):
    """
    Immediately return success
    """
    return {"result": True, "ret": True}


async def aping(hub):
    return {"result": True, "ret": True}


def ctx_(hub, ctx):
    return {"result": True, "comment": None, "ret": ctx}


def fail(hub):
    raise Exception("Expected failure")


async def afail(hub):
    raise Exception("Expected failure")


def echo(hub, value):
    """
    Return the parameter passed in without changing it at all
    """
    return value


async def aecho(hub, value):
    """
    Return the parameter passed in without changing it at all
    """
    return value


def more(hub, ctx, *args, **kwargs):
    """
    Return the ctx and all parameters passed to this state.
    """
    return {
        "result": True,
        "comment": None,
        "ret": {"args": args, "kwargs": kwargs, "ctx": ctx},
    }


async def event(
    hub,
    body: str,
    ingress_profile: str = "default",
    tags: Dict[str, Any] = None,
):
    """
    :param body: The event body
    :param ingress_profile: The ingress profile to allowlist for this event

    .. code-block:: bash

        $ idem exec test.event body ingress_profile="default" --serialize-plugin="json"
        $ idem exec test.event body="my_event" ingress_profile="default" --serialize-plugin="json"
    """
    event_kwargs = dict(body=body, profile=ingress_profile, tags=tags)
    await hub.idem.event.put(**event_kwargs)
    return {"result": True, "ret": event_kwargs}
