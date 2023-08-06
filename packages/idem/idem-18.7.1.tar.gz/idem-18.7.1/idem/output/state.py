# NOTES
# This is a VERY simple outputter for idem, it does not do everything the
# Salt highstate outputter does, and nor should it! This outputter should
# not become hyper complicated, things like terse should be another
# outputter, this should really just get things like errors added
from typing import Dict

from colored import attr
from colored import fg


def display(hub, data):
    """
    Display the data from an idem run
    """
    if not isinstance(data, dict):
        return hub.output.nested.display(data)
    endc = attr(0)
    strs = []
    fun_count = {}
    for tag in sorted(data, key=lambda k: data[k].get("__run_num", 0)):
        ret = data[tag]
        comps = tag.split("_|-")
        state = comps[0]
        id_ = comps[1]
        fun = comps[3]
        result = ret.get("result")
        comment = ret.get("comment")
        changes = hub.output.nested.display(ret.get("changes", {}))
        if result is True and changes:
            tcolor = fg(6)
        elif result is True:
            tcolor = fg(2)
        elif result is None:
            tcolor = fg(11)
        elif result is False:
            tcolor = fg(9)
        else:
            tcolor = fg(0)

        strs.append(f"{tcolor}--------{endc}")
        strs.append(f"{tcolor}      ID: {id_}{endc}")
        strs.append(f"{tcolor}Function: {state}.{fun}{endc}")
        strs.append(f"{tcolor}  Result: {result}{endc}")
        strs.append(f"{tcolor} Comment: {comment}{endc}")
        strs.append(f"{tcolor} Changes: {changes}{endc}")

        # Calculate counts for each function and result
        if fun_count.get(fun) is None:
            fun_count[fun] = {result: 1}
        elif fun_count[fun].get(result) is None:
            fun_count[fun][result] = 1
        else:
            fun_count[fun][result] += 1

    strs = strs + format_fun_counts(fun_count)
    return "\n".join(strs)


def format_fun_counts(fun_map: Dict[str, Dict[str, int]]) -> []:
    # Format counts for each function
    # Sample output:
    #  present: 1 successful
    #  present: 2 failed
    strs = ["\n"]

    for fun, result_and_count in fun_map.items():
        if result_and_count.get(True, 0) > 0:
            strs.append(f"{fun}: {result_and_count[True]} successful")
        if result_and_count.get(False, 0) > 0:
            strs.append(f"{fun}: {result_and_count[False]} failed")

    return strs
