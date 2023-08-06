import re

arg_reference_regex_pattern = re.compile(r"\${[^\${}]+}")


def reconcile(hub, high):
    """
    Parse high data and convert argument binding references like ${cloud:state:property_path} to arg_bind requisites

    ex:
    state1:
     cloud1.state_def:
      - parameters:
        arg1: ${cloud2:state2:property_path}
      - arg_bind:
       - cloud2:
        - state2:
          - property_path: arg1
    """
    errors = []
    # TODO: Add debug logging
    # Iterate over yield arguments and check if the argument value contains references
    for id_, body, state, run, arg_key, arg_value in hub.idem.tools.iter_high_leaf_args(
        high
    ):
        if (
            arg_value
            and isinstance(arg_value, str)
            and arg_reference_regex_pattern.search(arg_value)
        ):
            for arg_ref in arg_reference_regex_pattern.findall(arg_value):
                ref_chain_list = str(arg_ref[2 : arg_ref.index("}")]).split(":")

                if len(ref_chain_list) < 3:
                    # TODO: Find out why this doesn't fail the execution
                    errors.append(
                        f'Argument reference {arg_ref} for state "{id_}" is not properly formatted. '
                        f"Argument reference format is ${{referenced_cloud:referenced_state:argument_path}}."
                    )
                    continue

                ref_cloud = ref_chain_list.pop(0)
                ref_state = ref_chain_list.pop(0)

                # This code is executed for every idem iteration.
                # Make sure, arg_bind requisites don't get duplicated.
                arg_bind_req = _get_or_add_arg(high.get(id_).get(state), "arg_bind", [])
                arg_bind_cloud = _get_or_add_arg(arg_bind_req, ref_cloud, [])
                arg_bind_state = _get_or_add_arg(arg_bind_cloud, ref_state, [])
                _get_or_add_arg(arg_bind_state, ":".join(ref_chain_list), arg_key)

    return high, errors


def _get_or_add_arg(arg_list, arg_name, arg_value):
    for arg in arg_list:
        # Expected format is a list of dictionaries
        if isinstance(arg, dict) and arg.get(arg_name, None):
            # The same referenced state property can be bound to multiple arguments of the current state.
            # If the argument list contains expected argument and argument value is string,
            # make sure it is set to the argument value, otherwise add new argument for the value.
            if isinstance(arg_value, str) and isinstance(arg.get(arg_name), str):
                if arg.get(arg_name) == arg_value:
                    return arg.get(arg_name)
            else:
                return arg.get(arg_name)

    arg_state = {arg_name: arg_value}
    arg_list.append(arg_state)
    return arg_state.get(arg_name)
