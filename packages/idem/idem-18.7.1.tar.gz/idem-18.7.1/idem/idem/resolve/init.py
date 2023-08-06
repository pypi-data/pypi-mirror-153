"""
The sls source is used to gather sls files, render them and return the initial
phase 1 highdata. This involves translating sls references into file paths,
downloading those sls files and then rendering them.

Once an sls file is rendered the include statements are resolved as well.
"""
import warnings
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Set


__func_alias__ = {"iter_": "iter"}


def __init__(hub):
    hub.idem.resolve.init.HARD_FAIL = False


async def gather(hub, name: str, *sls, sources: List[str]) -> Dict[str, Any]:
    """
    Gather the named sls references

    :param hub:
    :param name: The state run name
    :param sls: sls locations within sources
    :param sources: sls-sources or params-sources
    """
    ret = {
        "state": {},
        "sls_refs": {},
        "blocks": {},
        "resolved": {},
        "errors": [],
        "rendered": {},
    }

    block_data = await hub.idem.resolve.init.get_blocks(name, sls, sources)
    ret.update(block_data)
    if ret["errors"]:
        return ret

    render_data = await hub.idem.resolve.init.render(
        name=name,
        blocks=block_data["blocks"],
        sls_refs=block_data["sls_refs"],
        resolved=block_data["resolved"],
    )
    unresolved_refs = render_data.pop("unresolved_refs", None)
    ret.update(render_data)

    if unresolved_refs:
        recurse = await hub.idem.resolve.init.gather(
            name, *unresolved_refs, sources=sources
        )
        ret["state"].update(recurse["state"])
        ret["rendered"].update(recurse["rendered"])
        ret["sls_refs"].update(recurse["sls_refs"])
        ret["blocks"].update(recurse["blocks"])
        ret["resolved"].update(recurse["resolved"])
        ret["errors"].extend(recurse["errors"])

    return ret


async def get_blocks(
    hub, name: str, sls: List[str], sources: List[str]
) -> Dict[str, Any]:
    """
    Returns the data from the SLS file if it can be found

    :param hub:
    :param name: The state run name
    :param sls: sls locations within sources
    :param sources: sls-sources or params-sources
    """
    ret = {"blocks": {}, "sls_refs": {}, "resolved": set(), "errors": []}
    for sls_ref in sls:
        cfn = None
        file_name = None
        try:
            file_name, cfn = await hub.idem.get.ref(name, sls_ref, sources)
        except Exception as e:
            msg = f"Error while collecting blocks: {e.__class__.__name__}: {e}"
            hub.log.debug(msg)
            ret["errors"].append(msg)
            if hub.idem.resolve.init.HARD_FAIL:
                raise
        if not cfn:
            msg = f"SLS ref '{sls_ref}' did not resolve from sources"
            hub.log.debug(msg)
            ret["errors"].append(msg)
            return ret

        blocks = hub.rend.init.blocks(fn=file_name, content=cfn)
        ret["blocks"][sls_ref] = blocks
        ret["sls_refs"][sls_ref] = file_name
        ret["resolved"].add(sls_ref)

    return ret


async def render(
    hub, name: str, blocks: Dict[str, Any], sls_refs: Dict[str, str], resolved: Set[str]
) -> Dict[str, Any]:
    """
    Pop the available blocks and render them if they have satisfied requisites

    :param hub:
    :param name: The state run name
    :param blocks: A mapping of sls refs to raw byte data representing a state
    :param sls_refs: References to sls within the given sources
    :param resolved: The names of SLSs that have been resolved
    """
    ret = {"rendered": {}, "state": {}, "unresolved_refs": set()}
    for sls_ref, block in blocks.items():
        ret["state"][sls_ref] = {}
        cfn = sls_refs[sls_ref]
        for bname, chunk in block.items():
            clear = True
            for key, val in chunk.get("keys", {}).items():
                # If there is a render requisite plugin for this key then run its "check" method
                if key in hub.idem.resolve.requisite:
                    clear &= hub.idem.resolve.requisite[key].check(name, val)
                else:
                    clear = False

            if not clear:
                continue

            state = await hub.rend.init.parse_bytes(
                chunk,
                hub.idem.RUNS[name]["render"],
                params=hub.idem.RUNS[name]["params"],
            )
            ret["rendered"][sls_ref] = bname
            if state is None:
                # if a rendered sls file turns to be empty
                warnings.warn(
                    f"SLS ref {sls_ref} is not resolved to any state.", RuntimeWarning
                )
                hub.log.warning(f"SLS ref {sls_ref} is not resolved to any state.")
                continue
            # Process the state through the resolve plugins
            unresolved_refs = await hub.idem.resolve.init.apply(
                name=name,
                state=state,
                sls_ref=sls_ref,
                cfn=cfn,
                resolved=resolved,
            )
            ret["unresolved_refs"].update(unresolved_refs)
            ret["state"][sls_ref].update(state)

    for sls_ref, bname in ret["rendered"].items():
        blocks[sls_ref].pop(bname, None)
    return ret


async def apply(
    hub,
    name: str,
    state: Dict[str, Any],
    sls_ref: str,
    cfn: str,
    resolved: Set[str],
) -> Set[str]:
    """
    Introduce the raw state into the running dataset

    :param hub:
    :param name: The state run name
    :param state: A rendered block from the sls
    :param sls_ref: A reference to another sls within the given sources
    :param cfn: The cache file name, or the location of sls within the given sources
    :param resolved: a set of refs that have already been resolved
    """
    unresolved_refs = set()
    if not isinstance(state, Dict):
        hub.idem.RUNS[name]["errors"].append(
            f"SLS {sls_ref} is not formed as a dict but as a {type(state)}"
        )
        return unresolved_refs

    for top_level_resolver in hub.idem.resolve._loaded:
        if top_level_resolver == "init":
            # We are currently in resolve.init.apply, avoid infinite recursion
            continue
        ret = await hub.idem.resolve[top_level_resolver].apply(
            name=name,
            state=state,
            sls_ref=sls_ref,
            cfn=cfn,
            resolved=resolved,
        )
        unresolved_refs.update(ret)
    return unresolved_refs


def iter_(hub, state: Dict[str, Any]) -> Generator:
    """
    iterate over a state, skipping known keywords

    :param hub:
    :param state: A rendered block from the sls
    """
    for id_ in state:
        if any(id_ in getattr(plugin, "KEYWORDS", []) for plugin in hub.idem.resolve):
            continue
        yield id_
