"""
Plugin for local state management
"""
import os
import pathlib
from typing import Any
from typing import Dict

import aiofiles


def __init__(hub):
    hub.esm.local.ACCT = ["esm.local"]


async def get_state(hub, ctx) -> Dict[str, Any]:
    """
    Read this context's state from it's cache_file

    :param hub:
    :param ctx:
    :return:
    """
    cache_file = _cache_file(ctx)
    async with aiofiles.open(cache_file, "rb+") as fh:
        data = await fh.read()
        if not data:
            return {}
        state = hub.serial[ctx.acct.serial_plugin].load(data)
        return state


async def set_state(hub, ctx, state: Dict[str, Any]):
    """
    Write the state to this context's cache_file

    :param hub:
    :param ctx:
    :param state:
    :return:
    """
    cache_file = _cache_file(ctx)
    async with aiofiles.open(cache_file, "wb+") as fh:
        data: bytes = hub.serial[ctx.acct.serial_plugin].dump(state)
        await fh.write(data)


async def enter(hub, ctx):
    """
    Verify that only one instance of run_name exists for the current user
    """
    pid_file = ctx.acct.cache_dir / "esm" / f"{ctx.acct.run_name}.pid"
    pid_file.parent.mkdir(exist_ok=True, parents=True)

    # Enter the context of the pid_file
    pid = await hub.esm.local.verify(pid_file)
    if pid:
        # A process with a different PID is already running for this run_name
        raise ChildProcessError(
            f"idem run '{ctx.acct.run_name}' is already active in process: {pid}"
        )

    # Write the current pid to the pid_file
    pid_file.parent.mkdir(exist_ok=True, parents=True)
    async with aiofiles.open(pid_file, "w+") as fh:
        pid = str(os.getpid())
        await fh.write(pid)

    return pid_file


async def exit_(hub, ctx, handle: pathlib.Path, exception: Exception):
    if exception:
        hub.log.error(f"{exception.__class__.__name__}: {exception}")
        return
    if handle.exists():
        handle.unlink()


async def verify(hub, pid_file: pathlib.Path) -> int or None:
    """
    If a pid is in the given file and is running, then return it.
    """
    if not pid_file.exists():
        # There is no existing pid_file, nothing to check
        return None

    async with aiofiles.open(pid_file, "r") as fh:
        contents = await fh.read()

    try:
        old_pid = int(contents)
    except (ValueError, TypeError):
        hub.log.error(f"Invalid pid_file '{fh.name}': {contents}")
        # There's no valid running pid, just return
        return None

    if hub.esm.local.exists(old_pid):
        # The pid_file has a pid in it that is still active, return it
        return old_pid


def exists(hub, pid: int) -> bool:
    """
    Check if a process exists with the given pid
    """
    try:
        # Send a no-op signal to the process
        os.kill(pid, 0)
        # If it was successful, the pid exists
        return True
    except OSError:
        # If there was an error, the pid does not exist
        return False


def _cache_file(ctx) -> pathlib.Path:
    """
    Return the Path to the cache file used for this ctx
    """
    cache_file: pathlib.Path = (
        ctx.acct.cache_dir
        / "esm"
        / "local"
        / f"{ctx.acct.run_name}.{ctx.acct.serial_plugin}"
    )
    # Ensure that the parent directories exist
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    # Ensure that the file exists
    cache_file.touch()
    return cache_file
