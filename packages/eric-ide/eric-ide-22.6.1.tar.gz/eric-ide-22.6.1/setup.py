#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module to prepare a distribution package for uploading to PyPI.
"""

import os
import sys
import subprocess                   # secok
import shutil
import fnmatch
import datetime
import json
import contextlib

from setuptools import setup, find_packages

installInfoName = "eric7installpip.json"

######################################################################
## some helper functions below
######################################################################


def getVersion():
    """
    Function to get the version from file.
    
    @return string containing the version
    @rtype str
    """
    version = "<unknown>"
    if sys.argv[-1].startswith(("1", "2")):
        # assume it is a version info starting with year
        version = sys.argv[-1]
        del sys.argv[-1]
    else:
        # calculate according our version scheme (year.month)
        today = datetime.date.today()
        version = "{0}.{1}".format(today.year - 2000, today.month)
    return version


def getPackageData(package, extensions):
    """
    Function to return data files of a package with given extensions.
    
    @param package name of the package directory
    @type str
    @param extensions list of extensions to test for
    @type list of str
    @return list of package data files
    @rtype list of str
    """
    filesList = []
    for dirpath, _dirnames, filenames in os.walk(package):
        for fname in filenames:
            if (
                not fname.startswith('.') and
                os.path.splitext(fname)[1] in extensions
            ):
                filesList.append(
                    os.path.relpath(os.path.join(dirpath, fname), package))
    return filesList


# TODO: add .desktop files for the eric tools
def getDataFiles():
    """
    Function to return data_files in a platform dependent manner.
    
    @return list containing the platform specific data files
    @rtype list of tuples of (str, list of str)
    """
    if sys.platform.startswith('linux'):
        dataFiles = [
            ('share/applications', [
                'linux/eric7.desktop',
                'linux/eric7_browser.desktop',
            ]),
            ('share/icons', [
                'eric7/icons/breeze-dark/eric.svg',
                'eric7/icons/breeze-dark/ericWeb48.svg',
                'eric7/pixmaps/eric48_icon.png',
                'eric7/pixmaps/ericWeb48_icon.png'
            ]),
            ('share/appdata', ['linux/eric7.appdata.xml']),
            ('share/metainfo', ['linux/eric7.appdata.xml']),
        ]
    elif sys.platform.startswith(("win", "cygwin")):
        dataFiles = [
            ('scripts', [
                'eric7/pixmaps/eric7.ico',
                'eric7/pixmaps/ericWeb48.ico'])
        ]
    else:
        dataFiles = []
    return dataFiles


def getLongDescription():
    """
    Function to get the long description via the README file.
    
    @return long description
    @rtype str
    """
    with open(os.path.join(os.path.dirname(__file__), "docs", "README.rst"),
              "r") as f:
        longDescription = f.read()
    
    if not longDescription:
        longDescription = (
            "eric is an integrated development environment for the Python"
            " programming language. It uses the PyQt6 bindings and the"
            " QScintilla2 editor widget. See"
            " https://eric-ide.python-projects.org for more details."
        )
    
    return longDescription

######################################################################
## functions to prepare the sources for building
######################################################################


def prepareInfoFile(fileName, version):
    """
    Function to prepare an Info.py file.
    
    @param fileName name of the Python file containing the info (string)
    @param version version string for the package (string)
    """
    if not fileName:
        return
    
    with contextlib.suppress(OSError):
        os.rename(fileName, fileName + ".orig")
    try:
        hgOut = subprocess.run(                     # secok
            ["hg", "identify", "-i"], check=True,
            capture_output=True, text=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        hgOut = ""
    if hgOut:
        hgOut = hgOut.strip()
        if hgOut.endswith("+"):
            hgOut = hgOut[:-1]
        with open(fileName + ".orig", "r", encoding="utf-8") as f:
            text = f.read()
        text = (
            text.replace("@@REVISION@@", hgOut)
            .replace("@@VERSION@@", version)
        )
        with open(fileName, "w") as f:
            f.write(text)
    else:
        shutil.copy(fileName + ".orig", fileName)


def prepareAppdataFile(fileName, version):
    """
    Function to prepare a .appdata.xml file.
    
    @param fileName name of the .appdata.xml file (string)
    @param version version string for the package (string)
    """
    if not fileName:
        return
    
    with contextlib.suppress(OSError):
        os.rename(fileName, fileName + ".orig")
    with open(fileName + ".orig", "r", encoding="utf-8") as f:
        text = f.read()
    text = (
        text.replace("@VERSION@", version)
        .replace("@DATE@", datetime.date.today().isoformat())
    )
    with open(fileName, "w") as f:
        f.write(text)


def cleanupSource(dirName):
    """
    Cleanup the sources directory to get rid of leftover files
    and directories.
    
    @param dirName name of the directory to prune (string)
    """
    # step 1: delete all Ui_*.py files without a corresponding
    #         *.ui file
    dirListing = os.listdir(dirName)
    for formName, sourceName in [
        (f.replace('Ui_', "").replace(".py", ".ui"), f)
            for f in dirListing if fnmatch.fnmatch(f, "Ui_*.py")]:
        if not os.path.exists(os.path.join(dirName, formName)):
            os.remove(os.path.join(dirName, sourceName))
            if os.path.exists(os.path.join(dirName, sourceName + "c")):
                os.remove(os.path.join(dirName, sourceName + "c"))
    
    # step 2: delete the __pycache__ directory and all remaining *.pyc files
    if os.path.exists(os.path.join(dirName, "__pycache__")):
        shutil.rmtree(os.path.join(dirName, "__pycache__"))
    for name in [f for f in os.listdir(dirName)
                 if fnmatch.fnmatch(f, "*.pyc")]:
        os.remove(os.path.join(dirName, name))
    
    # step 3: delete *.orig files
    for name in [f for f in os.listdir(dirName)
                 if fnmatch.fnmatch(f, "*.orig")]:
        os.remove(os.path.join(dirName, name))
    
    # step 4: descent into subdirectories and delete them if empty
    for name in os.listdir(dirName):
        name = os.path.join(dirName, name)
        if os.path.isdir(name):
            cleanupSource(name)
            if len(os.listdir(name)) == 0:
                os.rmdir(name)


def __pyName(py_dir, py_file):
    """
    Local function to create the Python source file name for the compiled
    .ui file.
    
    @param py_dir suggested name of the directory (string)
    @param py_file suggested name for the compile source file (string)
    @return tuple of directory name (string) and source file name (string)
    """
    return py_dir, "Ui_{0}".format(py_file)


def compileUiFiles(dirName):
    """
    Compile the .ui files to Python sources.
    
    @param dirName name of the directory to compile UI files for (string)
    """
    from PyQt6.uic import compileUiDir
    compileUiDir(dirName, True, __pyName)


def createInstallInfoFile(dirName):
    """
    Create a file containing some rudimentary install information.
    
    @param dirName name of the directory to compile UI files for
    @type str
    """
    global installInfoName
    
    installInfo = {
        "sudo": False,
        "user": "",
        "exe": "",
        "argv": "",
        "install_cwd": "",
        "eric": "",
        "virtualenv": False,
        "installed": False,
        "installed_on": "",
        "guessed": False,
        "edited": False,
        "pip": True,
        "remarks": "",
        "install_cwd_edited": False,
        "exe_edited": False,
        "argv_edited": False,
        "eric_edited": False,
    }
    with open(os.path.join(dirName, installInfoName), "w") as infoFile:
        json.dump(installInfo, infoFile, indent=2)

######################################################################
## setup() below
######################################################################

Version = getVersion()
sourceDir = os.path.join(os.path.dirname(__file__), "eric7")
infoFileName = os.path.join(sourceDir, "UI", "Info.py")
appdataFileName = os.path.join(os.path.dirname(__file__), "linux",
                               "eric7.appdata.xml")
if sys.argv[1].startswith("bdist"):
    # prepare the sources under "eric7" for building the wheel file
    print("preparing the sources...")       # __IGNORE_WARNING_M801__
    cleanupSource(sourceDir)
    compileUiFiles(sourceDir)
    prepareInfoFile(infoFileName, Version)
    prepareAppdataFile(appdataFileName, Version)
    createInstallInfoFile(sourceDir)
    print("Preparation finished")           # __IGNORE_WARNING_M801__

setup(
    name="eric-ide",
    version=Version,
    description="eric-ide is an integrated development environment for the"
                " Python language.",
    long_description=getLongDescription(),
    long_description_content_type="text/x-rst",
    author="Detlev Offenbach",
    author_email="detlev@die-offenbachs.de",
    url="https://eric-ide.python-projects.org",
    project_urls={
        "Source Code": "https://hg.die-offenbachs.homelinux.org/eric/",
        "Issues Tracker": "https://tracker.die-offenbachs.homelinux.org/",
    },
    platforms=["Linux", "Windows", "macOS"],
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
        "Natural Language :: German",
        "Natural Language :: Russian",
        "Natural Language :: Spanish",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)"
    ],
    keywords="Development PyQt6 IDE Python3",
    python_requires=">=3.7",
    install_requires=[
        "pip>=19.0",
        "wheel",
        "PyQt6>=6.2.0",
        "PyQt6-Charts>=6.2.0",
        "PyQt6-WebEngine>=6.2.0",
        "PyQt6-QScintilla>=2.13.0",
        "docutils",
        "Markdown",
        "pyyaml",
        "tomlkit",
        "chardet",
        "asttokens",
        "EditorConfig",
        "Send2Trash",
        "Pygments",
        "parso",
        "jedi",
        "packaging",
        "pipdeptree",
        "pywin32>=1.0;platform_system=='Windows'",
    ],
    data_files=getDataFiles(),
    packages=find_packages(),
    zip_safe=False,
    package_data={
        "": getPackageData(
            "eric7",
            [".png", ".svg", ".svgz", ".xpm", ".ico", ".gif", ".icns", ".txt",
             ".md", ".rst", ".tmpl", ".html", ".qch", ".css", ".scss", ".qss",
             ".ehj", ".ethj", ".api", ".bas", ".dat", ".xbel", ".xml", ".js"]
        ) + ["i18n/eric7_de.qm", "i18n/eric7_en.qm", "i18n/eric7_es.qm",
             "i18n/eric7_ru.qm",
             installInfoName,
             ]
    },
    entry_points={
        "gui_scripts": [
            "eric7 = eric7.eric7:main",
            "eric7_browser = eric7.eric7_browser:main",
            "eric7_compare = eric7.eric7_compare:main",
            "eric7_configure = eric7.eric7_configure:main",
            "eric7_diff = eric7.eric7_diff:main",
            "eric7_editor = eric7.eric7_editor:main",
            "eric7_hexeditor = eric7.eric7_hexeditor:main",
            "eric7_iconeditor = eric7.eric7_iconeditor:main",
            "eric7_plugininstall = eric7.eric7_plugininstall:main",
            "eric7_pluginrepository = eric7.eric7_pluginrepository:main",
            "eric7_pluginuninstall = eric7.eric7_pluginuninstall:main",
            "eric7_qregularexpression = eric7.eric7_qregularexpression:main",
            "eric7_re = eric7.eric7_re:main",
            "eric7_shell = eric7.eric7_shell:main",
            "eric7_snap = eric7.eric7_snap:main",
            "eric7_sqlbrowser = eric7.eric7_sqlbrowser:main",
            "eric7_tray = eric7.eric7_tray:main",
            "eric7_trpreviewer = eric7.eric7_trpreviewer:main",
            "eric7_uipreviewer = eric7.eric7_uipreviewer:main",
            "eric7_testing = eric7.eric7_testing:main",
            "eric7_virtualenv = eric7.eric7_virtualenv:main",
        ],
        "console_scripts": [
            "eric7_api = eric7.eric7_api:main",
            "eric7_doc = eric7.eric7_doc:main",
            "eric7_post_install = eric7.eric7_post_install:main",
        ],
    },
)

# cleanup
for fileName in [infoFileName, appdataFileName]:
    if os.path.exists(fileName + ".orig"):
        with contextlib.suppress(OSError):
            os.remove(fileName)
            os.rename(fileName + ".orig", fileName)
