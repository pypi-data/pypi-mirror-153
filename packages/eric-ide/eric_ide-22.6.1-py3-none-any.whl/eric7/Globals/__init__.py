# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module defining common data to be used by all modules.
"""

#
# Note: Do not import any eric stuff in here!!!!!!!
#

import contextlib
import os
import re
import sys

from PyQt6.QtCore import (
    QDir, QByteArray, QCoreApplication, QT_VERSION, QProcess, qVersion
)

from eric7config import getConfig

# names of the various settings objects
settingsNameOrganization = "Eric7"
settingsNameGlobal = "eric7"
settingsNameRecent = "eric7recent"

# key names of the various recent entries
recentNameMultiProject = "MultiProjects"
recentNameProject = "Projects"
recentNameFiles = "Files"
recentNameHexFiles = "HexFiles"
recentNameHosts = "Hosts"
recentNameBreakpointFiles = "BreakPointFiles"
recentNameBreakpointConditions = "BreakPointConditions"
recentNameTestDiscoverHistory = "UTDiscoverHistory"
recentNameTestFileHistory = "UTFileHistory"
recentNameTestNameHistory = "UTTestnameHistory"
recentNameTestFramework = "UTTestFramework"
recentNameTestEnvironment = "UTEnvironmentName"

configDir = None


def isWindowsPlatform():
    """
    Function to check, if this is a Windows platform.
    
    @return flag indicating Windows platform
    @rtype bool
    """
    return sys.platform.startswith(("win", "cygwin"))


def isMacPlatform():
    """
    Function to check, if this is a Mac platform.
    
    @return flag indicating Mac platform
    @rtype bool
    """
    return sys.platform == "darwin"


def isLinuxPlatform():
    """
    Function to check, if this is a Linux platform.
    
    @return flag indicating Linux platform
    @rtype bool
    """
    return sys.platform.startswith("linux")


def desktopName():
    """
    Function to determine the name of the desktop environment used
    (Linux only).
    
    @return name of the desktop environment
    @rtype str
    """
    if not isLinuxPlatform():
        return ""
    
    currDesktop = os.environ.get("XDG_CURRENT_DESKTOP", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("XDG_SESSION_DESKTOP", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("GDMSESSION", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("GNOME_DESKTOP_SESSION_ID", "")
    if currDesktop:
        return currDesktop
    
    currDesktop = os.environ.get("KDE_FULL_SESSION", "")
    if currDesktop:
        if currDesktop == "true":
            return "KDE"
        
        return currDesktop
    
    currDesktop = os.environ.get("DESKTOP_SESSION", "")
    if currDesktop:
        return currDesktop
    
    return ""


def isKdeDesktop():
    """
    Function to check, if the current session is a KDE desktop (Linux only).
    
    @return flag indicating a KDE desktop
    @rtype bool
    """
    if not isLinuxPlatform():
        return False
    
    isKDE = False
    
    desktop = (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower() or
        os.environ.get("XDG_SESSION_DESKTOP", "").lower() or
        os.environ.get("DESKTOP_SESSION", "").lower()
    )
    isKDE = (
        "kde" in desktop or "plasma" in desktop
        if desktop else
        bool(os.environ.get("KDE_FULL_SESSION", ""))
    )
    
    return isKDE


def isGnomeDesktop():
    """
    Function to check, if the current session is a Gnome desktop (Linux only).
    
    @return flag indicating a Gnome desktop
    @rtype bool
    """
    if not isLinuxPlatform():
        return False
    
    isGnome = False
    
    desktop = (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower() or
        os.environ.get("XDG_SESSION_DESKTOP", "").lower() or
        os.environ.get("GDMSESSION", "").lower()
    )
    isGnome = (
        "gnome" in desktop
        if desktop else
        bool(os.environ.get("GNOME_DESKTOP_SESSION_ID", ""))
    )
    
    return isGnome


def sessionType():
    """
    Function to determine the name of the running session (Linux only).
    
    @return name of the desktop environment
    @rtype str
    """
    if not isLinuxPlatform():
        return ""
    
    sessionType = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if "x11" in sessionType:
        return "X11"
    elif "wayland" in sessionType:
        return "Wayland"
    
    sessionType = os.environ.get("WAYLAND_DISPLAY", "").lower()
    if "wayland" in sessionType:
        return "Wayland"
    
    return ""


def isWaylandSession():
    """
    Function to check, if the current session is a wayland session.
    
    @return flag indicating a wayland session
    @rtype bool
    """
    return sessionType() == "Wayland"


def getConfigDir():
    """
    Module function to get the name of the directory storing the config data.
    
    @return directory name of the config dir
    @rtype str
    """
    if configDir is not None and os.path.exists(configDir):
        hp = configDir
    else:
        cdn = ".eric7"
        hp = os.path.join(os.path.expanduser("~"), cdn)
        if not os.path.exists(hp):
            os.mkdir(hp)
    return hp


def getInstallInfoFilePath():
    """
    Public method to get the path name of the install info file.
    
    @return file path of the install info file
    @rtype str
    """
    filename = "eric7install.{0}.json".format(
        getConfig("ericDir")
        .replace(":", "_")
        .replace("\\", "_")
        .replace("/", "_")
        .replace(" ", "_")
        .strip("_")
    )
    return os.path.join(getConfigDir(), filename)


def setConfigDir(d):
    """
    Module function to set the name of the directory storing the config data.
    
    @param d name of an existing directory
    @type str
    """
    global configDir
    configDir = os.path.expanduser(d)


def getPythonExecutable():
    """
    Function to determine the path of the (non-windowed) Python executable.
    
    @return path of the Python executable
    @rtype str
    """
    if sys.platform.startswith("linux"):
        return sys.executable
    elif sys.platform == "darwin":
        return sys.executable.replace("pythonw", "python")
    else:
        return sys.executable.replace("pythonw.exe", "python.exe")


def getPythonLibraryDirectory():
    """
    Function to determine the path to Python's library directory.
    
    @return path to the Python library directory
    @rtype str
    """
    import sysconfig
    return sysconfig.get_path('platlib')


def getPyQt6ModulesDirectory():
    """
    Function to determine the path to PyQt6 modules directory.
    
    @return path to the PyQt6 modules directory
    @rtype str
    """
    import sysconfig
    
    pyqtPath = os.path.join(sysconfig.get_path('platlib'), "PyQt6")
    if os.path.exists(pyqtPath):
        return pyqtPath
    
    return ""
    

def getPyQtToolsPath(version=5):
    """
    Module function to get the path of the PyQt tools.
    
    @param version PyQt major version
    @type int
    @return path to the PyQt tools
    @rtype str
    """
    import Preferences
    
    path = ""
    
    # step 1: check, if the user has configured a tools path
    if version == 5:
        path = Preferences.getQt("PyQtToolsDir")
    elif version == 6:
        path = Preferences.getQt("PyQt6ToolsDir")
    
    # step 2: determine from used Python interpreter (pylupdate is test object)
    if not path:
        program = "pylupdate{0}".format(version)
        if isWindowsPlatform():
            program += ".exe"
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                path = dirName
            elif os.path.exists(os.path.join(dirName, "Scripts", program)):
                path = os.path.join(dirName, "Scripts")
        else:
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                path = dirName
    
    return path


def getQtBinariesPath():
    """
    Module function to get the path of the Qt binaries.
    
    @return path of the Qt binaries
    @rtype str
    """
    import Preferences
    
    path = ""
    
    # step 1: check, if the user has configured a tools path
    path = Preferences.getQt("QtToolsDir")
    
    # step 2: try the qt6_applications package
    if not path:
        with contextlib.suppress(ImportError):
            import qt6_applications
            path = os.path.join(os.path.dirname(qt6_applications.__file__),
                                "Qt", "bin")
            # if qt6-applications is not installed just go to the next step
    
    # step 3: determine from used Python interpreter (designer is test object)
    if not path:
        program = "designer"
        if isWindowsPlatform():
            program += ".exe"
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                path = dirName
            elif os.path.exists(os.path.join(dirName, "Scripts", program)):
                path = os.path.join(dirName, "Scripts")
        else:
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                path = dirName
    
    return QDir.toNativeSeparators(path)


###############################################################################
## functions for version handling
###############################################################################


def versionToTuple(version, length=3):
    """
    Module function to convert a version string into a tuple.
    
    Note: A version string consists of non-negative decimals separated by "."
    optionally followed by a suffix. Suffix is everything after the last
    decimal.
    
    @param version version string
    @type str
    @param length desired length of the version tuple
    @type int
    @return version tuple without the suffix
    @rtype tuple of int
    """
    versionParts = []
    
    # step 1: extract suffix
    version = re.split(r"[^\d.]", version)[0]
    for part in version.split("."):
        with contextlib.suppress(ValueError):
            versionParts.append(int(part.strip()))
    versionParts.extend([0] * length)
    
    return tuple(versionParts[:length])


def qVersionTuple():
    """
    Module function to get the Qt version as a tuple.
    
    @return Qt version as a tuple
    @rtype tuple of int
    """
    return (
        (QT_VERSION & 0xff0000) >> 16,
        (QT_VERSION & 0xff00) >> 8,
        QT_VERSION & 0xff,
    )


###############################################################################
## functions for extended string handling
###############################################################################


def strGroup(txt, sep, groupLen=4):
    """
    Module function to group a string into sub-strings separated by a
    separator.
    
    @param txt text to be grouped
    @type str
    @param sep separator string
    @type str
    @param groupLen length of each group
    @type int
    @return result string
    @rtype str
    """
    groups = []
    
    while len(txt) // groupLen != 0:
        groups.insert(0, txt[-groupLen:])
        txt = txt[:-groupLen]
    if len(txt) > 0:
        groups.insert(0, txt)
    return sep.join(groups)


def strToQByteArray(txt):
    """
    Module function to convert a Python string into a QByteArray.
    
    @param txt Python string to be converted
    @type str, bytes, bytearray
    @return converted QByteArray
    @rtype QByteArray
    """
    if isinstance(txt, str):
        txt = txt.encode("utf-8")
    
    return QByteArray(txt)


def dataString(size):
    """
    Module function to generate a formatted size string.
    
    @param size size to be formatted
    @type int
    @return formatted data string
    @rtype str
    """
    if size < 1024:
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} Bytes").format(size)
    elif size < 1024 * 1024:
        size /= 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} KiB").format(size)
    elif size < 1024 * 1024 * 1024:
        size /= 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} MiB").format(size)
    elif size < 1024 * 1024 * 1024 * 1024:
        size /= 1024 * 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} GiB").format(size)
    else:
        size /= 1024 * 1024 * 1024 * 1024
        return QCoreApplication.translate(
            "Globals", "{0:4.2f} TiB").format(size)


###############################################################################
## functions for converting QSetting return types to valid types
###############################################################################


def toBool(value):
    """
    Module function to convert a value to bool.
    
    @param value value to be converted
    @type str
    @return converted data
    @rtype bool
    """
    if value in ["true", "1", "True"]:
        return True
    elif value in ["false", "0", "False"]:
        return False
    else:
        return bool(value)


def toList(value):
    """
    Module function to convert a value to a list.
    
    @param value value to be converted
    @type None, list or Any
    @return converted data
    @rtype list
    """
    if value is None:
        return []
    elif not isinstance(value, list):
        return [value]
    else:
        return value


def toByteArray(value):
    """
    Module function to convert a value to a byte array.
    
    @param value value to be converted
    @type QByteArray or None
    @return converted data
    @rtype QByteArray
    """
    if value is None:
        return QByteArray()
    else:
        return value


def toDict(value):
    """
    Module function to convert a value to a dictionary.
    
    @param value value to be converted
    @type dict or None
    @return converted data
    @rtype dict
    """
    if value is None:
        return {}
    else:
        return value


###############################################################################
## functions for web browser variant detection
###############################################################################


def getWebBrowserSupport():
    """
    Module function to determine the supported web browser variant.
    
    @return string indicating the supported web browser variant ("QtWebEngine",
        or "None")
    @rtype str
    """
    from eric7config import getConfig
    scriptPath = os.path.join(getConfig("ericDir"), "Tools",
                              "webBrowserSupport.py")
    proc = QProcess()
    proc.start(getPythonExecutable(), [scriptPath, qVersion()])
    variant = (
        str(proc.readAllStandardOutput(), "utf-8", 'replace').strip()
        if proc.waitForFinished(10000) else
        "None"
    )
    return variant
#
# eflag: noqa = M801
