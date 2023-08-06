from typing import Any
from typing import Dict


async def sig_loop(
    hub,
    pending_plugin: str,
    name: str,
    apply_kwargs: Dict[str, Any],
):
    """
    Validate the signature of the reconciliation loop function
    """
    ...


def post_loop(hub, ctx):
    """
    Conform the return structure of every loop function to this format.
    """
    assert isinstance(ctx.ret["re_runs_count"], int)
    assert isinstance(ctx.ret["require_re_run"], bool)
    return ctx.ret
