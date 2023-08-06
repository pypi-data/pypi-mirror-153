import copy
from typing import Any
from typing import Dict


def run(
    hub,
    seq: Dict[int, Dict[str, Any]],
    low: Dict[str, Any],
    running: Dict[str, Any],
    options: Dict[str, Any],
) -> Dict[int, Dict[str, Any]]:
    """
    Process the unique requisite
    Other requisites were already processed. 'Unique' is processed last to avoid circular dependencies.
    Convert 'unique' to 'unmet' dependency, to ensure sequential execution.
    Group all the states that require uniqueness for each 'unique' function.
    Find a state in the group that can be executed and mark all the other states dependent on it.
    This logic is executed after each run.
    Next state to execute is determined like this:
    1. State without unmet requirements
    2. State without dependencies on other States of the same type
    3. State with smallest dependencies chain
    """
    # Function reference to a list of tags/states
    unique_map = {}
    # Populate unique map, function and chunks that require 'unique' handling
    for ind, data in seq.items():
        if "unique" not in data["chunk"]:
            continue
        chunk = data["chunk"]
        fun_ref = f"{chunk['state']}.{chunk['fun']}"
        if fun_ref in unique_map:
            unique_map.get(fun_ref).append(data["tag"])
        else:
            unique_map = {fun_ref: [data["tag"]]}

    if len(unique_map) == 0:
        return seq

    # Map tag to data
    tag_map = {}
    # Populate tag map
    for data in seq.values():
        tag_map[data["tag"]] = data

    for fun_ref, tag_list in unique_map.items():
        if len(tag_list) <= 1:
            continue
        hub.log.debug(f"Ordering 'unique' states for '{fun_ref}'")
        # Check for a 'free' state
        tag_list_copy = copy.deepcopy(tag_list)
        next_unique_tag = _find_next_tag(tag_list_copy, tag_map)
        assert (
            next_unique_tag
        ), f"Expecting a first tag to be unique for function {fun_ref}"
        tag_list_copy.remove(next_unique_tag)
        for tag in tag_list_copy:
            tag_map[tag]["unmet"].add(next_unique_tag)

    return seq


def _find_next_tag(tag_list, tag_map):
    # Get next tag based on the following criteria:
    # 1. Tag without unmet requirements
    # 2. Tag without dependencies on other chunks of the same type
    # 3. Tag with fewest dependency chain
    if len(tag_list) == 0:
        return None

    tags = _find_independent_tags(tag_list, tag_map)
    if len(tags) == 1:
        return tags.pop()
    if not tags:
        tags = tag_list

    # Map tag to a numerical value of its dependency tree depth
    depth_map = {}
    for tag in tags:
        depth_map[tag] = _calculate_depth(tag, tag_map, 0)
    return list(_sort_tags(depth_map).keys())[0]


def _find_independent_tags(tag_list, tag_map):
    # There must be at least one tag that is not dependent on any other
    # items from the list
    if len(tag_list) == 0:
        return []
    if len(tag_list) == 1:
        return tag_list

    independent_tags = []
    for tag in tag_list:
        unmet_for_tag = tag_map[tag].get("unmet", set())
        if len(unmet_for_tag) == 0:
            independent_tags.append(tag)
        # Tag should not be dependent on others from the list
        elif len(unmet_for_tag.intersection(tag_list)) == 0:
            independent_tags.append(tag)

    return independent_tags


def _calculate_depth(tag, tag_map, depth):
    if tag_map[tag]["unmet"] is None or len(tag_map[tag]["unmet"]) == 0:
        return depth
    max = -1
    for dependent in tag_map[tag]["unmet"]:
        d = _calculate_depth(dependent, tag_map, depth + 1)
        if d > max:
            max = d
    return max


def _sort_tags(depth_map) -> Dict:
    # Sort from lower depth to lower
    return dict(sorted(depth_map.items(), key=lambda item: item[1], reverse=False))
