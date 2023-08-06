import re

# Some match examples
#  ?? params.get('rg_name').get('your_rg', 'default') ?? ^^rg_name^^.~~your_rg ??
#  ?? params['locations'][0] ?? ^^locations^^[0] ??
#  ?? params['locations'][3].get('xstate') ?? ^^locations^^[3].~~xstate ??
regex = re.compile(r"[?][?] (.+?(?= [?][?])) [?][?] .+?(?= [?][?]) [?][?]")


def _remap(value):
    return regex.sub(r"{{ \1 }}", value)


def _remap_recursively(var):
    if isinstance(var, dict):
        result = {}
        for key, value in var.items():
            result[_remap(key)] = _remap_recursively(value)
        return result
    elif isinstance(var, list):
        result = []
        for item in var:
            result.append(_remap_recursively(item))
        return result
    elif isinstance(var, str):
        return _remap(var)
    else:
        return var


def _remap_run_data(run_data, keys):
    for key in keys:
        run_data[key] = _remap_recursively(run_data[key])


def stage(hub, name):
    _remap_run_data(
        hub.idem.RUNS[name], ["high", "low", "meta", "parameters", "warnings"]
    )
