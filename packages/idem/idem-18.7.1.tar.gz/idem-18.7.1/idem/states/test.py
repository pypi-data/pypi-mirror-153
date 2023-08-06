"""
Test States
===========

Provide test case states that enable easy testing of things to do with state
calls, e.g. running, calling, logging, output filtering etc.

.. code-block:: yaml

    always-passes-with-any-kwarg:
      test.nop:
        - name: foo
        - something: else
        - foo: bar

    always-passes:
      test.succeed_without_changes:
        - name: foo

    always-fails:
      test.fail_without_changes:
        - name: foo

    always-changes-and-succeeds:
      test.succeed_with_changes:
        - name: foo

    always-changes-and-fails:
      test.fail_with_changes:
        - name: foo
"""
import inspect
import random
import threading

TREQ = {
    "treq": {
        "require": [
            "test.nop",
        ]
    },
    "unique": ["unique_op"],
}

UNIQUE_LOCK = threading.Lock()

__contracts__ = ["resource"]


def __init__(hub):
    hub.states.test.ACCT = ["test"]


def acct(hub, ctx, name):
    """
    Return exactly what was passed into ctx.acct
    """
    ret = {
        "name": name,
        "result": True,
        "comment": None,
        "old_state": None,
        "new_state": ctx.acct,
    }
    if not ctx.acct:
        ret["result"] = False

    return ret


def treq(hub, ctx, name, **kwargs):
    """
    Ensure that a transparent requisite is applied
    """
    return succeed_without_changes(hub, ctx, name)


def nop(hub, ctx, name, **kwargs):
    """
    A no-op state that does nothing. Useful in conjunction with the `use`
    requisite, or in templates which could otherwise be empty due to jinja
    rendering
    """
    if ctx["test"]:
        return none_without_changes(hub, ctx, name)
    return succeed_without_changes(hub, ctx, name)


async def anop(hub, ctx, name, **kwargs):
    """
    A no-op state that does nothing. Useful in conjunction with the `use`
    requisite, or in templates which could otherwise be empty due to jinja
    rendering
    """
    if ctx["test"]:
        return none_without_changes(hub, ctx, name)
    return succeed_without_changes(hub, ctx, name)


async def unique_op(hub, ctx, name, **kwargs):
    """
    A state that is defined as 'unique' treq, and require a single instance
    to be invoked at a time. performs locking.
    """
    # Throw an error if could not acquire the lock
    assert UNIQUE_LOCK.acquire(blocking=False) == True, "unique_op is running. Locked!"
    await hub.pop.loop.sleep(2)
    UNIQUE_LOCK.release()

    if ctx["test"]:
        return none_without_changes(hub, ctx, name)
    return succeed_without_changes(hub, ctx, name)


def succeed_with_comment(hub, ctx, name, comment, **kwargs):
    ret = {
        "name": name,
        "changes": {},
        "result": True,
        "comment": comment,
    }
    return ret


def succeed_without_changes(hub, ctx, name, **kwargs):
    """
    name
        A unique string.
    """
    ret = {"name": name, "changes": {}, "result": True, "comment": "Success!"}
    return ret


def none_without_changes(hub, ctx, name, **kwargs):
    """
    name
        A unique string.
    """
    ret = {"name": name, "changes": {}, "result": None, "comment": "Success!"}
    return ret


def fail_without_changes(hub, ctx, name, **kwargs):
    """
    Returns failure.

    name:
        A unique string.
    """
    ret = {"name": name, "changes": {}, "result": False, "comment": "Failure!"}

    return ret


def succeed_with_changes(hub, ctx, name, **kwargs):
    """
    Returns successful and changes is not empty

    name:
        A unique string.
    """
    ret = {
        "name": name,
        "old_state": {},
        "new_state": {},
        "changes": {},
        "result": True,
        "comment": "Success!",
    }

    ret["changes"] = {
        "testing": {"old": "Unchanged", "new": "Something pretended to change"},
        "tests": [[{"new": "new_test"}]],
    }

    ret["new_state"] = {
        "testing": {"old": "Unchanged", "new": "Something pretended to change"},
        "tests": [[{"new": "new_test"}]],
    }

    return ret


def succeed_with_arg_bind(hub, ctx, name, **kwargs):
    """
    Returns successful and changes is not empty

    name:
        A unique string.
    """
    ret = {
        "name": name,
        "old_state": {},
        "new_state": {},
        "changes": {},
        "result": True,
        "comment": "Success!",
    }

    ret["changes"] = {"testing": kwargs.get("parameters", {})}

    ret["new_state"] = {"testing": kwargs.get("parameters", {})}

    return ret


def fail_with_changes(hub, ctx, name, **kwargs):
    """
    Returns failure and changes is not empty.

    name:
        A unique string.
    """
    ret = {"name": name, "changes": {}, "result": False, "comment": "Failure!"}
    ret["changes"] = {
        "testing": {"old": "Unchanged", "new": "Something pretended to change"}
    }
    return ret


def update_low(hub, ctx, name):
    """
    Use the __run_name to add a run to the low
    """
    extra = {
        "__sls__": "none",
        "name": "totally_extra_alls",
        "__id__": "king_arthur",
        "state": "test",
        "fun": "nop",
    }
    hub.idem.RUNS[ctx["run_name"]]["add_low"].append(extra)
    return succeed_without_changes(hub, ctx, name)


def mod_watch(hub, ctx, name, **kwargs):
    """
    Return a mod_watch call for test
    """
    ret = {
        "name": name,
        "changes": {"watch": True},
        "result": True,
        "comment": "Watch ran!",
    }
    return ret


def configurable_test_state(
    hub, ctx, name, changes=True, result=True, comment="", **kwargs
):
    """
    A configurable test state which determines its output based on the inputs.

    name:
        A unique string.
    changes:
        Do we return anything in the changes field?
        Accepts True, False, and 'Random'
        Default is True
    result:
        Do we return successfully or not?
        Accepts True, False, and 'Random'
        Default is True
        If test is True and changes is True, this will be None.  If test is
        True and and changes is False, this will be True.
    comment:
        String to fill the comment field with.
        Default is ''
    """
    ret = {"name": name, "changes": {}, "result": False, "comment": comment}

    change_data = {
        "testing": {"old": "Unchanged", "new": "Something pretended to change"}
    }

    # If changes is True, then we place our dummy change dictionary into it
    if changes == "Random":
        if random.choice([True, False]):
            ret["changes"] = change_data
    elif changes is True:
        ret["changes"] = change_data
    elif changes is False:
        ret["changes"] = {}

    if result == "Random":
        ret["result"] = random.choice([True, False])
    elif result is True:
        ret["result"] = True
    elif result is False:
        ret["result"] = False

    if ctx["test"]:
        ret["result"] = True if changes is False else None
        ret["comment"] = "This is a test" if not comment else comment

    return ret


def present(
    hub, ctx, name: str, old_state=None, new_state=None, result=True, force_save=None
):
    """
    Return the previous old_state, if it's not specified in sls, and the given new_state.
    Raise an error on fail
    """
    if old_state is None:
        old_state = ctx.get("old_state")
    ret = {
        "name": name,
        "old_state": old_state,
        "new_state": new_state,
        "result": result,
        "comment": None,
    }
    if force_save is not None:
        ret["force_save"] = force_save
    return ret


def absent(hub, ctx, name: str, new_state=None, result=True):
    old_state = ctx.get("old_state")
    return {
        "name": name,
        "old_state": old_state,
        "new_state": new_state,
        "result": result,
        "comment": None,
    }


async def describe(hub, ctx):
    """
    Get the functions
    """
    ret = {}
    for func in hub.states.test:
        name = func.__name__
        if name in ("present", "absent", "succeed_with_arg_bind", "describe"):
            continue
        ref = f"test.{name}"
        state_name = f"Description of {ref}"
        ret[state_name] = {ref: []}

        # Collect args
        for arg, p in func.signature.parameters.items():
            if arg in ("hub", "ctx", "kwargs"):
                continue
            elif arg == "name":
                ret[state_name][ref].append({arg: name})
            else:
                if p.default == inspect._empty:
                    ret[state_name][ref].append({arg: None})
                else:
                    ret[state_name][ref].append({arg: p.default})

    return ret
