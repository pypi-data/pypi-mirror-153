import pathlib


def gather(hub, profiles):
    """
    The "default" profile for esm.local is created with configuration values
    Other profiles can be created manually with the following format.

    .. code-block:: sls

        esm.local:
            profile_name:
                run_name: ...
                cache_dir: /path/to/cache/dir
                serial_plugin: json|msgpack
    """
    sub_profiles = {}
    for profile, ctx in profiles.get("esm.local", {}).items():
        idem_opts = hub.OPT.get("idem", {})
        # Fill in any missing params from hub.OPT if possible
        if not ctx.get("run_name"):
            ctx["run_name"] = idem_opts.get("run_name")
        if not ctx.get("cache_dir"):
            ctx["cache_dir"] = idem_opts.get("cache_dir")
        if not isinstance(ctx["cache_dir"], pathlib.Path):
            ctx["cache_dir"] = pathlib.Path(ctx["cache_dir"])
        if not ctx.get("serial_plugin"):
            ctx["serial_plugin"] = idem_opts.get("serial_plugin")
        sub_profiles[profile] = ctx
    return sub_profiles
