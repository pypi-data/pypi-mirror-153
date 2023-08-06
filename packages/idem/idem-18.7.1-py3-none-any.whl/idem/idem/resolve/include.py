from typing import Any
from typing import Dict
from typing import List
from typing import re
from typing import Set

KEYWORDS = ["include"]


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> Set[str]:
    """
    Parse through the includes and download not-yet-resolved includes

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    unresolved = set()
    include = state.pop("include", [])
    if not isinstance(include, List):
        hub.idem.RUNS[name]["errors"].append(
            f"Include Declaration in SLS {sls_ref} is not formed as a list but as a {type(include)}"
        )
        return unresolved

    for inc_sls in include:
        if inc_sls.startswith("."):
            match = re.match(r"^(\.+)(.*)$", inc_sls)
            if match:
                levels, include = match.groups()
            else:
                hub.idem.RUNS[name]["errors"].append(
                    f'Badly formatted include {inc_sls} found in SLS "{sls_ref}"'
                )
                continue
            level_count = len(levels)
            p_comps = sls_ref.split(".")
            if cfn.endswith("/init.sls"):
                p_comps.append("init")
            if level_count > len(p_comps):
                hub.idem.RUNS[name]["errors"].append(
                    f'Attempted relative include of "{inc_sls}" within SLS {sls_ref} goes beyond top level package'
                )
                continue
            inc_sls = ".".join(p_comps[:-level_count] + [include])
            unresolved.add(inc_sls)
        if inc_sls not in resolved:
            unresolved.add(inc_sls)
    return unresolved
