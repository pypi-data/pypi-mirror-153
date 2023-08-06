# Changelog

## V 1.0.0; June 6th 2022

**The version was bumped to a major release because pre V0.5.0 configs have been fully deprecated, if you are using an old config see migration steps below**

There are 3 primary focuses for this release:

1. Improve developer/contributor documentation and infrastructure
2. Add metadata to configs so you can review how you use ahd
3. Finalize some features that make ahd more intuitive and simple to use

Features:

- Added spell-check for suggestions when input is close to a valid command
- Added additional metadata to config file for each entry:
  - `updated`: The datestamp when the command was updated (will update on re-registering)
  - `created`: The datestamp when the command was created (will not update on re-registering)
  - `runs`: The number of times a command has been run
  - `last_run`: The datestamp when the command was last run (initially "never")
- Added `-d` flag to display command details
  - Added command metadata for usage details like how many times it's been run and when it was added (access using `ahd <command> -d`)
  - Also will provide details like the current config for a given command, similar to `ahd list` but for a single command
- Updated testing to run on a schedule for quicker bug awareness
- Updated testing for coverage of all modules
- Allowed for globbing paths with files
  - for example you can run a command over all files by extension in a path using `ahd register <command name> "<command>" "/path/*.<extension>"`

Documentation:

- Added documentation about removing migration for pre `V0.5.0` configurations

Bug Fixes:

- Fixed errors in testing pipeline
- Fixed bugs with initializing a config file
- Added missing reserved commands to autocomplete
- Fixed bugs on *nix installs without bash
- Fixed several bugs with escaping on *nix systems

Migrating old configs:

in order to migrate old configs install ahd v0.5.0 `pip install --upgrade ahd==0.5.0` then follow guide here (ignore step 1): [Migrating from Pre v0.5.0 configs - Ad-Hoc Dispatcher (ahd.readthedocs.io)](https://ahd.readthedocs.io/en/v0.5.0/migration/)

Once updated to new config reinstall latest version using `pip install --upgrade ahd`

## V 0.5.0; August 22nd 2020

Focus for this release was to make it easier to understand how to use and contribute to ahd, to convert from configparser to PyYaml and cleanup some left over errors in deepsource.

Features:

- Replaced configparser with [PyYaml](https://pyyaml.org/); see migration notice in the docs for details

Documentation:

- Overhauled user documentation site for clarity
  - Revamped README
  - Added Glossary
  - Revamped contribution guide
  - Added Code Style guide
  - Cleaned up wording surrounding what the project actually does
- Transitioned from full roadmap project boards to per-release project boards

Bug Fixes:

- Inability to build from sdist due to missing files; Thanks to [thatch](https://github.com/thatch) for the fix
- Fixed testing pipeline in github actions

## V 0.4.0; February 10th 2020

Focus for this release was breaking up command line parsing into more testable chunks.

Features:

- All argument parsing is now based on discrete functions
- Added a list command to show your current available commands

Documentation:

- Created API documentation site: https://kieranwood.ca/ahd

## V 0.3.0; February 6th 2020

Focus for this release was on building sustainable development pipelines (logging, testing etc.), and making the project more reliable in edge cases and error handling.

Features:

- Built out the testing suite to be run before release
- Built out the logging mechanism for debugging
- Introduced many error catches for various issues.

Bug Fixes:

- Added config command to bash autocomplete

## V 0.2.1; February 2nd 2020

- Added support for . as current directory path
- Fixed issue with being unable to import configuration files
- Fixed issue with docs command when running --api

## V 0.2.0; February 2nd 20202

Focus was on improving the overall useability of ahd. Note this version breaks backwards compatibility, but includes a migration guide in the docs (to be removed in V0.3.0).

Features:

- Bash Autocomplete implemented (ZSH and fish to come)
- Ability to export configuration
- Ability to import configuration
- Added a top level "docs" command to easy access documentation
- Added cross-platform wildcard support (see docs for usage)
- Added cross-platform home directory (see docs for details)

Bug fixes:

- Fixed issue where running "register" command without any flags would error out instead of printing help info
- Fixed issue with relative path tracking

Documentation improvements:

- Added issue templates for bug reports and feature requests
- Added pull request templates
- Added contribution guide
- Added migration information
- Added relevant documentation for all features released in V0.2.0

## V 0.1.0; January 28th 2020

Initial release focused on creating the basic functionality for the ahd command.

Features:

- Ability to register a command
- Ability to specify command to run
- Ability to specify the location(s) to run the command in.
- Have commands store to a configuration file using configparser
