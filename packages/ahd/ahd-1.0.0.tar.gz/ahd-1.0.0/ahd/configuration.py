"""This file houses functions related to configuration management

Module Variables
----------------

CONFIG_FILE_PATH(str):
    The path to the configuration file

CURRENT_PATH(str):
    Used to keep track of users current directory
    to cd back into it after script execution

command_list(list[namedtuple]):
    A list of all the root commands baked into
    ahd for autocompletion generation

Module Functions
----------------
configure(export:bool=False, import_config:bool=False, config:dict={}):
    Handles all the exporing and importing of configurations

register(macro_name:str, commands:str, paths:str, config:dict={}):
    Handles registering of custom commands, and autocompletion generation
"""
import os                              # Used primarily to validate paths
import sys                             # Used to safely exit interpreter session
import datetime

# Internal dependencies
from .autocomplete import command, generate_bash_autocomplete

# Third-party dependencies
import colored                         # Used to colour terminal output
import yaml                            # Used to handle configuration serialization/deserialization

# The default (and currently only) path to the configuration file
CONFIG_FILE_PATH = f"{os.path.dirname(__file__)}{os.sep}ahd.yml"

CURRENT_PATH = os.curdir  # Keeps track of current directory to return to after executing commands

command_list = [  # Used for autocompletion generation
    command("docs", ["-a", "--api", "-o", "--offline"]),
    command("register", []),
    command("config", ["-e", "--export", "-i", "--import"]),
    command("list", ["-l", "--long"]),
]


def configure(export:bool=False, import_config:bool=False, config:dict={}) -> None:
    """Handles all the exporing and importing of configurations

    Parameters
    ----------
    export: (bool)
        When specified will export the current configuration to the cwd

    import_config: (bool|str)
        False if no path, otherwise a string representation of path to config file.

    config: (dict)
        The dict that contains the current config

    Notes
    -----
    - If neither export or import_config are specified, then usage is printed.
    """

    if not export and not import_config:
        print("Please provide either the export (-e or --export) or import (-i or --import) flag")
        sys.exit(1)
    if export:
        print(f"Exporting configuration from {CONFIG_FILE_PATH} to {os.path.abspath(CURRENT_PATH)}{os.sep}ahd.yml")
        with open(CONFIG_FILE_PATH) as config_file:
            config = yaml.safe_load(config_file)
            with open(f"{os.path.abspath(CURRENT_PATH)}{os.sep}ahd.yml", "w") as export_file:
                yaml.dump(config, export_file, default_flow_style=False)

    if import_config:
        try:
            with open(import_config, "r") as config_file:  # Read new config file
                new_config = yaml.safe_load(config_file)
            print(f"Importing {os.path.abspath(import_config)} to {CONFIG_FILE_PATH}")
            os.remove(CONFIG_FILE_PATH)
            with open(CONFIG_FILE_PATH, "w") as config_file:
                yaml.dump(new_config, config_file, default_flow_style=False)
            
        except PermissionError:
            print(f"{colored.fg(1)} Unable to import configuration file, are you sudo?")
            print(f"{colored.fg(15)}\tTry running: sudo ahd config -i \"{import_config}\" ")

def register(macro_name:str, commands:str, paths:str, config:dict={}) -> None:
    """Handles registering of custom commands, and autocompletion generation.

    Parameters
    ----------
    macro_name: (str)
        The name used to call the macro.

    commands: (str)
        The set of commands the macro should execute.
    
    paths: (str)
        A string representation of the paths to execute the command with.

    config: (dict)
        The dict that contains the current config

    Notes
    -----
    - When passing paths to this function make sure they are preprocessed.
    """
    print(f"Registering macro {macro_name} \n\tCommand: {commands} \n\tPaths: {paths}")
    if macro_name in ["docs", "register", "config", "list"]: # If macro name is reserved
        raise ValueError(f"{macro_name} is a reserved macro name")
    try:
        config["macros"][macro_name] = {
            "command": commands,
            "paths": paths,
            "updated": str(datetime.datetime.now())[:10:]
        }
        if not config["macros"][macro_name].get("created", False):
            config["macros"][macro_name]["created"] = str(datetime.datetime.now())[:10:]
        if not config["macros"][macro_name].get("runs", False):
            config["macros"][macro_name]["runs"] = 0
        if not config["macros"][macro_name].get("last_run", False):
            config["macros"][macro_name]["last_run"] = "never"
    except KeyError:  # If the configuration is empty
        config["macros"] = {}
        config["macros"][macro_name] = {
            "command": commands,
            "paths": paths,
            "updated": str(datetime.datetime.now())[:10:]
        }
        if not config["macros"][macro_name].get("created", False):
            config["macros"][macro_name]["created"] = str(datetime.datetime.now())[:10:]
        if not config["macros"][macro_name].get("runs", False):
            config["macros"][macro_name]["runs"] = 0
        if not config["macros"][macro_name].get("last_run", False):
            config["macros"][macro_name]["last_run"] = "never"

    try:
        print(f"Begin writing config file to {CONFIG_FILE_PATH}")
        with open(CONFIG_FILE_PATH, "w") as config_file:
            yaml.dump(config, config_file, default_flow_style=False)
        print(f"Configuration file saved {macro_name} registered")
    except PermissionError:
        print(f"{colored.fg(1)}Unable to register command are you sudo?")
        print(f"{colored.fg(15)}\tTry running: sudo ahd register {macro_name} \"{commands}\" \"{paths}\" ")

    if not os.name == "nt":  # Generate bash autocomplete
        for custom_command in config["macros"]:
            command_list.append(command(custom_command, []))

        autocomplete_file_text = generate_bash_autocomplete(command_list)
        try:
            with open("/etc/bash_completion.d/ahd.sh", "w+") as autocomplete_file:
                autocomplete_file.write(autocomplete_file_text)
            print("Bash autocompletion file written to /etc/bash_completion.d/ahd.sh \nPlease restart shell for autocomplete to update")
        except PermissionError:
            print(f"{colored.fg(1)}Unable to write bash autocompletion file are you sudo?")
        except FileNotFoundError:
            print(f"{colored.fg(1)}Unable to write bash autocompletion file, file was not found")

    # Since executing commands requires changing directories, make sure to return after
    os.chdir(CURRENT_PATH)
    sys.exit()
