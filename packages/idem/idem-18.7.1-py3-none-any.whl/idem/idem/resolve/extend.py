from typing import Any
from typing import Dict
from typing import Set

KEYWORDS = ["extend", "__extend__"]


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> Set[str]:
    """
    Resolve the extend statement

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    if "extend" not in state:
        return set()
    ext = state.pop("extend", {})
    if not isinstance(ext, Dict):
        hub.idem.RUNS[name]["errors"].append(
            f'Extension value in SLS "{sls_ref}" is not a dictionary'
        )
        return
    for id_ in ext:
        if not isinstance(ext[id_], Dict):
            hub.idem.RUNS[name]["errors"].append(
                f'Extension ID "{id_}" in SLS "{sls_ref}" is not a dictionary'
            )
            continue
        if "__sls__" not in ext[id_]:
            ext[id_]["__sls__"] = sls_ref
        # if '__env__' not in ext[id_]:
        #    ext[id_]['__env__'] = saltenv
        for key in list(ext[id_]):
            if key.startswith("_"):
                continue
            if not isinstance(ext[id_][key], list):
                continue
            if "." in key:
                comps = key.split(".")
                ext[id_][comps[0]] = ext[id_].pop(key)
                ext[id_][comps[0]].append(comps[1])
    if ext:
        state.setdefault("__extend__", []).append(ext)

    return set()
