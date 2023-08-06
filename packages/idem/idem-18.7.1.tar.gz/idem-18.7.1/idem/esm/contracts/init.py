from typing import Any
from typing import Dict


async def sig_enter(hub, ctx):
    """
    :param hub:
    :param ctx:

    Enter the context of the enforced state manager
    Only one instance of a state run will be running for the given context.
    This function enters the context and locks the run.

    The return of this function will be passed by idem to the "handle" parameter of the exit function
    """


async def sig_exit_(hub, ctx, handle, exception: Exception):
    """
    :param hub:
    :param ctx:
    :param handle: The output of the corresponding "enter" function
    :param exception: Any exception that was raised while inside the context manager or None

    Exit the context of the enforced state manager
    """


async def sig_get_state(hub, ctx) -> Dict[str, Any]:
    """
    :param hub:
    :param ctx:

    Use the information provided in ctx.acct to retrieve the enforced managed state.
    Return it as a python dictionary.
    """


async def sig_set_state(hub, ctx, state: Dict[str, Any]):
    """
    :param hub:
    :param ctx:

    Use the information provided in ctx.acct to upload/override the enforced managed state with "state".
    """
