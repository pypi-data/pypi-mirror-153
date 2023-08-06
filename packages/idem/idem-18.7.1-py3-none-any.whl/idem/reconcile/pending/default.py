def is_pending(hub, ret: dict, state: str = None) -> bool:
    """
    Default implementation of pending plugin
    Pending plugin returns 'True' when the state is still 'pending'
    and reconciliation is required.
    This implementation requires reconciliation until 'result' is 'True'
    and there are no 'changes'.

    :param hub: The hub
    :param ret: (dict) Returned structure of a run
    :param state: (Text, Optional) The name of the state
    :return: bool
    """
    return not ret["result"] is True or bool(ret["changes"])
