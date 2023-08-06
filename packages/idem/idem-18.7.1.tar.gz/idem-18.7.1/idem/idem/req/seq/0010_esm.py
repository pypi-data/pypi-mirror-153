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
    Process the requisites from ESM
    This function will check if the requisites for argument binding is present in this run
    If its present we do not do anything as requisites from the current run will already be added.
    If the requisite is not present in this run we check the ESM
    if the resource is already run previously, and it exists in ESM,
    we prepare the requisite and add to the resource requisites.

    This function will only add requisites to resources if they are not present in current run and exists in ESM
    This will not modify the current running resources nor this will send any events
    We only read a state from ESM to add to requisites. The state is not written back to ESM nor added to current run.
    """
    for ind, data in seq.items():
        if "arg_bind" not in data["chunk"]:
            continue
        chunk = data["chunk"]
        for rdef in chunk["arg_bind"]:
            if not isinstance(rdef, dict):
                data["errors"].append(f"{rdef} should be dictionary")
                continue
            state = next(iter(rdef))
            if isinstance(rdef[state], list):
                name_defs = rdef[state]
            else:
                name_defs = [{rdef[state]: []}]

            for name_def in name_defs:
                if not isinstance(name_def, dict):
                    data["errors"].append(f"{name_def} should be dictionary")
                    continue
                name = next(iter(name_def))
                args = name_def[name]
                r_chunks = hub.idem.tools.get_chunks(low, state, name)
                if not r_chunks:
                    # If r_chunks is not found in current run check if its present in ESM
                    hub.log.debug(
                        f"Requisite arg_bind {state}:{name} not found in current run. checking in ESM for arg_bind requisite"
                    )
                    r_chunks_from_esm = hub.tool.idem.esm.get_chunks_from_esm(
                        state, name
                    )
                    if not r_chunks_from_esm:
                        data["errors"].append(
                            f"Requisite arg_bind {state}:{name} not found"
                        )
                    for r_chunk in r_chunks_from_esm:
                        reqret_esm = hub.tool.idem.esm.update_running_from_esm(r_chunk)
                        r_tag = hub.idem.tools.gen_tag(r_chunk)
                        reqret = {
                            "req": "arg_bind",
                            "name": name,
                            "state": state,
                            "r_tag": r_tag,
                            "ret": reqret_esm,
                            "chunk": "r_chunk",
                            "args": args,
                        }
                        data["reqrets"].append(reqret)
    return seq
