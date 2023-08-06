import enum
import json
import uuid
from typing import Any
from typing import Dict
from typing import List

import dict_tools.update

__func_alias__ = {"compile_": "compile"}


class Status(enum.IntEnum):
    FINISHED = 0
    CREATED = 1
    GATHERING = 2
    COMPILING = 3
    RUNNING = 4
    COMPILATION_ERROR = -1
    GATHER_ERROR = -2
    RUNTIME_ERROR = -3
    UNDEFINED = -4


def update_status(hub, name: str, status_: Status):
    """
    Update the status of the run and fire an event
    """
    if name in hub.idem.RUNS:
        hub.idem.RUNS[name]["status"] = status_
    hub.idem.event.put_nowait(
        profile="idem-status",
        body=status_.name,
        tags={"ref": "idem.state.update_status", "type": "state-status"},
    )


async def create(
    hub,
    name: str,
    sls_sources: List[str],
    render: str,
    runtime: str,
    subs: List[str],
    cache_dir: str,
    test: bool,
    acct_file: str,
    acct_key: str,
    acct_profile: str,
    acct_blob: bytes,
    managed_state: Dict[str, Any],
    param_sources: List[str],
    acct_data: Dict[str, Any] = None,
    invert_state: bool = False,
):
    """
    Create a new instance to execute against
    """
    if acct_data is None:
        acct_data = await hub.idem.acct.data(
            acct_key=acct_key, acct_file=acct_file, acct_blob=acct_blob
        )

    hub.idem.RUNS[name] = {
        "sls_sources": sls_sources,
        "param_sources": param_sources,
        "render": render,
        "runtime": runtime,
        "subs": subs,
        "cache_dir": cache_dir,
        "states": {},
        "test": test,
        "resolved": set(),
        "files": set(),
        "high": {},
        # Jinja render uses the params python dict object to read the value corresponding to
        # any parameter. When the parameter is not present params dict object's get() returns
        # the None object. We need to return __PYTHON_NONE__ instead, so that it gets suitably
        # converted into the python None object in the replacement renderer.
        # Here we are using type library function to create a new type object, that has get()
        # function which returns self[key] if parameter (key) is present, default value (if
        # specified), and __PYTHON_NONE__ otherwise. Python dict is used as base class.
        # Thus, for all parameters that are not present in dict, this get() lambda returns
        # __PYTHON_NONE__.
        "params": type(
            "",
            (dict,),
            {
                "get": lambda self, key, value=None: self[key]
                if key in self
                else value
                if value is not None
                else "__PYTHON_NONE__"
            },
        )(),
        "post_low": [],
        "errors": [],
        "iorder": 100000,
        "sls_refs": {},
        "blocks": {},
        "running": {},
        "meta": {"SLS": {}, "ID_DECS": {}},
        "run_num": 1,
        "add_low": [],
        "acct_profile": acct_profile,
        "acct_data": acct_data,
        "status": Status.CREATED,
        "managed_state": managed_state,
        "invert_state": invert_state,
    }


async def validate(
    hub,
    name: str,
    sls_sources: List[str],
    render: str,
    runtime: str,
    subs: List[str],
    cache_dir: str,
    sls: List[str],
    test: bool = False,
    invert_state: bool = False,
    acct_file: str = None,
    acct_key: str = None,
    acct_profile: str = "default",
    acct_blob: bytes = None,
):
    """
    Run idem!
    """
    await hub.idem.state.create(
        name,
        sls_sources,
        render,
        runtime,
        subs,
        cache_dir,
        test,
        acct_file=acct_file,
        acct_key=acct_key,
        acct_profile=acct_profile,
        acct_blob=acct_blob,
        managed_state=None,
        param_sources=None,
        invert_state=invert_state,
    )
    # Get the sls file
    # render it
    # compile high data to "new" low data (bypass keyword issues)
    # Run the low data using act/idem
    hub.idem.RUNS[name]["params"] = hub.tool.parameter.get_validate_params()
    # process sls-sources
    hub.idem.RUNS[name]["status"] = Status.GATHERING
    await hub.idem.sls_source.init.gather(name, *sls)
    if hub.idem.RUNS[name]["errors"]:
        hub.idem.RUNS[name]["status"] = Status.GATHER_ERROR
        return
    if not hub.idem.RUNS[name].get("high"):
        # If there is no high data after rendering, that means the rendered result is empty. So we return.
        hub.idem.state.update_status(name, Status.FINISHED)
        return
    hub.idem.RUNS[name]["status"] = Status.COMPILING
    await hub.idem.state.compile(name)
    if hub.idem.RUNS[name]["errors"]:
        hub.idem.RUNS[name]["status"] = Status.COMPILATION_ERROR
        return
    await hub.idem.state.validate_(name)


async def apply(
    hub,
    name: str,
    sls_sources: List[str],
    render: str,
    runtime: str,
    subs: List[str],
    cache_dir: str,
    sls: List[str],
    test: bool = False,
    invert_state: bool = False,
    acct_file: str = None,
    acct_key: str = None,
    acct_profile: str = "default",
    acct_blob: bytes = None,
    acct_data: Dict[str, Any] = None,
    managed_state: Dict[str, Any] = None,
    param_sources: List[str] = None,
    params: List[str] = None,
):
    """
    Run idem!
    """
    if params is None:
        params = []
    await hub.idem.state.create(
        name,
        sls_sources,
        render,
        runtime,
        subs,
        cache_dir,
        test,
        acct_file=acct_file,
        acct_key=acct_key,
        acct_profile=acct_profile,
        acct_blob=acct_blob,
        acct_data=acct_data,
        managed_state=managed_state,
        param_sources=param_sources or [],
        invert_state=invert_state,
    )

    hub.idem.state.update_status(name, Status.GATHERING)
    if params:
        await hub.idem.sls_source.param.gather(name, *params)
        if hub.idem.RUNS[name]["errors"]:
            hub.idem.state.update_status(name, Status.GATHER_ERROR)
            return

    # Get the sls file
    # render it
    # compile high data to "new" low data (bypass keyword issues)
    # Run the low data using acct/idem
    await hub.idem.sls_source.init.gather(name, *sls)
    if hub.idem.RUNS[name]["errors"]:
        hub.idem.state.update_status(name, Status.GATHER_ERROR)
        return
    if not hub.idem.RUNS[name].get("high"):
        # If there is no high data after rendering, that means the rendered result is empty. So we return.
        hub.idem.state.update_status(name, Status.FINISHED)
        return
    hub.idem.state.update_status(name, Status.COMPILING)
    await hub.idem.state.compile(name)
    if hub.idem.RUNS[name]["errors"]:
        hub.idem.state.update_status(name, Status.COMPILATION_ERROR)
        return

    hub.idem.state.update_status(name, Status.RUNNING)
    try:
        await hub.idem.run.init.start(name)
    finally:
        hub.idem.state.update_status(name, Status.FINISHED)


async def compile_(hub, name):
    """
    Compile the data defined in the given run name
    """
    for mod in hub.idem.compiler:
        if hasattr(mod, "stage"):
            ret = mod.stage(name)
            await hub.pop.loop.unwrap(ret)


async def validate_(hub, name):
    for mod in hub.idem.validate:
        if hasattr(mod, "stage"):
            ret = mod.stage(name)
            await hub.pop.loop.unwrap(ret)


async def single(hub, _ref_: str, _test_: bool = None, *args, **kwargs):
    """
    Run a single state and return the raw result
    :param hub:
    :param _ref_: The state's reference on the hub
    :param _test_: Run the state in a low-consequence test-mode
    :param args: Args to be passed straight through to the state
    :param kwargs: Kwargs to be passed straight through to the state
    """
    if _test_ is None:
        _test_ = hub.OPT.idem.test

    acct_file = hub.OPT.acct.acct_file
    acct_key = hub.OPT.acct.acct_key
    acct_profile = hub.OPT.acct.get("acct_profile", "default")

    args = [a for a in args]

    if not _ref_.startswith("states."):
        _ref_ = f"states.{_ref_}"

    func = getattr(hub, _ref_)
    params = func.signature.parameters

    if "ctx" in params:
        ctx = await hub.idem.acct.ctx(_ref_, acct_file, acct_key, acct_profile)
        ctx.test = _test_
        args.insert(0, ctx)

    ret = func(*args, **kwargs)
    return await hub.pop.loop.unwrap(ret)


async def batch(
    hub,
    states: Dict[str, Dict[str, Any]],
    runtime: str = None,
    test: bool = None,
    renderer: str = None,
    profiles: Dict[str, Any] = None,
    encrypted_profiles: str = None,
    acct_key: str = None,
    default_acct_profile: str = "default",
    name: str = None,
    crypto_plugin: str = "fernet",
    reconcile_plugin: str = None,
    pending_plugin: str = None,
    esm_plugin: str = None,
    esm_profile: str = None,
):
    """
    Run multiple states defined in code
    :param hub:
    :param states: A dictionary definition of the states to run
    :param runtime: "serial" or "parallel"
    :param test: Set "test" to "True" in the implicit ctx parameter
    :param renderer: The render pipe to use
    :param profiles: An unencrypted dump of acct profiles
    :param encrypted_profiles: An encoded dump of acct profiles encrypted with a crypto key
    :param acct_key: The decryption fernet key for acct profiles, defaults to the key defined in idem's runtime config
    :param default_acct_profile: The acct profile to use for states that don't have a profile explicitly defined
    :param name: A unique identifier for this batch's run
    :param crypto_plugin: The plugin that should be used to decrypt encrypted profile blobs
    :param reconcile_plugin: The plugin for reconciliation
    :param pending_plugin: The plugin for determining state's 'pending' status for reconciliation
    """
    name = name or f"name_{uuid.uuid4()}"
    runtime = runtime or hub.OPT.idem.runtime
    render = renderer or hub.OPT.idem.render
    test = hub.OPT.idem.test if test is None else test
    sls_source = f"sls_source_{uuid.uuid4()}"
    sls = [sls_source]
    data = {sls_source: states}
    sls_sources = [f"json://{json.dumps(data)}"]

    acct_key = acct_key or hub.OPT.acct.acct_key
    acct_profile = default_acct_profile or hub.OPT.acct.get("acct_profile", "default")

    # TODO the default reconcile will change to "basic" once reconciliation loop is enabled
    reconcile_plugin = reconcile_plugin or hub.OPT.idem.get("reconciler", "none")
    pending_plugin = pending_plugin or hub.OPT.idem.get("pending", "default")

    if profiles:
        if not acct_key:
            # If no acct_key exists, temporarily encrypt the profiles locally with a random key
            acct_key = hub.crypto[crypto_plugin].generate_key()
        elif encrypted_profiles:
            # combine the encrypted and unencrypted profiles into a single entity
            decrypted = hub.crypto[crypto_plugin].decrypt(encrypted_profiles, acct_key)
            profiles = dict_tools.update.update(profiles, decrypted, merge_lists=True)

        # Encrypt the raw profiles so that idem can easily consume them
        encrypted_profiles = hub.crypto[crypto_plugin].encrypt(profiles, acct_key)

    apply_kwargs = dict(
        name=name,
        sls_sources=sls_sources,
        render=render,
        runtime=runtime,
        subs=["states"],
        cache_dir=hub.OPT.idem.cache_dir,
        sls=sls,
        test=test,
        acct_key=acct_key,
        acct_profile=acct_profile,
    )
    if encrypted_profiles:
        if isinstance(encrypted_profiles, str):
            encrypted_profiles = encrypted_profiles.encode()
        apply_kwargs["acct_blob"] = encrypted_profiles
    else:
        # Default to the acct_file defined in the environment at runtime
        apply_kwargs["acct_file"] = hub.OPT.acct.acct_file

    context_manager = hub.idem.managed.context(
        run_name=name,
        cache_dir=hub.OPT.idem.cache_dir,
        esm_plugin=esm_plugin or hub.OPT.idem.esm_plugin,
        esm_profile=esm_profile or hub.OPT.idem.esm_profile,
        acct_key=acct_key,
        acct_blob=encrypted_profiles,
        serial_plugin=hub.OPT.idem.esm_serial_plugin,
    )
    try:
        async with context_manager as state:
            apply_kwargs["managed_state"] = state
            await hub.idem.state.apply(**apply_kwargs)

            if hub.idem.RUNS[name]["errors"]:
                # pop is required to remove the run from memory
                run_data = hub.idem.RUNS.pop(name)
                return run_data["errors"]

            # Reconciliation loop
            await hub.reconcile.init.run(
                plugin=reconcile_plugin, pending_plugin=pending_plugin, **apply_kwargs
            )
    except Exception as e:
        display = hub.output.nested.display(str(e))
        print(display)
        # Return a non-zero error code
        return 1

    run_data = hub.idem.RUNS.pop(name)
    return run_data["running"]


def status(hub, name: str) -> Dict[str, Any]:
    """
    Get the status of the named state run

        .. code-block:: json

            {
                "test": True or False,
                "errors": [],
                "running": {},
                "acct_profile": "acct profile name used for this run",
                "status": 0
                "status_name": "FINISHED"
            }
    :param hub:
    :param name: The unique identifier that was given to the state run
    :returns: A dictionary of the requested state run, An empty dictionary if the name doesn't exist
    """
    if name in hub.idem.RUNS:
        run = hub.idem.RUNS[name]
        hub.idem.state.update_status(name, run["status"])
        return {
            "test": run["test"],
            "errors": run["errors"],
            "running": run["running"],
            "acct_profile": run["acct_profile"],
            "status": run["status"].value,
            "status_name": run["status"].name,
        }
    else:
        hub.log.error(f"No idem run with Job ID: {name}")
        hub.idem.state.update_status(name, Status.UNDEFINED)
        return {
            "test": None,
            "errors": [],
            "running": {},
            "acct_profile": "",
            "status": Status.UNDEFINED.value,
            "status_name": Status.UNDEFINED.name,
        }
