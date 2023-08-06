from typing import Any
from typing import Dict
from typing import Set


async def sig_apply(
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
