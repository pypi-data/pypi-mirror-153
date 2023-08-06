"""Contains all the configuration for the package on pip"""
import setuptools
from ahd.__init__ import __version__ as version

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string

    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "ahd",
    version = version,
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "Create ad-hoc macros to be dispatched in their own namespace.",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    project_urls = {
        "User Docs" :      "https://ahd.readthedocs.io/en/latest/",
        "API Docs"  :      "https://kieranwood.ca/ahd",
        "Source" :         "https://github.com/Descent098/ahd",
        "Bug Report":      "https://github.com/Descent098/ahd/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D",
        "Feature Request": "https://github.com/Descent098/ahd/issues/new?assignees=Descent098&labels=enhancement&template=feature_request.md&title=%5BFeature%5D",
        "Roadmap":         "https://github.com/Descent098/ahd/projects"
    },
    include_package_data = True,
    packages = setuptools.find_packages(),
    entry_points = { 
            'console_scripts': ['ahd = ahd.cli:main']
        },
    install_requires = [
    "docopt", # Used for argument parsing
    "colored",# Used to color terminal output
    "pyyaml", # Used for configuration parsing
    "fuzzywuzzy", # Used for fuzzy string matching
    "python-Levenshtein", # Used to optimize string matching
    "mkdocs", # Used to create HTML versions of the markdown docs in the docs directory
    "pdoc3", # Used for building API documentation
        ],
    extras_require = {
        "dev" : ["nox",   # Used to run automated processes
                "pytest", # Used to run the test code in the tests directory
                ],

    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
)
