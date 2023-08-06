import re
from typing import Any
from typing import Dict


def check(
    hub,
    name: str,
    ctx: Dict[str, Any],
    condition: Any,
    reqret: Dict[str, Any],
    chunk: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Parse argument binding reference and update the chunk argument with the requisite value.
    For example:
    - arg_bind:
        - cloud:
            - referenced_state:
                - referenced_state_property: this_state_property
    """
    if condition != "arg_bind":
        return {"errors": [f'"{condition}" is not a supported arg resolver.']}

    if not isinstance(reqret.get("args", {}), list):
        return {"errors": [f'"{condition}" is not in a supported format.']}

    # TODO: Add debug logging
    # Iterate over args of the "arg_bind" requisite, each arg is an argument binding
    for req_def in reqret.get("args", []):
        # Validate that requisite definition is a key/value pair,
        # where the key is the referenced state argument path
        # and the value is the current state argument path
        if not isinstance(req_def, dict):
            return {"errors": [f'"{req_def}" is not in a supported format.']}
        req_key_path = next(iter(req_def))
        chunk_key_path = req_def[req_key_path]
        resource_state = reqret.get("state")
        resource_name = reqret.get("name")

        if reqret["ret"].get("new_state", None) is None:
            return {
                "errors": [
                    f'"{resource_state}:{resource_name}" state does not have "new_state" in the state returns.'
                ]
            }

        # Construct state argument reference definition based on arg_bind requisite
        arg_reference_def = (
            "${" + f"{resource_state}:{resource_name}:{req_key_path}" + "}"
        )

        # First, find the value of the referenced state argument, based on the path
        req_arg_value = reqret["ret"]["new_state"]

        try:
            # Iterate over referenced state argument key chain and find the value in the state "new_state"
            for req_arg_key in req_key_path.split(":"):
                # The requisite argument path might include nested index, ex arg[0][1][2]
                req_arg_key, indexes = _parse_index(req_arg_key)

                if req_arg_key not in req_arg_value:
                    return {
                        "errors": [
                            f'"{req_key_path}" is not found as part of "{resource_state}" state "new_state".'
                        ]
                    }

                # If argument path contains a nested collection, find the element in the collection
                req_arg_value = _get_chunk_with_index(
                    req_arg_value[req_arg_key], indexes, req_key_path
                )

            # Second, set current state argument to the referenced state argument value
            hub.log.debug(
                f"Replacing references to `{arg_reference_def}` with value `{req_arg_value}`"
            )

            _set_chunk_arg_value(
                chunk, arg_reference_def, chunk_key_path.split(":"), req_arg_value, None
            )
        except AttributeError as ex:
            return {"errors": [f"{ex}"]}
        except IndexError as ex:
            return {"errors": [f"{ex}"]}

    return {}


def _parse_index(key_to_parse):
    """
    Parse indexes of key. For example, test[0][1] will return "test" as parsed key and [0,1] as parsed indexes.
    """
    indexes = re.findall(r"\[\d+\]", key_to_parse)
    if indexes:
        index_digits = []
        for index in indexes:
            index_digit = re.search(r"\d+", index).group(0)
            index_digits.append(int(index_digit))

        return key_to_parse[0 : key_to_parse.index("[")], index_digits

    return key_to_parse, None


def _set_chunk_arg_value(
    chunk, arg_reference_def, arg_key_chain, arg_value, chunk_indexes
):
    """
    Recursively iterate over arg_keys and update the chunk desired key with the referenced value
    """
    arg_key = arg_key_chain.pop(0)
    arg_key, next_chunk_indexes = _parse_index(arg_key)
    # Unescape dictionary references in the key definition.
    arg_key = arg_key.replace("[\\", "[")

    if len(arg_key_chain) == 0:
        indexed_chunk = _get_chunk_with_index(chunk, chunk_indexes, arg_key)

        if next_chunk_indexes:
            # arg_key is set to a (nested) collection and arg_value is added to it , ex: arg_key[0][1][2]
            _set_chunk_with_index(
                indexed_chunk[arg_key], next_chunk_indexes, arg_reference_def, arg_value
            )
        else:
            if arg_key not in indexed_chunk:
                indexed_chunk[arg_key] = ""
            # arg_key is set to arg_value
            indexed_chunk[arg_key] = _replace_arg_reference_with_arg_value(
                indexed_chunk[arg_key], arg_reference_def, arg_value
            )

    else:
        chunk = _get_chunk_with_index(chunk, chunk_indexes, arg_key)
        if arg_key not in chunk:
            chunk[arg_key] = {}

        _set_chunk_arg_value(
            chunk[arg_key],
            arg_reference_def,
            arg_key_chain,
            arg_value,
            next_chunk_indexes,
        )


def _get_chunk_with_index(chunk, chunk_indexes, arg_key):
    indexed_chunk = chunk
    if chunk_indexes:
        for index in chunk_indexes:
            if not isinstance(indexed_chunk, list) or len(indexed_chunk) < index + 1:
                raise AttributeError(
                    f'Cannot parse argument key {arg_key} for index "{index}", '
                    f'because argument key is not a list or it does not include element with index "{index}".'
                )
            indexed_chunk = indexed_chunk[index]

    return indexed_chunk


def _set_chunk_with_index(chunk, chunk_indexes, arg_reference_def, arg_value):
    index = chunk_indexes.pop(0)
    if not isinstance(chunk, list) or len(chunk) < index + 1:
        raise AttributeError(
            f'Cannot set argument value for index "{index}", '
            f'because argument key is not a list or it does not include element with index "{index}".'
        )

    if len(chunk_indexes) == 0:
        chunk[index] = _replace_arg_reference_with_arg_value(
            chunk[index], arg_reference_def, arg_value
        )
    else:
        _set_chunk_with_index(chunk[index], chunk_indexes, arg_reference_def, arg_value)


def _replace_arg_reference_with_arg_value(
    chunk_arg_value, arg_reference_def, arg_value
):
    """
    Find all occurrences of arg_reference_def in chunk_arg_value and replace them with arg_value.
    Return chunk_arg_value with all references to arg_reference_def resolved, or arg_value if no
    references found.
    """
    if (
        chunk_arg_value
        and isinstance(chunk_arg_value, str)
        and isinstance(arg_value, str)
        and arg_reference_def in chunk_arg_value
    ):
        return str.replace(chunk_arg_value, arg_reference_def, arg_value)
    else:
        return arg_value
