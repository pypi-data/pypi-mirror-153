from typing import Any
from typing import Dict
from typing import List

DEFAULT_RESOLVER = "all"


def resolve(hub, rdats: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """
    Given the dict of requisite data sets, determine if the defined
    requisites passed. This allows for requisites to be defined
    as requiring, all, some, one, or none of the required states to
    pass
    """
    errors = []
    for req, requisite_list in rdats.items():
        requisite_map = hub.idem.RMAP[req]
        resolver = requisite_map.get("resolver", DEFAULT_RESOLVER)
        new_errors = hub.idem.resolver[resolver].check(requisite_list)
        errors.extend(new_errors)
    return errors


def check(hub, rlist: List[Dict[str, Any]]) -> List[str]:
    return []
