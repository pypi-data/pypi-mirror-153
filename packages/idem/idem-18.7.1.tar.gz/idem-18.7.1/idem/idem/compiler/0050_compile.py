def stage(hub, name: str):
    """
    Apply the exclude value
    """
    low = hub.idem.ccomps.low.compile(
        hub.idem.RUNS[name]["high"], hub.idem.RUNS[name]["add_low"]
    )
    hub.idem.RUNS[name]["low"] = low
