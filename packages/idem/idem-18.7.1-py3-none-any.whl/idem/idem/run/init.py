import copy
from typing import List

import dict_tools.data as data


async def start(hub, name, pending_tags: List = None):
    """
    Called only after the named run has compiled low data. If no low data
    is present an exception will be raised
    pending_tags: list of state tags to re-run, if called from reconciliation,
                    otherwise all states are executed
    """
    if not hub.idem.RUNS[name].get("low"):
        raise ValueError(f"No low data for '{name}' in RUNS")
    ctx = data.NamespaceDict({"run_name": name, "test": hub.idem.RUNS[name]["test"]})

    rtime = hub.idem.RUNS[name]["runtime"]
    low = hub.idem.RUNS[name].get("low")
    # Fire an event with all the pre-rendered low-data for all states
    await hub.idem.event.put(
        profile="idem-low",
        body=low,
        tags={"ref": "idem.run.init.start", "type": "state-low-data"},
    )
    old_seq = {}
    old_seq_len = -1
    needs_post_low = True
    options = {"invert_state": hub.idem.RUNS[name]["invert_state"]}

    # If there are pending tags re-run only those (reconciliation)
    if pending_tags is None:
        running_copy = hub.idem.RUNS[name]["running"]
    else:
        running_copy = copy.deepcopy(hub.idem.RUNS[name]["running"])
        for tag in hub.idem.RUNS[name]["running"]:
            if tag in pending_tags:
                running_copy.pop(tag)

    while True:
        seq = hub.idem.req.seq.init.run(None, low, running_copy, options)
        if seq == old_seq:
            unmet_reqs = {chunk["tag"]: chunk["unmet"] for chunk in seq.values()}
            if len(unmet_reqs) == 0:
                raise Exception(f"Invalid syntax for '{name}'")
            raise Exception(f"No sequence changed for '{name}': {unmet_reqs}")
        await hub.idem.run[rtime].runtime(
            name,
            ctx,
            seq,
            low,
            running_copy,
            hub.idem.RUNS[name]["managed_state"],
        )

        render_data = await hub.idem.resolve.init.render(
            name,
            blocks=hub.idem.RUNS[name]["blocks"],
            sls_refs=hub.idem.RUNS[name]["sls_refs"],
            resolved=hub.idem.RUNS[name]["resolved"],
        )
        await hub.idem.sls_source.init.update(name, render_data)

        await hub.idem.state.compile(name)
        low = hub.idem.RUNS[name].get("low")
        await hub.idem.event.put(
            profile="idem-low",
            body=low,
            tags={"ref": "idem.run.init.start", "type": "state-low-data"},
        )
        if len(low) <= len(hub.idem.RUNS[name]["running"]):
            if hub.idem.RUNS[name]["post_low"] and needs_post_low:
                hub.idem.RUNS[name]["low"].extend(hub.idem.RUNS[name]["post_low"])
                needs_post_low = False
                continue
            else:
                break
        if len(seq) == old_seq_len:
            raise RecursionError(f"No progress made on '{name}', Recursive Requisite!")
        old_seq = seq
        old_seq_len = len(seq)
        # Check for any new, available blocks to render
