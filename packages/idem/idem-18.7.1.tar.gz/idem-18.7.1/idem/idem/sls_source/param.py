from typing import Dict
from typing import List


def get_refs(hub, *, sources: List[str], refs: List[str]) -> Dict[str, List[str]]:
    """
    Determine where the param sls sources are

    :param hub:
    :param sources: sls-sources or params-sources
    :param refs: References to sls within the given sources
    """
    ret = {"param_sources": [], "params": []}

    if not refs:
        return ret

    for ref in refs:
        hub.idem.sls_source.init.process(ret["param_sources"], ret["params"], ref)

    ret["param_sources"].extend(sources)

    return ret


async def gather(hub, name: str, *sls):
    """
    Gather the named param references into the RUNS structure

    :param hub:
    :param name: The state run name
    :param sls: sls locations within sources
    """
    sources = hub.idem.RUNS[name]["param_sources"]
    gather_data = await hub.idem.resolve.init.gather(name, *sls, sources=sources)
    if gather_data["errors"]:
        hub.idem.RUNS[name]["errors"] = gather_data["errors"]
        return

    for state in gather_data["state"].values():
        for id_ in hub.idem.resolve.init.iter(state):
            # In case of params_processing being true, such as when we are doing
            # parameter processing only: we will just read the key and value pairs and add
            # to hub.idem.RUNS[name]["params"] dict. Then we can access the parameter value
            # as {{ params.get('foo') }}
            hub.idem.RUNS[name]["params"][id_] = (
                state[id_] if state[id_] is not None else "__PYTHON_NONE__"
            )
