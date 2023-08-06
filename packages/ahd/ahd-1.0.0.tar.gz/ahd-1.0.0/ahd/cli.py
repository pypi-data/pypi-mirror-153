"""This file houses the primary entrypoint, and main business logic of ahd.

Module Variables
----------------

usage (str):
    Used by docopt to setup argument parsing;
    Defines the actual command line interface

config(dict):
    The dictionary containing the current configuration
    once deserialized from CONFIG_FILE_PATH

CONFIG_FILE_PATH(str):
    The path to the configuration file

CURRENT_PATH(str):
    Used to keep track of users current directory
    to cd back into it after script execution

Module Functions
----------------
main():
    The primary entrypoint for the ahd script handles argument parsing

list_macros(verbose:bool = False, config:dict={}):
    Lists commands currently in config

docs(api:bool = False, offline:bool = False):
    Processes incoming arguments when the docs command is invoked

dispatch(name, command:str=False, paths:str=False, config:dict={}):
    Controls the dispatching of macros

Notes
-----
While you an invoke functions directly it is recommended to use the CLI 

Documentation
-------------
User docs website: https://ahd.readthedocs.io
API Docs website: https://kieranwood.ca/ahd
Source Code: https://github.com/Descent098/ahd
Roadmap: https://github.com/Descent098/ahd/projects
"""

# Standard lib dependencies
import datetime
import os                                      # Used primarily to validate paths
import sys                                     # Used to check length of input arguments
import glob                                    # Used to preprocess wildcard paths
import logging                                 # Used to log valueable logging info
import webbrowser                              # Used to auto-launch the documentation link
import subprocess                              # Used to run the dispatched commands


# Internal dependencies
from .configuration import configure, register, CONFIG_FILE_PATH
from .__init__ import __version__ as version


# Third-party dependencies
import colored                                 # Used to colour terminal output
import yaml                                    # Used to handle configuration serialization/deserialization
from docopt import docopt                      # Used to parse arguments and setup POSIX compliant usage info
from fuzzywuzzy import process as suggest_word # Used to parse word similarity for incorrect spellings


usage = """Add-hoc dispatcher

Create ad-hoc commands to be dispatched within their own namespace.

Usage: 
    ahd [-h] [-v]
    ahd list [-l]
    ahd docs [-a] [-o]
    ahd config [-e] [-i CONFIG_FILE_PATH]
    ahd register <name> [<command>] [<paths>]
    ahd <name> [<command>] [<paths>] [-d]

Options:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -l, --long            Shows all commands in configuration with paths and commands
    -a, --api             shows the local API docs
    -o, --offline         shows the local User docs instead of live ones
    -e, --export          exports the configuration file
    -i CONFIG_FILE_PATH, --import CONFIG_FILE_PATH 
                        imports the configuration file
    -d, --details         prints the details of a command
    """

config = {}  # The dictionary containing the current configuration once deserialized from CONFIG_FILE_PATH

CURRENT_PATH = os.curdir # Keeps track of current directory to return to after executing commands

def main() -> None:
    """The primary entrypoint for the ahd script handles argument parsing

    All primary business logic is within this function."""
    # Setup arguments for parsing
    arguments = docopt(usage, version=f"ahd V{version}")

    if len(sys.argv) == 1:
        print("\n", usage)
        sys.exit()

    if os.path.exists(CONFIG_FILE_PATH): # If the file already exists
        with open(CONFIG_FILE_PATH, "r") as config_file:
            config = yaml.safe_load(config_file)
            config = dict(config)

    else: # If a file does not exist create one
        print(f"{colored.fg(1)}Could not locate valid config file creating new one at {CONFIG_FILE_PATH} {colored.fg(15)}")
        with open(CONFIG_FILE_PATH, "w") as config_file:
            config_file.write("macros:")
            config = {"macros": {}}

    # Begin argument parsing

    if arguments["list"]:
        list_macros(arguments["--long"], config)
        sys.exit()

    # ========= Docs argument parsing =========
    if arguments["docs"]:
        docs(arguments["--api"], arguments["--offline"])
        sys.exit()

    # ========= config argument parsing =========
    if arguments["config"]:
        configure(arguments["--export"], arguments["--import"], config)
        sys.exit()

    # ========= preprocessing commands and paths =========
    if not arguments["<paths>"]:
        logging.debug("No paths argument registered setting to \'\'")
        arguments["<paths>"] = ""
    else:
        arguments["<paths>"] = _preprocess_paths(arguments["<paths>"])

    if not arguments["<command>"]:
        logging.debug("No command argument registered setting to \'\'")
        arguments["<command>"] = ""

    if "." == arguments["<command>"]: # If <command> is . set to specified value
        logging.debug(f". command registered, setting to {config['macros'][arguments['<name>']]['command']}")
        arguments["<command>"] = config["macros"][arguments["<name>"]]["command"]

    # ========= register argument parsing =========
    if arguments["register"]:
        register(arguments["<name>"], arguments["<command>"], arguments["<paths>"], config)

    # ========= User command argument parsing =========

    if arguments['<name>']:
        if arguments["--details"]:
            try:
                config['macros'][arguments['<name>']] # Force a KeyError if the macro does not exist
                print(f"{colored.fg(6)}{arguments['<name>']}{colored.fg(15)}\n")
                print(f"\tCommand = {config['macros'][arguments['<name>']]['command']}")
                print(f"\tPaths = {config['macros'][arguments['<name>']]['paths']}")
                if config['macros'][arguments['<name>']].get("runs", False):
                    print(f"\tRuns = {config['macros'][arguments['<name>']]['runs']}")
                if config['macros'][arguments['<name>']].get("created", False):
                    print(f"\tCreated = {config['macros'][arguments['<name>']]['created']}")
                if config['macros'][arguments['<name>']].get("updated", False):
                    print(f"\tUpdated = {config['macros'][arguments['<name>']]['updated']}")
                if config['macros'][arguments['<name>']].get("last_run", False):
                    print(f"\tLast Run = {config['macros'][arguments['<name>']]['last_run']}")
                exit()
            except KeyError:
                ... # If the command is not registered, do nothing and let the dispatch spellchecker find it                
        if not arguments['<paths>'] and not arguments['<command>']:
            dispatch(arguments['<name>'], config=config)

        else:
            if arguments['<paths>'] and not arguments['<command>']: 
                # Process inputted paths
                arguments['<paths>'] = _preprocess_paths(arguments['<paths>'])
                arguments['<paths>'] = _postprocess_paths(arguments['<paths>'])
                dispatch(arguments['<name>'], paths = arguments['<paths>'], config=config)

            if arguments['<command>'] and not arguments['<paths>']:
                dispatch(arguments['<name>'], command = arguments['<command>'], config=config)

            else:
                # Process inputted paths
                arguments['<paths>'] = _preprocess_paths(arguments['<paths>'])
                arguments['<paths>'] = _postprocess_paths(arguments['<paths>'])
                dispatch(arguments['<name>'], paths = arguments['<paths>'], command = arguments['<command>'], config=config)


def list_macros(verbose:bool = False, config:dict={}) -> None:
    """Lists commands currently in config

    Parameters
    ----------
    verbose: (bool)
        When specified will print both the command name and
        associated commands + paths. Additionally the dictionary
        will only return when this flag is specified.

    config: (dict)
        The dict that contains the current config
    """

    # Iterate over the config, and pull information about the macros
    count = 0
    for count, macro in enumerate(config["macros"]):
        if verbose:
            print(f"{colored.fg(6)}{macro}{colored.fg(15)}\n")
            try:
                print(f"\tCommand = {config['macros'][macro]['command']}")
                print(f"\tPaths = {config['macros'][macro]['paths']}")
            except KeyError:
                print(f"Macro {macro} is not configured correctly, check the command and paths variables")
                sys.exit(1)
            if config['macros'][macro].get("runs", False):
                print(f"\tRuns = {config['macros'][macro]['runs']}")
            if config['macros'][macro].get("created", False):
                print(f"\tCreated = {config['macros'][macro]['created']}")
            if config['macros'][macro].get("updated", False):
                print(f"\tUpdated = {config['macros'][macro]['updated']}")
            if config['macros'][macro].get("last_run", False):
                print(f"\tLast Run = {config['macros'][macro]['last_run']}")
        else:
            print(f"\n{colored.fg(6)}{macro}{colored.fg(15)}")
    print(f"\n\n{count+1} macros detected")


def docs(api:bool = False, offline:bool = False) -> None:
    """Processes incoming arguments when the docs command is invoked

    Parameters
    ----------
    api: (bool)
        When specified, shows API docs as opposed to user docs.

    offline: (bool)
        When specified will build local copy of docs instead of going to website

    Notes
    -----
    - By Default user documentation is selected
    - By default the online documentation is selected
    """
    if not api and not offline:
        webbrowser.open_new("https://ahd.readthedocs.io")
    else:
        if offline and not api:
            from mkdocs.commands import serve # Used to serve the user documentation locally
            print("Docs available at http://localhost:8000/")
            webbrowser.open_new("http://localhost:8000/")
            serve.serve()

        elif api:
            if not offline:
                webbrowser.open_new("https://kieranwood.ca/ahd")
            else:
                # Simulates `pdoc --http : ahd`
                from pdoc.cli import main as pdoc_main # Used to serve the api documentation locally
                sys.argv = [sys.argv[0], "--http", ":", "ahd"]
                webbrowser.open_new("http://localhost:8080/ahd")
                pdoc_main()


def dispatch(name, command:str=False, paths:str=False, config:dict={}) -> None:
    """Controls the dispatching of macros

    Parameters
    ----------
    name: (str)
        The name of the macro to dispatch

    command: (str)
        Used to override the macros configured command
        when set to False, will pull from configuration

    paths: (str)
        Used to override the macros configured paths
        when set to False, will pull from configuration

    config: (dict)
        The dict that contains the current config"""
    if "register" == name:
                print(usage)
                sys.exit()
    logging.info(f"Beggining execution of {name}")

    try: # Accessing stored information on the command
        config["macros"][name]
        if not config["macros"][name].get("runs", False):
            config["macros"][name]["runs"] = 1
        else:
            config["macros"][name]["runs"] += 1
        config["macros"][name]["last_run"] = str(datetime.datetime.now())[:10:]

        with open(CONFIG_FILE_PATH, "w+") as config_file:
            yaml.dump(config, config_file, default_flow_style=False) # Update config file with new metadata

    except KeyError: # When command does not exist in config
        if not config.get("macros", False):
            print(f"{colored.fg(1)}No macros found in current config {colored.fg(15)}\n")
            sys.exit(1)
        commands = [current_command for current_command in config["macros"]] # Get list of commands in config
        error_threshold = 60 # The percentage of likelyhood before similar words will throw out result
        similar_words = suggest_word.extractBests(name, commands,score_cutoff=error_threshold , limit=3) # Generate word sugestions
        if not similar_words: # If there are not similar commands that exist in the config
            print(f"{colored.fg(1)}Could not find macro {colored.fg(15)}{name}{colored.fg(1)} or any valid suggestions with %{error_threshold} or higher likelyhood, please check spelling {colored.fg(15)}\n")
            sys.exit(1)

        # Suggestions found for similar commands
        suggestions = ""
        for index, word in enumerate(similar_words):
            suggestions+= f"\t{index+1}. {colored.fg(3)}{word[0]}{colored.fg(15)}  | %{word[1]} likelyhood\n"
        print(f"{colored.fg(1)}No command {name} found {colored.fg(15)} here are some suggestions: \n{suggestions}")
        if not command:
            command = ""
        if not paths:
            paths = ""
        print(f"Most likely suggestion is {colored.fg(3)}{similar_words[0][0]}{colored.fg(15)} rerun using: \n\t> ahd {similar_words[0][0]} \"{command}\" \"{paths}\"")
        sys.exit(1)
    
    if not command or command == ".":
        command = config["macros"][name]['command']
    
    if not paths:
        paths = _postprocess_paths(config["macros"][name]['paths'])

    if len(paths) > 1:
        for current_path in paths:
            if os.name == "nt":
                current_path = current_path.replace("~", os.getenv('USERPROFILE'))
                current_path = current_path.replace("/", f"{os.sep}")
            if os.path.isdir(current_path):
                print(f"Running: cd {current_path} && {command} ".replace("\'",""))
                subprocess.Popen(f"cd {current_path} && {command} ".replace("\'",""), shell=True)
            elif os.path.isfile(current_path):
                print(f"Running: {command} {current_path}".replace("\'",""))
                subprocess.Popen(f"{command} {current_path}".replace("\'",""), shell=True)

    else: # if only a single path is specified instead of a 'list' of them
        current_path = paths[0]
        if os.name == "nt":
            current_path = current_path.replace("~", os.getenv('USERPROFILE'))
            current_path = current_path.replace("/", f"{os.sep}")
        if os.path.isdir(current_path):
            print(f"Running: cd {paths[0]} && {command} ".replace("\'",""))
            subprocess.Popen(f"cd {paths[0]} && {command} ".replace("\'",""), shell=True)
        elif os.path.isfile(current_path):
            print(f"Running: {command} {current_path}".replace("\'",""))
            subprocess.Popen(f"{command} {current_path}".replace("\'",""), shell=True)


def _preprocess_paths(paths:str) -> str:
    """Preprocesses paths from input and splits + formats them
    into a useable list for later parsing.

    Example
    -------
    ```
    paths = '~/Desktop/Development/Canadian Coding/SSB, C:\\Users\\Kieran\\Desktop\\Development\\*, ~\\Desktop\\Development\\Personal\\noter, .'

    paths = _preprocess_paths(paths)

    print(paths) # Prints: '~/Desktop/Development/Canadian Coding/SSB,~/Desktop/Development/*,~/Desktop/Development/Personal/noter,.'
    ```
    """
    logging.info(f"Beginning path preprocessing on {paths}")
    result = paths.split(",")
    for index, directory in enumerate(result):
        directory = directory.strip()
        logging.debug(f"Directory: {directory}")
        if directory.startswith(".") and (len(directory) > 1):
            directory = os.path.abspath(directory)
        if "~" not in directory:
            if os.name == "nt":
                directory = directory.replace(os.getenv('USERPROFILE'),"~")

            else:
                directory = directory.replace(os.getenv('HOME'),"~")
            directory = directory.replace("\\", "/")
            result[index] = directory
        else:
            directory = directory.replace("\\", "/")
            result[index] = directory

    logging.debug(f"Result: {result}")
    result = ",".join(result)

    return result


def _postprocess_paths(paths:str) -> list:
    """Postprocesses existing paths to be used by dispatcher.

    This means things like expanding wildcards, and processing correct path seperators.

    Example
    -------
    ```
    paths = 'C:\\Users\\Kieran\\Desktop\\Development\\Canadian Coding\\SSB, C:\\Users\\Kieran\\Desktop\\Development\\Canadian Coding\\website, ~/Desktop/Development/Personal/noter, C:\\Users\\Kieran\\Desktop\\Development\\*'

    paths = _preprocess_paths(paths)

    print(_postprocess_paths(paths)) 
    # Prints: ['C:/Users/Kieran/Desktop/Development/Canadian Coding/SSB', ' C:/Users/Kieran/Desktop/Development/Canadian Coding/website', ' C:/Users/Kieran/Desktop/Development/Personal/noter', 'C:/Users/Kieran/Desktop/Development/Canadian Coding', 'C:/Users/Kieran/Desktop/Development/Personal', 'C:/Users/Kieran/Desktop/Development/pystall', 'C:/Users/Kieran/Desktop/Development/python-package-template', 'C:/Users/Kieran/Desktop/Development/Work']
    ```
    """
    logging.info(f"Beginning path postprocessing on {paths}")

    paths = paths.split(",")
    result = []
    for directory in paths:
        directory = directory.strip()

        if os.name == "nt":
            directory = directory.replace("/", "\\")

        if directory.startswith("."):
            try:
                if directory[1] == "/" or directory[1] == "\\":
                    directory = f"{os.curdir}{directory[1::]}"
            except IndexError:
                directory = os.path.abspath(".")

        if "~" in directory:
            if os.name == "nt":
                directory = directory.replace("~",f"{os.getenv('USERPROFILE')}")
            else:
                directory = directory.replace("~", f"{os.getenv('HOME')}")
        if "*" in directory:

            wildcard_paths = glob.glob(directory.strip())

            for wildcard_directory in wildcard_paths:
                wildcard_directory = wildcard_directory.replace("\\", "/")
                result.append(wildcard_directory)
        else:
            result.append(directory)

    logging.debug(f"Result: {result}")
    return result


if __name__ == "__main__":
    main()
