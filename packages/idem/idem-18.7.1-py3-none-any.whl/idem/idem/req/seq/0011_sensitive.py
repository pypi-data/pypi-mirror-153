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
    Process the sensitive requisite.
    """
    for ind, data in seq.items():
        if "sensitive" not in data["chunk"]:
            continue
        chunk = data["chunk"]
        r_tag = hub.idem.tools.gen_tag(chunk)
        reqret = {
            "r_tag": r_tag,
            "req": "sensitive",
            "ret": {},
        }
        data["reqrets"].append(reqret)

    return seq
