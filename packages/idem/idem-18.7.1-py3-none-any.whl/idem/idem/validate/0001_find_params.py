import re

base_var_regex = r"[^\W0-9]\w*"  # Matches python identifier name
array_index = r"(\[(\d+)\])?"  # Matches array index

# Some example matches
#  ^^rg_name^^
#  ^^locations^^[0]
#  ^^lo_t10ns^^[19]
start_var = rf"\^\^({base_var_regex})\^\^({array_index})"

# Some example matches
#  ~~rg_name
#  ~~locations[0]
#  ~~lo_t10ns[19]
sub_var = rf"\.~~({base_var_regex})({array_index})"

# Compile the regular expressions
start_var_regex = re.compile(start_var)
sub_var_regex = re.compile(sub_var)

# Some match examples
#  ?? params.get('rg_name').get('your_rg', 'default') ?? ^^rg_name^^.~~your_rg ??
#  ?? params['locations'][0] ?? ^^locations^^[0] ??
#  ?? params['locations'][3].get('xstate') ?? ^^locations^^[3].~~xstate ??
extract_param_info_regex = re.compile(
    r"[?][?] .+?(?= [?][?]) [?][?] (.+?(?= [?][?])) [?][?]"
)


def _process_vars(params, input, pos):
    global start_var_regex

    # Here we are doing a regex match for strings like
    # ^^rg_name^^ or ^^locations^^[0]
    # That is a string starting and ending with double ^^,
    # with optional index. This gives us the parameter
    # name, and array index, if any.
    match = start_var_regex.search(input, pos)
    if match is None:
        return

    pos = _process_match(params, -1, match, input)
    _process_vars(params, input, pos)


def _fill_list(l, i):
    for i in range(len(l), i + 1):
        l.append(None)


# This function processes recursively any subparameters. For e.g.
# in the string   ^^rg_name^^.~~my_rg.~~abc   this function will
# process    .~~my_rg.~~abc
def _process_dot_vars(params, parent_index, param_name, index, input, pos):
    global sub_var_regex

    # Matchs a string like    ~~my_rg[3]    where array index
    # is optional.
    match = sub_var_regex.match(input, pos)

    # No match means we don't have sub parameter to process. For e.g.
    # in case of string being    ^^rg_name^^.~~my_rg.~~abc   we
    # have processed till abc and there is nothing to process further.
    if match is None:
        if isinstance(params, list):
            _fill_list(params, index)
            params[parent_index] = {param_name: ""}
        else:
            if param_name not in params:
                if index < 0:
                    params[param_name] = {}
                else:
                    params[param_name] = []
                    _fill_list(params[param_name], index)
            if index < 0:
                params[param_name] = ""
            else:
                params[param_name][index] = ""
        return pos

    if isinstance(params, list):
        if index < 0:
            o = {}
        else:
            o = []
            _fill_list(o, index)
        params[parent_index] = {param_name: o}
        return _process_match(o, index, match, input)
    else:
        if param_name not in params:
            if index < 0:
                params[param_name] = {}
            else:
                params[param_name] = []
                _fill_list(params[param_name], index)
        else:
            if index >= 0:
                _fill_list(params[param_name], index)

    return _process_match(params[param_name], index, match, input)


def _process_match(params, parent_index, match, input):
    groups = match.groups()
    param_name = groups[0]

    # A index is matched, which means we are dealing with array
    if len(groups) == 4 and groups[2] is not None:
        return _process_dot_vars(
            params, parent_index, param_name, int(groups[3]), input, match.end()
        )
    else:  # we are dealing with something that is not an array
        return _process_dot_vars(
            params, parent_index, param_name, -1, input, match.end()
        )


def _iterate_over_state(state, var):
    if isinstance(var, dict):
        for key, value in var.items():
            yield from _iterate_over_state(state, key)
            yield from _iterate_over_state(state, value)
    elif isinstance(var, list):
        for item in var:
            yield from _iterate_over_state(state, item)
    else:
        yield (state, var)


def _iterate_over(states):
    for state, value in states.items():
        sls = value["__sls__"]
        yield (f"{sls}.{state}", state)
        yield from _iterate_over_state(f"{sls}.{state}", value)


def _fill_list(l, i):
    for i in range(len(l), i + 1):
        l.append(None)


def stage(hub, name):
    all_params = {}
    # Here we iterate over all the strings in high data. Subsequently
    # in the _process_vars we process each such string, identifying
    # parameters (if any), in the context of a state.
    for state, value in _iterate_over(hub.idem.RUNS[name]["high"]):

        if not isinstance(value, str):
            continue

        if state not in all_params:
            all_params[state] = {}

        for param_info in extract_param_info_regex.findall(value):
            _process_vars(all_params[state], param_info, 0)

    hub.idem.RUNS[name]["parameters"] = {
        "GLOBAL": hub.idem.RUNS[name]["params"].params(),
        "ID_DECS": all_params,
    }
