from typing import Any
from typing import Dict
from typing import Tuple

import pop.hub

__func_alias__ = {"ctx_": "ctx"}


async def run(
    hub,
    path: str,
    args: Tuple[Any],
    kwargs: Dict[str, Any],
    *,
    acct_file: str = None,
    acct_key: str = None,
    acct_blob: bytes = None,
    acct_profile: str = None,
    acct_data: Dict[str, Any] = None,
):
    if acct_profile is None:
        acct_profile = hub.acct.DEFAULT

    args = [a for a in args]

    if not path.startswith("exec."):
        path = f"exec.{path}"

    func = hub[path]
    if isinstance(func, pop.hub.ReverseSub):
        params = func._resolve().signature.parameters
    else:
        params = func.signature.parameters

    if "ctx" in params:
        ctx = await hub.idem.acct.ctx(
            path,
            acct_file=acct_file,
            acct_key=acct_key,
            acct_profile=acct_profile,
            acct_blob=acct_blob,
            acct_data=acct_data,
        )
        args.insert(0, ctx)

    ret = func(*args, **kwargs)
    return await hub.pop.loop.unwrap(ret)


async def single(hub, path: str, *args, **kwargs):
    acct_file = hub.OPT.acct.acct_file
    acct_key = hub.OPT.acct.acct_key
    acct_profile = hub.OPT.acct.get("acct_profile", hub.acct.DEFAULT)

    ret = await hub.idem.ex.run(
        path,
        args=args,
        kwargs=kwargs,
        acct_file=acct_file,
        acct_key=acct_key,
        acct_profile=acct_profile,
    )
    return ret
