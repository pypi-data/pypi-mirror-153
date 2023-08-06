CLI_CONFIG = {
    "config": {"options": ["-c"], "subcommands": ["_global_"]},
    # Describe Options
    "desc_glob": {
        "display_priority": 0,
        "positional": True,
        "subcommands": ["describe", "refresh"],
        "help": "A glob to match the refs that should be ran",
    },
    "progress": {
        "action": "store_true",
        "subcommands": ["describe", "refresh"],
        "help": "Show a progress bar",
    },
    "hard_fail": {
        "action": "store_true",
        "subcommands": ["describe", "refresh"],
        "help": "Hard stop the first time an error is raised",
    },
    "filter": {
        "type": str,
        "subcommands": ["describe"],
        "help": "A JMES search path",
    },
    # Exec Options
    "exec_func": {
        "display_priority": 0,
        "positional": True,
        "subcommands": ["exec"],
        "help": "The execution function to run by it's reference on the hub",
    },
    "exec_args": {
        "display_priority": 1,
        "positional": True,
        "nargs": "*",
        "render": "cli",
        "subcommands": ["exec"],
    },
    # State and validate options
    "run_name": {
        "subcommands": ["state", "exec", "describe", "validate", "refresh", "restore"],
    },
    "sls_sources": {"nargs": "*", "subcommands": ["state", "validate"]},
    "param_sources": {"nargs": "*", "subcommands": ["state", "describe"]},
    "test": {"options": ["-t"], "action": "store_true", "subcommands": ["state"]},
    "tree": {
        "options": ["-T"],
        "subcommands": ["state", "validate"],
    },
    "cache_dir": {"subcommands": ["state", "validate", "refresh", "restore"]},
    "root_dir": {"subcommands": ["state", "validate", "refresh", "restore"]},
    "params": {"nargs": "*", "subcommands": ["state", "describe"]},
    "invert": {
        "action": "store_true",
        "subcommands": ["state", "validate"],
        "help": "Inverts the action taken during state execution. For example, absent in case of present and present in case of absent.",
    },
    "render": {
        "subcommands": ["state", "validate"],
    },
    "runtime": {
        "subcommands": ["state"],
    },
    "reconciler": {
        "options": ["-r", "-R"],
        "subcommands": ["state"],
    },
    "pending": {
        "options": ["-p", "-P"],
        "subcommands": ["state"],
    },
    "output": {
        "source": "rend",
        "subcommands": [
            "exec",
            "state",
            "describe",
            "decrypt",
            "validate",
            "refresh",
            "doc",
        ],
    },
    "sls": {"positional": True, "nargs": "*", "subcommands": ["state", "validate"]},
    "esm_plugin": {"subcommands": ["state", "validate", "refresh", "restore"]},
    "esm_profile": {"subcommands": ["state", "validate", "refresh", "restore"]},
    # ACCT options
    "input_file": {
        "source": "acct",
        "positional": True,
        "subcommands": ["encrypt", "decrypt"],
    },
    "output_file": {
        "subcommands": ["encrypt"],
        "source": "acct",
    },
    "acct_file": {
        "source": "acct",
        "os": "ACCT_FILE",
        "subcommands": ["state", "exec", "describe", "validate", "refresh", "restore"],
    },
    "acct_key": {
        "source": "acct",
        "os": "ACCT_KEY",
        "subcommands": [
            "state",
            "exec",
            "describe",
            "encrypt",
            "decrypt",
            "validate",
            "refresh",
            "restore",
        ],
    },
    "acct_profile": {
        "os": "ACCT_PROFILE",
        "subcommands": ["state", "exec", "describe", "validate", "refresh"],
    },
    "crypto_plugin": {
        "source": "acct",
        "subcommands": ["encrypt", "decrypt"],
    },
    "render_pipe": {
        "source": "acct",
        "subcommands": ["encrypt", "decrypt"],
    },
    "extras": {
        "source": "acct",
        "subcommands": ["state", "exec", "describe", "validate", "refresh"],
    },
    # EVBUS options
    "serialize_plugin": {
        "source": "evbus",
        "subcommands": ["exec", "describe", "state", "validate"],
    },
    # RESTORE options
    "esm_cache_file": {"positional": True, "subcommands": ["restore"]},
    # DOC options
    "ref": {
        "type": str,
        "help": "The reference on the hub to show",
        "source": "pop_tree",
        "positional": True,
        "subcommands": ["doc"],
        "nargs": "?",
    },
}

CONFIG = {
    "config": {
        "default": None,
        "help": "Load extra options from a .yaml configuration file onto hub.OPT",
    },
    "esm_plugin": {
        "default": "local",
        "help": "The esm (enforced state manager) plugin to use with a state run",
    },
    "esm_serial_plugin": {
        "default": "msgpack",
        "help": "The serial plugin used to store ESM data",
    },
    "esm_keep_cache": {
        "default": False,
        "help": "Do not delete the local ESM cache after it has been flushed to the ESM plugin",
    },
    "esm_profile": {
        "default": "default",
        "help": "The acct profile to use with the enforced state manager",
    },
    "run_name": {
        "default": "cli",
        "help": "A name for this run, this is used in internal tracking and to organize events",
    },
    "sls_sources": {
        "default": [],
        "help": "list off the sources that should be used for gathering sls files and data",
    },
    "param_sources": {
        "default": [],
        "help": "list off the sources that should be used for gathering parameter sls files",
    },
    "test": {
        "default": False,
        "help": "Set the idem run to execute in test mode. No changes will be made, idem will only detect if changes will be made in a real run.",
    },
    "tree": {
        "default": "",
        "help": "The directory containing sls files",
    },
    "params": {
        "default": "",
        "help": "The location of param.sls file containing parameter definitions",
    },
    "cache_dir": {
        "default": "/var/cache/idem",
        "help": "The location to use for the cache directory relative to the root_dir",
    },
    "root_dir": {
        "default": "/",
        "help": 'The root directory to run idem from. By default it will be "/", or in the case of running as non-root it is set to <HOMEDIR>/.idem',
    },
    "render": {
        "default": "jinja|yaml|replacements",
        "help": "The render pipe to use, this allows for the language to be specified",
    },
    "runtime": {
        "default": "parallel",
        "help": "Select which execution runtime to use. Options: 'parallel' (default), 'serial'.",
    },
    "sls": {
        "default": [],
        "help": "A space delimited list of sls refs to execute",
    },
    "exec": {
        "default": "",
        "help": "The name of an execution function to execute",
    },
    "exec_args": {
        "default": [],
        "help": "Arguments to pass to the named execution function",
    },
    "acct_profile": {
        "os": "ACCT_PROFILE",
        "help": "The profile to use when when calling exec modules and states",
        "default": "default",
    },
    "reconciler": {
        "default": "none",
        "help": "The reconciler plugin to use, 'none' by default",
    },
    "pending": {
        "default": "default",
        "help": "The pending plugin to use within the reconciler, 'default' by default",
    },
}
SUBCOMMANDS = {
    "encrypt": {
        "desc": "Use the acct subsystem to encrypt data",
        "help": "Use the acct subsystem to encrypt data",
        "source": "acct",
    },
    "decrypt": {
        "desc": "Use the acct subsystem to decrypt data",
        "help": "Use the acct subsystem to decrypt data",
        "source": "acct",
    },
    "state": {
        "desc": "Execute a specific state file or reference",
        "help": "Commands to run idempotent states",
    },
    "exec": {
        "desc": "Execute a specific execution routine",
        "help": "Commands to run execution routines",
    },
    "describe": {
        "desc": "Get an SLS representation of the account",
        "help": "Commands to run description routines",
    },
    "validate": {
        "desc": "Validate the given SLS tree and return the internal working data for the tree",
        "help": "Commands to validate SLS files",
    },
    "refresh": {
        "desc": "Update enforced state management with described resources",
        "help": "Update enforced state management with described resources",
    },
    "restore": {
        "desc": "Restore the enforced managed state from a cache file",
        "help": "Restore the enforced managed state from a cache file",
    },
    "doc": {
        "desc": "Print documentation from code",
        "help": "Print documentation from code",
    },
}
DYNE = {
    "esm": ["esm"],
    "source": ["source"],
    "idem": ["idem"],
    "exec": ["exec"],
    "log": ["log"],
    "states": ["states"],
    "tool": ["tool"],
    "output": ["output"],
    "reconcile": ["reconcile"],
    "acct": ["acct"],
}
