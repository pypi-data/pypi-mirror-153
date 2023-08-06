from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set

KEYWORDS = ["order"]


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> Set[str]:
    """
    Take a state and apply the iorder system

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    for id_ in hub.idem.resolve.init.iter(state):
        if isinstance(state[id_], str):
            continue
        if not isinstance(state[id_], Iterable):
            continue
        for s_dec in state[id_]:
            if not isinstance(s_dec, str):
                # PyDSL OrderedDict?
                continue

            if not isinstance(state[id_], Dict):
                # Include's or excludes as lists?
                continue
            if not isinstance(state[id_][s_dec], List):
                # Bad syntax, let the verify seq pick it up later on
                continue

            found = False
            if s_dec.startswith("_"):
                continue

            for arg in state[id_][s_dec]:
                if isinstance(arg, Dict):
                    if len(arg) > 0:
                        if next(iter(arg)) == "order":
                            found = True
            if not found:
                if not isinstance(state[id_][s_dec], List):
                    # quite certainly a syntax error, managed elsewhere
                    continue

                state[id_][s_dec].append({"order": hub.idem.RUNS[name]["iorder"]})
                hub.idem.RUNS[name]["iorder"] += 1
    return set()
