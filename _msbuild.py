import os
from pymsbuild import *

# See https://packaging.python.org/en/latest/specifications/core-metadata/ for fields
METADATA = {
    "Metadata-Version": "2.1",
    "Name": "pymsbuild-winui",
    "Version": "1.0",
    "Author": "Steve Dower",
    "Author-email": "steve.dower@python.org",
    "Home-page": "https://github.com/zooba/pymsbuild-winui",
    "Project-url": [
        "Bug Tracker, https://github.com/zooba/pymsbuild-winui",
    ],
    "Summary": "A WinUI extension for PyMSBuild",
    "Description": File("README.md"),
    "Description-Content-Type": "text/markdown",
    "Keywords": "your,keywords,go,here",
    "Classifier": [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Compilers",
        "Topic :: Utilities",
    ],
    "Requires-Dist": [
        "pymsbuild>=1.0.0b7",
        "pybind11",
        "jinja2",
    ],

    # Semi-universal, we only build once per OS
    "WheelTag": "py3-none-win32.win_amd64",

    #"BuildSdistRequires": [],
    #"BuildWheelRequires": [],
}


PACKAGE = Package(
    'pymsbuild_winui',
    PyFile('pymsbuild_winui/*.py'),
    Package(
        'targets',
        File('pymsbuild_winui/targets/*'),
    ),
    Package(
        'templates',
        File('pymsbuild_winui/templates/*'),
    ),
)


def init_METADATA():
    version = os.getenv("BUILD_BUILDNUMBER")
    ghref = os.getenv("GITHUB_REF")
    if ghref:
        version = ghref.rpartition("/")[2]
    if version:
        METADATA["Version"] = version


def init_PACKAGE(tag=None):
    pass
