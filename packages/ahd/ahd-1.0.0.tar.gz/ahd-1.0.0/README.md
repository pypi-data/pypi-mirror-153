![ahd-logo](https://raw.githubusercontent.com/Descent098/ahd/master/docs/img/ahd-logo.png) 


[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Descent098/ahd/?ref=repository-badge) 


[![Downloads](https://pepy.tech/badge/ahd)](https://pepy.tech/project/ahd)

# Ad-Hoc Dispatcher

*Create ad-hoc macros to be dispatched within their own namespace.*

## Table of contents

- [What does ahd do?](#what-does-ahd-do?)
  - [Features & Roadmap](#features-&-roadmap)
    - [Path Expansion](#path-expansion)
    - [Cross Platform](#cross-platform)
    - [Dynamic Execution & Organization](#dynamic-execution-&-organization)
    - [Roadmap](#roadmap)
  - [Example use cases](#example-use-cases)
- [Why should I use ahd?](#why-should-I-use-ahd)
- [Who is ahd for?](#who-is-ahd-for)
- [Quick Start](#quick-start)
  - [Dependencies](#dependencies)
  - [Installation](#installation)
    - [From PyPi](#from-pypi)
    - [From Source](#from-source)
  - [Usage](#usage)
    - [Register](#register)
    - [Using a Registered Command](#using-a-registered-command)
    - [List](#list)
    - [Docs](#docs)
    - [Config](#config)
- [Contact/Contribute](#contact/contribute)
- [Glossary](https://ahd.readthedocs.io/en/latest/glossary/)

## Additional Documentation

This readme will give you enough information to get up and running with ahd. If you are confused about terminology used then take a look at the [glossary section](#https://ahd.readthedocs.io/en/latest/glossary/) of the docs. If you are looking for more in-depth documentation:

- Additional user and development/contribution documentation will be available at [https://ahd.readthedocs.io/en/latest/](https://ahd.readthedocs.io/en/latest/)
- API documentation is available at [https://kieranwood.ca/ahd](https://kieranwood.ca/ahd)



## What does ahd do? 

ahd allows you to take annoying to remember commands and organize them into easy to re-use macros.

## Features & Roadmap

### Path Expansion

- Macros can take full advantage of wildcards + regex to match directories. 
For example if you wanted to delete all PDFs in all folders on the desktop you can use ```sudo ahd register no-pdfs "rm *.pdf" "~/Desktop/*"```.
- *nix and windows path adages are cross-platform. For example ```~``` is converted to ```%USERPROFILE%``` on windows,  ```\``` paths are converted to ```/``` on *nix systems and vice-versa.

### Cross platform

- ahd natively supports windows and any *nix systems (including Mac OS). 
- Supports copy-paste cross platform configurations (assuming the same commands and file structure are on both)
For example if you want to write a command that git pulls in a folder called ```/development``` on your desktop using the \*nix standard ```~/Desktop/development/*``` works on both \*nix and windows.

### Dynamic Execution & Organization
- One YAML file contains the configuration for all your macros instead of being all over the place.
- Macros can be updated manually (editing the YAML file), or simply re-registered.
- The defined Paths and commands can be overwritten on each use (see [overriding](https://ahd.readthedocs.io/en/latest/usage#overriding) for details).

### Roadmap

A full roadmap for each project version can be found here: https://github.com/Descent098/ahd/projects

## Example use cases

Really the possibilities are only limited to what you can type in your regular terminal, but here are some good examples:
- Update every git repo in a directory
- Organize your downloads folder by various filetypes
- Multi-stage project compilation/build in various directories


## Why should I use ahd?

The easiest way to understand why this project is useful is with an example. Let's say you want to write a simple script to take all the PDF's in a directory and put them in a ```.7z``` archive and then remove them. Well all you need is this simple command ```7za a -t7z PDFs.7z *.pdf && rm *.pdf```...

Yeah, pretty awful to remember. Assuming we want to do this every so often let's make a script we can call. Currently with bash you need to drop the script in ```usr/bin``` (and try to remember what you called it), or add it to your bash/fish/zsh aliases (assuming you use the alias file, or ```.bashrc``` etc. if you don't), and on windows it's just not even worth it.

Enter ahd, you can register a macro (lets call it zip-pdfs) using the same annoying command, in this case ```sudo ahd register zip-pdfs "7za a -t7z PDFs.7z *.pdf && rm *.pdf" "."```. Now when we want to re-use this macro in the directory we're in you just type ```ahd zip-pdfs```. 

If you forget the name there's a list command, and if you use a longer name there's bash autocomplete (fish and zsh support coming later).

## Who is ahd for?

The primary audience is developers looking to speed up annoying workflows. However there are a number of other people it could benefit, such as:
- devops specialists; can use ahd to create a common set of macros across servers .
- dual booters; people who want one common config for multiple OS's.
- testers; if you need to execute multiple tests on various systems you can write one macro to run them all.
- etc; people who are sick of having a bunch of random scripts everywhere and want one config file for complex commands.


## Quick-start

### Dependencies

- Python 3.6+ (or is at least only tested and officially supported for 3.6+)
- pip for python



### Installation

Once you have python3 and pip you have a few installation options.



#### From Pypi

Run ```pip install ahd``` or ```sudo pip3 install ahd``` (need a network connection)

#### From source

1. Clone this repo: (https://github.com/Descent098/ahd)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory (one with setup.py)



### Usage

```bash
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
```

#### Register

The register command allows you to register a command to be used later on. 

<u>Required Arguments:</u>

- *\<name\>*;  This is a **positional** placeholder value for the name of a command you  are registering. Once the command is registered you can run it by using ```ahd <name>```.

- *\<command\>*;  This is a **positional** placeholder value for the macro you want to run when the command is used after being registered. For example if you wanted to delete all the PDF's in a directory the macro you would normally run is ```rm *.pdf``` and so you would do ```ahd register <name> "rm *.pdf" <paths>```. 

  It is generally advised to use encapsulating quotes since this avoids argument parsing artifacts.

- *\<paths\>*;  This is a **positional** placeholder value for the path(s) that you want the command to run the macro in by default. For example if you wanted to a command to execute a macro on the desktop when it's run you can do ```ahd register <name> <command> "~/Desktop"```.

  It is generally advised to use encapsulating quotes since this avoids argument parsing artifacts. Additionally you can specify multiple directories through comma delimiting, for example: ```ahd register <name> <command> "~/Desktop, ~/Documents, ~/Pictures"```, or you can use **path expansion** which will match directories through regex or wildcards. For example to run a command in all directories **within** the desktop you could do ```ahd register <name> <command> "~/Desktop/*"``` or just use regex to match paths more explicitly for example to only include folders on the desktop that are numbers between 0-9 you could do: ```ahd register <name> <command> "~/Desktop/[0-9]"```.



#### Using a Registered Command

You can use a registered command by simply typing ```ahd <name>```, where ```<name>``` is whatever name you gave to the command.

<u>Optional Arguments:</u>

- *\<command\>*; This is an optional positional argument that lets you overwrite the command, while retaining the registered paths. For example lets say you have a set of paths registered with a command that typically runs ```git pull``` over the specified paths. You want to run a different command on the paths (lets say remove all the pdfs in the folder) You can do: ```ahd <name> "rm *.pdf"``` which will execute ```rm *.pdf``` instead of ```git pull``` on the defined paths.

  It is generally advised to use encapsulating quotes since this avoids argument parsing artifacts.
- *\<paths\>*; This is an optional positional argument that lets you overwrite the paths the command will run against. To retain the original command you must use a ".". So for example lets say you have a command registered that runs ```git pull``` against ```~/Desktop/*```, but now you want to run ```git pull``` against ```~/Documents/*``` you can use ```ahd <name> "." "~/Documents/*"``` and it will run the macro against ```~/Documents/*``` instead of ```~/Desktop/*```

  It is generally advised to use encapsulating quotes since this avoids argument parsing artifacts. Additionally you can specify multiple directories through comma delimiting, for example: ```ahd register <name> <command> "~/Desktop, ~/Documents, ~/Pictures"```, or you can use **path expansion** which will match directories through regex or wildcards. For example to run a command in all directories **within** the desktop you could do ```ahd register <name> <command> "~/Desktop/*"``` or just use regex to match paths more explicitly for example to only include folders on the desktop that are numbers between 0-9 you could do: ```ahd register <name> <command> "~/Desktop/[0-9]"```.



#### list

The list command shows a list of your current registered commands.

<u>Optional Arguments:</u>

- *\-l or \-\-long*: Shows all commands in configuration with the registered paths and macros.



#### docs

The docs command is designed to bring up documentation as needed, you can run ```ahd docs``` to open the documentation site in the default browser.



<u>Optional Arguments:</u>

- *\-a or \-\-api*: Used to serve local API documentation (Not yet implemented)

- *\-o or \-\-offline*: Used to serve local user documentation (Not yet implemented)



#### config

This command is used for configuration management. It is recomended to use [register](#register) to register/update commands. The config command is for managing configurations manually take a look at the documentation for details about [manual configuration](https://ahd.readthedocs.io/en/latest/usage#wildcards-and-cross-platform-paths).



<u>Optional Arguments:</u>

  \-e \-\-export: Export the current configuration file (called ```ahdconfig.yml```)

  \-i \-\-import: Import a configuration file; takes the path to the config file as an argument



## Contact/Contribute

For a full contribution guide, check the [contribution section of the documentation](https://ahd.readthedocs.io/en/latest/contributing/). Also be sure to check the [faq](https://ahd.readthedocs.io/en/latest/faq/) before submitting issues.

For any additional questions please submit then through github [here](https://github.com/Descent098/ahd/issues/new?assignees=Descent098&labels=documentation&template=question.md&title=%5Bquestion%5D) (much faster response), or my email [kieran@canadiancoding.ca](mailto:kieran@canadiancoding.ca?subject=AHD:Question).


