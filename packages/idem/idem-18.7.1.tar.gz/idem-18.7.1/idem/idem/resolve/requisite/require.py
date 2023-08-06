def check(hub, name: str, value: str) -> bool:
    """
    Verify that states using a "require" shebang have had their requisite met

    :param hub:
    :param name: The state run name
    :param value: A string value to find in running states

    .. code-block:: yaml

        state_1:
          test.nop

        #!require:state_1
        state_2:
          test.nop:
    """
    for tag, data in hub.idem.RUNS[name]["running"].items():
        if data["name"] == value:
            return True
    return False
