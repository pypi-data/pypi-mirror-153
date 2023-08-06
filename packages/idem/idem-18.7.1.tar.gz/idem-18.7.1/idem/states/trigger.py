import uuid
from collections import ChainMap
from typing import List

import dict_tools.differ as differ


async def build(hub, ctx, name: str, triggers: List = None, resource_id: str = None):
    """
    A state to represent a trigger. A trigger will be a dictionary of key-values,
    which when changed, can be used to trigger another state. The dictionary can
    hold values that are user defined e.g. last_run_id: {{ range(1, 51) | random }}
    or it can hold values from the output of a different state as supported in arg
    binding e.g. user_name: ${aws.iam.user:aws_iam_user.extension-jenkins:user_name}.

    Note: Triggers dictionary can hold values which won't change over the course
    of multiple execution. The example below is a constantly changing trigger state.


    :param hub:
    :param ctx:
    :param name: The name of the state
    :param resource_id: The resource_id to represent this trigger in ESM. Its an internal id to track
                 whether this resource has run or not.
    :param triggers: The dictionary to hold key-value pairs

    .. code-block:: sls

        always-changes-and-succeeds:
          test.succeed_with_changes:
            - name: foo

        always-changes-trigger:
            trigger.build:
                - triggers:
                     - last_run_id: {{ range(1, 51) | random }}
                     - comment: ${test:always-changes-and-succeeds:testing}

        watch_changes:
          test.nop:
            - onchanges:
              - trigger: always-changes-trigger

    In the example above , Only when there are `changes` when the aws.trigger.build is run , the `local-command` state runs.
    """
    result = dict(comment=(), old_state={}, new_state={}, name=name, result=True)
    before = None

    if resource_id:
        before = ctx.get("old_state")
    else:
        resource_id = "idem-trigger-" + str(uuid.uuid4())
    if before:
        result["old_state"] = before

    if triggers:
        triggers = dict(ChainMap(*triggers))

    result["new_state"] = dict(triggers=triggers, resource_id=resource_id)

    try:
        result["changes"] = differ.deep_diff(
            result["old_state"].get("triggers"), result["new_state"].get("triggers")
        )

        if result["changes"]:
            result["comment"] = (f"Trigger '{name}' built with changes",)
        else:
            result["comment"] = (f"Trigger '{name}' built with no changes",)
    except Exception as e:
        result["result"] = False
        result["comment"] = result["comment"] + (str(e),)

    return result
