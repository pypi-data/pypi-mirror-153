from typing import Dict
from typing import List


def sig_get_refs(hub, *, sources: List[str], refs: List[str]) -> Dict[str, List[str]]:
    """
    :param hub:
    :param sources: sls-sources or params-sources
    :param refs: References to sls within the given sources
    """


async def sig_gather(hub, name: str, *sls):
    """
    :param hub:
    :param name: The state run name
    :param sls: sls locations within sources
    """
