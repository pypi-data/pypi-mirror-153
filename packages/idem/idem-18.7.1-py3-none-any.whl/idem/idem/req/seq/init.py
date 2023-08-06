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
    Process the multi stage routine to determine the current requisite sequence
    """
    for seq_plugin in sorted(hub.idem.req.seq._loaded.keys()):
        if seq_plugin == "init":
            continue
        seq = hub.idem.req.seq[seq_plugin].run(seq, low, running, options)
    return seq
