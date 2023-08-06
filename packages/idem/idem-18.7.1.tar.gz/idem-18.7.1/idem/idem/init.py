# The order of the sequence that needs to be implemented:
# Start with a single sls file, just like you started with salt
# Stub out the routines around gathering the initial sls file
# Just use a yaml renderer and get it to where we can manage some basic
# includes to drive to highdata
# Then we can start to fill out renderers while at the same time
# deepening the compiler
import sys


def __init__(hub):
    hub.pop.sub.load_subdirs(hub.idem, recurse=True)
    hub.idem.RUNS = {}
    hub.pop.sub.add(dyne_name="log")
    hub.pop.sub.add(dyne_name="acct")
    hub.pop.sub.add(dyne_name="rend")
    hub.pop.sub.add(dyne_name="output")
    hub.pop.sub.add(dyne_name="evbus")
    hub.pop.sub.add(dyne_name="reconcile")
    hub.pop.sub.add(dyne_name="source")
    hub.pop.sub.load_subdirs(hub.reconcile, recurse=True)
    hub.pop.sub.add(dyne_name="tool")
    hub.pop.sub.load_subdirs(hub.tool, recurse=True)
    hub.pop.sub.add(dyne_name="esm")
    hub.pop.sub.add(dyne_name="exec")
    hub.pop.sub.load_subdirs(hub.exec, recurse=True)
    hub.pop.sub.add(dyne_name="states")
    hub.pop.sub.load_subdirs(hub.states, recurse=True)
    hub.pop.sub.add(dyne_name="tree", omit_class=False)
    hub.idem.RMAP = hub.idem.req.init.define()
    hub.idem.RUN_NAME = "cli"


def cli(hub):
    """
    Execute a single idem run from the cli
    """
    hub.pop.config.load(["idem", "acct", "rend", "evbus", "pop_tree"], cli="idem")
    # Initialize the async loop for the entire project
    hub.pop.loop.create()
    # Start the main program within the async loop
    retcode = hub.pop.Loop.run_until_complete(hub.idem.init.cli_apply())
    sys.exit(retcode)


async def cli_apply(hub) -> int:
    """
    Run the CLI routine in a loop
    """
    if hub.SUBPARSER in ("encrypt", "decrypt"):
        # Break early for acct commands
        return await hub.acct.init.cli_apply()
    elif hub.SUBPARSER == "doc":
        return await hub.idem.cli.doc()

    # Initialize the broker queue for evbus
    await hub.evbus.broker.init()

    # Specify the serializing plugin for evbus
    hub.evbus.SERIAL_PLUGIN = hub.OPT.evbus.serial_plugin
    # Use the run name as a routing key for exec modules
    hub.idem.RUN_NAME = hub.OPT.idem.run_name
    # Keep the local ESM cache file if explictly configured to do so
    hub.idem.managed.KEEP_CACHE_FILE = hub.OPT.idem.esm_keep_cache

    # Collect ingress profiles from acct
    ingress_profiles = await hub.evbus.acct.profiles(
        acct_file=hub.OPT.acct.acct_file,
        acct_key=hub.OPT.acct.acct_key,
    )

    # Start the listener in it's own task
    listener = hub.pop.Loop.create_task(hub.evbus.init.start(ingress_profiles))
    try:
        await hub.evbus.init.join()

        if hub.SUBPARSER == "state":
            return await hub.idem.cli.sls()
        elif hub.SUBPARSER == "exec":
            return await hub.idem.cli.exec()
        elif hub.SUBPARSER == "describe":
            return await hub.idem.cli.desc()
        elif hub.SUBPARSER == "validate":
            return await hub.idem.cli.validate()
        elif hub.SUBPARSER == "refresh":
            return await hub.idem.cli.refresh()
        elif hub.SUBPARSER == "restore":
            return await hub.idem.cli.restore()
        else:
            print(hub.args.parser.help())
            return 2
    finally:
        await hub.evbus.init.stop()
        await listener
