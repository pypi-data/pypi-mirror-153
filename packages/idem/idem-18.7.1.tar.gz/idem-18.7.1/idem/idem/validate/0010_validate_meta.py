def _validate_extracted_params_recursively(state, extracted_params, meta, dot):
    if isinstance(extracted_params, dict):
        for key, value in extracted_params.items():
            if meta is None or key not in meta:
                yield (state, f"{dot}{key}")
                next_meta = None
            elif meta[key] is not None and "properties" in meta[key]:
                next_meta = meta[key]["properties"]
            else:
                next_meta = None

            for state, param in _validate_extracted_params_recursively(
                state, value, next_meta, "."
            ):
                yield (state, f"{dot}{key}{param}")
    elif isinstance(extracted_params, list):
        for item in extracted_params:
            if item is None or isinstance(item, str):
                continue

            if meta is None or key not in meta:
                next_meta = None
            elif meta[key] is not None and "items" in meta[key]:
                next_meta = meta[key]["items"]
            else:
                next_meta = None

            for state, param in _validate_extracted_params_recursively(
                state, item, next_meta, "."
            ):
                yield (state, f"[]{param}")


def _validate_extracted_params(parameters, meta):
    for state, extracted_params in parameters.items():
        if meta is None or state not in meta or "params" not in meta[state]:
            state_meta = None
        else:
            state_meta = meta[state]["params"]

        for state, param in _validate_extracted_params_recursively(
            state, extracted_params, state_meta, ""
        ):
            yield (state, param)


def stage(hub, name):
    hub.idem.RUNS[name]["warnings"] = {"GLOBAL": {}, "ID_DECS": {}}

    if (
        "parameters" not in hub.idem.RUNS[name]
        or "ID_DECS" not in hub.idem.RUNS[name]["parameters"]
    ):
        return

    if (
        "meta" not in hub.idem.RUNS[name]
        or "ID_DECS" not in hub.idem.RUNS[name]["meta"]
    ):
        all_meta = None
    else:
        all_meta = hub.idem.RUNS[name]["meta"]["ID_DECS"]

    all_warnings = {}

    for state, missing_param in _validate_extracted_params(
        hub.idem.RUNS[name]["parameters"]["ID_DECS"], all_meta
    ):
        if state not in all_warnings:
            all_warnings[state] = {"params_meta_missing": []}
        all_warnings[state]["params_meta_missing"].append(missing_param)

    for state, warnings in all_warnings.items():
        hub.idem.RUNS[name]["warnings"]["ID_DECS"][state] = warnings
