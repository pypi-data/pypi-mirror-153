from typing import Any
from typing import Dict


async def loop(
    hub,
    pending_plugin: str,
    name: str,
    apply_kwargs: Dict[str, Any],
):
    # This is the default reconciler
    # Reconciliation loop is skipped for backward compatibility
    return {
        "re_runs_count": 0,
        "require_re_run": False,
    }
