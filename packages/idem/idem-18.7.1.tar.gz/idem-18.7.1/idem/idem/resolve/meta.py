from typing import Any
from typing import Dict
from typing import Set

KEYWORDS = ["META"]


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> Set[str]:
    """
    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    if "META" in state:
        raw_meta = state.pop("META")
        hub.idem.RUNS[name]["meta"]["SLS"][sls_ref] = raw_meta
    for id_ in state:
        if isinstance(state[id_], Dict):
            if "META" in state[id_]:
                ref = f"{sls_ref}.{id_}"
                raw_meta = state[id_].pop("META")
                hub.idem.RUNS[name]["meta"]["ID_DECS"][ref] = raw_meta
    return set()
