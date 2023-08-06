# Mapping of function refs that can be inverted and the
# corresponding function refs.
inversion_mapping = {
    "absent": "present",
    "present": "absent",
}


def apply(hub, low):
    """
    This function maps function ref to its complimentary
    value. For example, absent is converted to present,
    and present to absent.
    """

    for state in low:
        if state["fun"] in inversion_mapping:
            hub.log.debug(
                f"Inverting function ref from `{state['fun']}` to `{inversion_mapping[state['fun']]}` for state {state['__id__']}"
            )
            state["fun"] = inversion_mapping[state["fun"]]

        state["order"] *= -1

    return low
