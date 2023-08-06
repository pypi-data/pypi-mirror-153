def stage(hub, name: str):
    """
    Take the highdata and convert argument references to arg_bind requisites
    """
    high, errors = hub.idem.ccomps.arg_bind.reconcile(hub.idem.RUNS[name]["high"])
    hub.idem.RUNS[name]["high"] = high
    hub.idem.RUNS[name]["errors"] = errors
