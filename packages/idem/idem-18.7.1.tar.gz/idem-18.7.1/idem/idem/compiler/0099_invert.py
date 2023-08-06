def stage(hub, name: str):
    """
    Invert present absent states if required
    """

    if (
        "invert_state" not in hub.idem.RUNS[name]
        or not hub.idem.RUNS[name]["invert_state"]
    ):
        hub.log.debug("Skipping invert as not enabled")
        return

    low = hub.idem.ccomps.invert.apply(hub.idem.RUNS[name]["low"])
    hub.idem.RUNS[name]["low"] = low
