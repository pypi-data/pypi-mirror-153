import json
import pathlib
import tempfile

from idem.exec.init import ExecReturn

__func_alias__ = {"exec_": "exec"}


async def sls(hub) -> int:
    """
    Execute the cli routine to run states
    """
    sls_sources = list(hub.OPT.idem.sls_sources)
    if hub.OPT.idem.tree:
        tree = f"file://{hub.OPT.idem.tree}"
        sls_sources.append(tree)
    src = hub.idem.sls_source.init.get_refs(sources=sls_sources, refs=hub.OPT.idem.sls)
    param = hub.idem.sls_source.param.get_refs(
        sources=hub.OPT.idem.param_sources, refs=hub.OPT.idem.params
    )
    name = hub.idem.RUN_NAME
    cache_dir = hub.OPT.idem.cache_dir

    # Get the acct information for the enforced state manager
    context_manager = hub.idem.managed.context(
        run_name=name,
        cache_dir=cache_dir,
        esm_plugin=hub.OPT.idem.esm_plugin,
        esm_profile=hub.OPT.idem.esm_profile,
        acct_file=hub.OPT.acct.acct_file,
        acct_key=hub.OPT.acct.acct_key,
        serial_plugin=hub.OPT.idem.esm_serial_plugin,
    )
    try:
        async with context_manager as state:
            await hub.idem.state.apply(
                name=name,
                sls_sources=src["sls_sources"],
                render=hub.OPT.idem.render,
                runtime=hub.OPT.idem.runtime,
                subs=["states"],
                cache_dir=cache_dir,
                sls=src["sls"],
                test=hub.OPT.idem.test,
                invert_state=hub.OPT.idem.invert,
                acct_file=hub.OPT.acct.acct_file,
                acct_key=hub.OPT.acct.acct_key,
                acct_profile=hub.OPT.idem.acct_profile,
                managed_state=state,
                param_sources=param["param_sources"],
                params=param["params"],
            )

            errors = hub.idem.RUNS[name]["errors"]
            if errors:
                display = hub.output.nested.display(errors)
                print(display)
                # Return a non-zero error code
                return len(errors)

            # Reconciliation loop
            await hub.reconcile.init.run(
                plugin=hub.OPT.idem.reconciler,
                pending_plugin=hub.OPT.idem.pending,
                name=name,
                apply_kwargs=dict(
                    sls_sources=src["sls_sources"],
                    render=hub.OPT.idem.render,
                    runtime=hub.OPT.idem.runtime,
                    cache_dir=hub.OPT.idem.cache_dir,
                    sls=src["sls"],
                    test=hub.OPT.idem.test,
                    acct_file=hub.OPT.acct.acct_file,
                    acct_key=hub.OPT.acct.acct_key,
                    acct_profile=hub.OPT.idem.acct_profile,
                    subs=["states"],
                    managed_state=state,
                ),
            )
    except Exception as e:
        display = hub.output.nested.display(str(e))
        print(display)
        # Return a non-zero error code
        return 1

    running = hub.idem.RUNS[name]["running"]

    output = hub.OPT.rend.output or "state"
    display = hub.output[output].display(running)
    print(display)
    return 0


async def exec_(hub) -> int:
    exec_path = hub.OPT.idem.exec_func
    exec_args = hub.OPT.idem.exec_args
    if not exec_path.startswith("exec"):
        exec_path = f"exec.{exec_path}"
    args = []
    kwargs = {}
    for arg in exec_args:
        if isinstance(arg, dict):
            kwargs.update(arg)
        else:
            args.append(arg)
    ret = await hub.idem.ex.run(
        path=exec_path,
        args=args,
        kwargs=kwargs,
        acct_file=hub.OPT.acct.acct_file,
        acct_key=hub.OPT.acct.acct_key,
        acct_profile=hub.OPT.idem.acct_profile,
    )

    output = hub.OPT.rend.output or "exec"
    display = hub.output[output].display(ret)
    print(display)

    if isinstance(ret, ExecReturn):
        return int(not ret.result)

    return 1


async def desc(hub) -> int:
    state_path = hub.OPT.idem.desc_glob
    ret = await hub.idem.describe.run(
        state_path,
        hub.OPT.acct.acct_file,
        hub.OPT.acct.acct_key,
        hub.OPT.idem.acct_profile,
        progress=hub.OPT.idem.progress,
        hard_fail=hub.OPT.idem.hard_fail,
        search_path=hub.OPT.idem.filter,
    )

    output = hub.OPT.rend.output or "yaml"
    display = hub.output[output].display(ret)
    print(display)
    return 0


async def validate(hub) -> int:
    """
    Execute the cli routine to validate states
    """
    sls_sources = hub.OPT.idem.sls_sources
    if hub.OPT.idem.tree:
        sls_sources.append(f"file://{hub.OPT.idem.tree}")
    src = hub.idem.sls_source.init.get_refs(sources=sls_sources, refs=hub.OPT.idem.sls)
    name = hub.OPT.idem.run_name
    await hub.idem.state.validate(
        name=name,
        sls_sources=src["sls_sources"],
        render=hub.OPT.idem.render,
        runtime=hub.OPT.idem.runtime,
        subs=["states"],
        cache_dir=hub.OPT.idem.cache_dir,
        sls=src["sls"],
        test=hub.OPT.idem.test,
        invert_state=hub.OPT.idem.invert,
        acct_file=hub.OPT.acct.acct_file,
        acct_key=hub.OPT.acct.acct_key,
        acct_profile=hub.OPT.idem.acct_profile,
    )

    errors = hub.idem.RUNS[name]["errors"]
    if errors:
        display = hub.output.nested.display(errors)
        print(display)
        # Return a non-zero error code
        return len(errors)

    ret = {
        "high": hub.idem.RUNS[name]["high"],
        "low": hub.idem.RUNS[name]["low"],
        "meta": hub.idem.RUNS[name]["meta"],
        "parameters": hub.idem.RUNS[name]["parameters"],
        "warnings": hub.idem.RUNS[name]["warnings"],
    }
    output = hub.OPT.rend.output or "nested"
    display = hub.output[output].display(ret)
    print(display)
    return 0


async def refresh(hub) -> int:
    """
    Update enforced state management with described resources.
    Run "describe" for the given path, then run `idem state --test` on it's output.
    This brings it in to the enforced state management.
    Nothing should be changed on the resources after this command.
    """
    state_path = hub.OPT.idem.desc_glob
    run_name = hub.idem.RUN_NAME
    cache_dir = hub.OPT.idem.cache_dir
    output = hub.OPT.rend.output or "state"

    # Generate an sls file based on "describe"
    ret = await hub.idem.describe.run(
        state_path,
        hub.OPT.acct.acct_file,
        hub.OPT.acct.acct_key,
        hub.OPT.idem.acct_profile,
        progress=hub.OPT.idem.progress,
        hard_fail=hub.OPT.idem.hard_fail,
        search_path=None,
    )
    if not ret:
        raise ValueError(f"No descriptions available for the given path: {state_path}")

    # Get the acct information for the enforced state manager
    context_manager = hub.idem.managed.context(
        run_name=run_name,
        cache_dir=cache_dir,
        esm_plugin=hub.OPT.idem.esm_plugin,
        esm_profile=hub.OPT.idem.esm_profile,
        acct_file=hub.OPT.acct.acct_file,
        acct_key=hub.OPT.acct.acct_key,
        serial_plugin=hub.OPT.idem.esm_serial_plugin,
    )
    try:
        async with context_manager as state:
            # Write the describe output to a file
            with tempfile.NamedTemporaryFile(suffix=".sls", delete=True) as fh:
                path = pathlib.Path(fh.name)
                display = hub.output.json.display(ret)
                fh.write(display.encode())
                fh.flush()

                # Apply the state from the describe file
                await hub.idem.state.apply(
                    name=run_name,
                    sls_sources=[f"file://{path.parent}"],
                    render="json",
                    runtime="parallel",
                    subs=["states"],
                    cache_dir=cache_dir,
                    sls=[path.stem],
                    test=True,
                    acct_file=hub.OPT.acct.acct_file,
                    acct_key=hub.OPT.acct.acct_key,
                    acct_profile=hub.OPT.idem.acct_profile,
                    managed_state=state,
                )
    except Exception as e:
        display = hub.output.nested.display(str(e))
        print(display)
        # Return a non-zero error code
        return 1

    # Report Errors
    errors = hub.idem.RUNS[run_name]["errors"]
    if errors:
        display = hub.output.nested.display(errors)
        print(display)
        # Return a non-zero error code
        return len(errors)

    # If something changed, which it shouldn't, it will show up now
    running = hub.idem.RUNS[run_name]["running"]
    # Get all the describe states that reported changes
    changed = {k: v for k, v in running.items() if v.get("changes")}
    display = hub.output[output].display(changed)
    print(display)
    if changed:
        hub.log.error(f"Changes were made by refresh on path: {state_path}")
    return len(changed)


async def restore(hub) -> int:
    """
    Restore the centralized state management context from a local json file
    """
    name = hub.idem.RUN_NAME
    cache_dir = hub.OPT.idem.cache_dir
    esm_plugin = hub.OPT.idem.esm_plugin

    with open(hub.OPT.idem.esm_cache_file) as fh:
        restore_data = json.load(fh)

    # Get the acct information for the centralized state manager
    context_manager = hub.idem.managed.context(
        run_name=name,
        cache_dir=cache_dir,
        esm_plugin=esm_plugin,
        esm_profile=hub.OPT.idem.esm_profile,
        acct_file=hub.OPT.acct.acct_file,
        acct_key=hub.OPT.acct.acct_key,
        serial_plugin=hub.OPT.idem.esm_serial_plugin,
    )
    try:
        async with context_manager as state:
            state.update(restore_data)
    except Exception as e:
        display = hub.output.nested.display(str(e))
        print(display)
        # Return a non-zero error code
        return 1

    return 0


async def doc(hub) -> int:
    """
    Get documentation for functions under the given reference
    """
    # Get all the documentation from the hub as a single tree
    tree = await hub.tree.init.traverse()

    if hub.OPT.pop_tree.ref:
        # Parse the tree for the named reference
        tree = hub.tree.ref.get(tree, hub.OPT.pop_tree.ref)

        if not tree:
            hub.log.error(
                f"Reference does not exist on the hub: {hub.OPT.pop_tree.ref}"
            )
            return 1

        # Flatten the tree so that each full reference is a top-level key
        ret = hub.tree.ref.list(tree)

        # Get all the references under the named reference from the tree
        result = {}
        for ref, docs in ret.items():
            if ref.startswith(hub.OPT.pop_tree.ref) and "parameters" in docs:
                result[ref] = docs

        if not result:
            result = {hub.OPT.pop_tree.ref: ret[hub.OPT.pop_tree.ref]}
    else:
        # Flatten the tree and return every function reference
        result = {}
        ret = hub.tree.ref.list(tree)
        for ref, docs in ret.items():
            if "parameters" in docs:
                result[ref] = docs

    outputter = hub.OPT.rend.output or "nested"

    print(hub.output[outputter].display(result))
    return 0
