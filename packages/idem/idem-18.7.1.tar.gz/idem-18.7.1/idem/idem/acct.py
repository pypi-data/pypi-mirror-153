from typing import Any
from typing import Dict
from typing import Iterable

import aiofiles
import dict_tools.data

__func_alias__ = {"ctx_": "ctx"}


async def ctx_(
    hub,
    path: str,
    acct_profile: str = "default",
    acct_file: str = None,
    acct_key: str = None,
    acct_blob: bytes = None,
    acct_data: Dict = None,
):
    """
    :param hub:
    :param path:
    :param acct_profile:
    :param acct_file:
    :param acct_key:
    :param acct_blob:
    :param acct_data:
    :return:
    """
    ctx = dict_tools.data.NamespaceDict()

    parts = path.split(".")
    if parts[0] in ("exec", "states", "esm"):
        parts = parts[1:]
    elif parts[0] in ("idem",) and parts[1] in ("sls",):
        parts = parts[2:]

    sname = parts[0]

    acct_paths = (
        f"exec.{sname}.ACCT",
        f"states.{sname}.ACCT",
        f"esm.{sname}.ACCT",
        f"source.{sname}.ACCT",
    )

    if acct_data is None:
        acct_data = {}
    if acct_key:
        if acct_file:
            async with aiofiles.open(acct_file, "rb") as fh:
                acct_blob = await fh.read()
        if acct_blob:
            acct_data.update(
                await hub.acct.init.unlock_blob(acct_blob, acct_key=acct_key)
            )

    subs = set()
    for name in acct_paths:
        sub = getattr(hub, name, None)
        if not sub:
            continue
        if isinstance(sub, Iterable):
            subs.update(sub)

    # The SafeNamespaceDict will not print it's values, only keys
    ctx.acct = dict_tools.data.SafeNamespaceDict(
        await hub.acct.init.gather(
            subs,
            acct_profile,
            profiles=acct_data.get("profiles"),
        )
    )

    return ctx


async def data(hub, acct_key: str, acct_file: str, acct_blob: bytes) -> Dict[str, Any]:
    """
    Return a raw dictionary with all the profiles from an encrypted acct
    """
    acct_data = {}
    if acct_key:
        if acct_file:
            async with aiofiles.open(acct_file, "rb") as fh:
                acct_blob = await fh.read()
        if acct_blob:
            acct_data = await hub.acct.init.unlock_blob(acct_blob, acct_key=acct_key)
    return acct_data
