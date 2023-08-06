from typing import Any
from typing import Dict
from typing import List
from typing import Set

KEYWORDS = ["exclude", "__exclude__"]


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> Set[str]:
    """
    Resolve any exclude statements

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    if "exclude" not in state:
        return set()
    exc = state.pop("exclude", [])
    if not isinstance(exc, List):
        hub.idem.RUNS[name]["errors"].append(
            f"Exclude Declaration in SLS {sls_ref} is not formed as a list"
        )
    if exc:
        state.setdefault("__exclude__", []).extend(exc)

    return set()
