from typing import Any
from typing import Dict
from typing import List


def check(hub, rlist: List[Dict[str, Any]]) -> List[str]:
    """
    Chek the resolve list from the requisite systems and return errors from all
    errored requisites
    """
    errors = []
    for rdat in rlist:
        errors.extend(rdat.get("errors", []))
    return errors
