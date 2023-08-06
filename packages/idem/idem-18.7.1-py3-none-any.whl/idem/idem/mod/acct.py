from typing import Any
from typing import Dict

from dict_tools.data import SafeNamespaceDict


async def modify(hub, name: str, chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check the state containing the target func and call the mod_creds
    function if present. Therefore gathering the list of creds systems
    to use
    """
    run_name = chunk["ctx"]["run_name"]
    state = chunk["state"].split(".")[0]
    subs = []
    if hasattr(hub, f"states.{state}.ACCT"):
        subs = getattr(hub, f"states.{state}.ACCT")
    elif hasattr(hub, f"{state}.ACCT"):
        subs = getattr(hub, f"{state}.ACCT")
    elif hasattr(hub, f"exec.{state}.ACCT"):
        subs = getattr(hub, f"exec.{state}.ACCT")
    elif hasattr(hub, f"tool.{state}.ACCT"):
        subs = getattr(hub, f"tool.{state}.ACCT")
    hub.log.debug(f"Loaded acct from subs: {subs}")

    # Get the acct_profile that is being used from the chunk and fallback to the acct_profile in the RUN
    profile = chunk.pop("acct_profile", hub.idem.RUNS[run_name]["acct_profile"])

    # Some idem tests or projects that call idem from pure python specify a sub other than "states" for state modules
    # Check for state modules being in alternate locations but default to "states"
    sub = "states"
    for sub in hub.idem.RUNS[run_name]["subs"]:
        try:
            # Get the keyword arguments of the state function that will be called
            function_parameters = hub[sub][chunk["state"]][
                chunk["fun"]
            ].signature.parameters
            break
        except AttributeError:
            ...
    else:
        function_parameters = {}

    # If the acct_profile was in the function parameters, then add back the acct_profile that is being used
    if "acct_profile" in function_parameters:
        chunk["acct_profile"] = profile

    # If acct_data was in the function parameters and in the chunk, then return the chunk without constructing ctx.acct
    # The function is going to decide what to do with the acct_data
    if "acct_data" in function_parameters and chunk.get("acct_data"):
        # Allow acct_data in the function parameters, but protect it from being exposed in events and logs
        chunk["acct_data"] = SafeNamespaceDict(chunk["acct_data"])
        return chunk

    # Retrieve the acct_data from the state chunk and fallback to the acct_data from the RUN
    acct_data = chunk.pop("acct_data", hub.idem.RUNS[run_name]["acct_data"])

    # Validate that the specified acct_profile is specified is within the profiles
    try:
        if hub[sub][state] and hub[sub][state].ACCT:
            if (
                profile
                and acct_data
                and acct_data["profiles"].get(state)
                and profile not in acct_data["profiles"][state]
            ):
                msg = f"Could not find profile '{profile}' in profiles: {acct_data['profiles'][state].keys()}"
                hub.log.error(msg)
                raise Exception(msg)
    # hub.states[state].ACCT may not exists
    except AttributeError:
        ...

    hub.log.debug(f"Loaded profile: {profile}")
    chunk["ctx"]["acct"] = await hub.acct.init.gather(
        subs,
        profile,
        profiles=acct_data.get("profiles"),
    )
    return chunk
