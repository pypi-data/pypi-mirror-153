from typing import Any
from typing import Dict
from typing import List


def check(hub, rlist: List[Dict[str, Any]]) -> List[str]:
    """
    Check if any of the required list passes. If a single check passes then
    all is well, only return the errors is ALL FAIL
    """
    errors = []
    good = False
    for rdat in rlist:
        err = rdat.get("errors", [])
        if not err:
            good = True
        errors.extend(rdat.get("errors", []))
    if good:
        return []
    return errors
