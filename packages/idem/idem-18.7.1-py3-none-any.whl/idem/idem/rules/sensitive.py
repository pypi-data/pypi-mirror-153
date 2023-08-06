from typing import Any
from typing import Dict


def check(
    hub,
    name: str,
    ctx: Dict[str, Any],
    condition: Any,
    reqret: Dict[str, Any],
    chunk: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Make sensitive data from sls blocks to be available in Idem RUNS global variable.
    """
    if condition != "sensitive":
        return {"errors": [f'"{condition}" is not sensitive requisite.']}
    if "sensitive" in chunk:
        if not isinstance(chunk["sensitive"], list):
            return {
                "errors": [
                    f'sensitive requisite should contain a list of sensitive parameters, not {chunk["sensitive"]}'
                ]
            }
        tag = hub.idem.tools.gen_tag(chunk)
        if hub.idem.RUNS[name].get("sensitive"):
            hub.idem.RUNS[name]["sensitive"].update({tag: chunk["sensitive"]})
        else:
            hub.idem.RUNS[name]["sensitive"] = {tag: chunk["sensitive"]}
    return {"errors": []}
