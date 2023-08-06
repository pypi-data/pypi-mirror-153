from typing import Any
from typing import Dict


def run(
    hub,
    seq: Dict[int, Dict[str, Any]],
    low: Dict[str, Any],
    running: Dict[str, Any],
    options: Dict[str, Any],
) -> Dict[int, Dict[str, Any]]:
    """
    Invert the requisites. If invert command line parameter is specified, requisites
    need to be reverted as well since order of execution is exact reverse in case of
    present and absent function references. The following code achieves the same.
    """
    if "invert_state" not in options or not options["invert_state"]:
        hub.log.debug("Skipping invert as not enabled")
        return seq

    tag_state_map = {}
    for ind, data in seq.items():
        tag_state_map[data["tag"]] = ind

    unmets = {}
    for data in seq.values():
        if "unmet" not in data:
            continue

        tag = data["tag"]
        for unmet in data["unmet"]:
            ind = tag_state_map[unmet]
            if ind not in unmets:
                unmets[ind] = set()
            unmets[ind].add(tag)
        data["unmet"] = set()

    for ind, unmet in unmets.items():
        seq[ind]["unmet"] = unmet

    return seq
