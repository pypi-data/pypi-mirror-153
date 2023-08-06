import datetime
from typing import Any
from typing import Dict


def get_chunks_from_esm(hub, resource_type, name):
    rets = []
    run_name = hub.idem.RUN_NAME
    # Get the current state
    esm_state: Dict[str, Any] = dict(hub.idem.RUNS[run_name]["managed_state"])

    for resource_in_state in esm_state:
        chunk = convert_state_data_to_chunk(
            esm_state[resource_in_state], resource_type, name
        )
        esm_tag = hub.idem.managed.gen_tag(chunk)
        if resource_in_state == esm_tag:
            chunk["resource_state"] = esm_state[resource_in_state]
            rets.append(chunk)
    return rets


def convert_state_data_to_chunk(state_data, resource_type, name):
    chunk = state_data
    chunk["state"] = resource_type
    chunk["__id__"] = name
    chunk["fun"] = "present"
    if "name" not in chunk:
        chunk["name"] = name

    return chunk


def update_running_from_esm(hub, chunk):
    tag = hub.idem.tools.gen_tag(chunk)
    esm_tag = hub.idem.managed.gen_tag(chunk)
    start_time = datetime.datetime.now()
    run_num = hub.idem.RUNS[hub.idem.RUN_NAME]["run_num"]
    return {
        "tag": tag,
        "name": chunk["name"],
        "changes": {},
        "new_state": chunk["resource_state"],
        "old_state": chunk["resource_state"],
        "comment": (),
        "result": True,
        "esm_tag": esm_tag,
        "__run_num": run_num,
        "start_time": str(start_time),
        "total_seconds": 0,
    }
