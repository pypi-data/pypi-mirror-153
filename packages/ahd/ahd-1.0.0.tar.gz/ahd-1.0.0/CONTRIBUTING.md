# Contribution & Development Guide

Here is everything you need to know about getting started for contributing to the project (thanks for doing so by the way).



## Development guide



### Getting dev dependencies

To grab the specified development dependencies simply run ```pip install adh[dev]```, this will grab everything you need.



If for some reason this does not work, here are a list of development dependencies:

```
nox    # Used to run automated processes
pytest # Used to run the test code in the tests directory
mkdocs # Used to create HTML versions of the markdown docs in the docs directory
```



### Building "API" docs

API docs are useful if you want an easily navigatable version of the in-line documentation. The best way to do this currently is to download [pdoc3](https://pdoc3.github.io/pdoc/doc/pdoc/); ```pip install pdoc3``` then (assuming ahd is installed) run ````pdoc ahd --http localhost:8080`. Go to a browser and type in [http://localhost:8080/ahd](http://localhost:8080/ahd).



### Nox integration

If you have never used [nox](https://nox.readthedocs.io/) before it is a great system for automating tedius tasks (builds, distributions, testing etc). This project uses nox for a number of things and in the following sections I will explain each. 



#### Running tests

Testing is implemented using [pytest](https://docs.pytest.org/en/latest/), and can be run 1 of 2 ways:

1. Run the tests through nox using ```nox -s tests```, this will automatically run the tests against python 3.5-3.8 (assuming they are installed on system).
2. Go to the root directory and run ```pytest```, this should automatically detect the /tests folder and run all tests.



#### Building the package

This is not necessary for pull requests, or even development but if you want to validate that it doesn't break buildability here is how to do it. You can use ```nox -s build```, this will create a source distribution for you using pythons [setuptools module](https://setuptools.readthedocs.io/en/latest/).



## Contribution guide

### TLDR

1. Commenting/documentaion is **not** optional
2. Breaking platform compatability is **not** acceptable
3. Do **everything** through [github](https://github.com/Descent098/ahd) (don't email me), and (mostly) everything has been setup for you.



### Bug Reports & Feature Requests

Submit all bug reports and feature requests on [github](https://github.com/Descent098/ahd/issues/new/choose), the format for each is pre-defined so just follow the outlined format



### Pull requests

Pull requests should be submitted through github and follow the default pull request template specified. If you want the rundown of what needs to be present:

1. Provide a clear explination of what you are doing/fixing
2. Feature is tested on Windows & *nix (unless explicitly incompatable)
3. All Classes, modules, and functions must have docstrings that follow the [numpy-style guide](https://numpydoc.readthedocs.io/en/latest/format.html).
4. Unless feature is essential it cannot break backwards compatability
