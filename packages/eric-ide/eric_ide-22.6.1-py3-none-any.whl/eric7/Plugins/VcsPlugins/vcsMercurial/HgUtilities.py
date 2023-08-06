# -*- coding: utf-8 -*-

# Copyright (c) 2010 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some common utility functions for the Mercurial package.
"""

import os
import re
import sys

from PyQt6.QtCore import QProcess, QProcessEnvironment, QCoreApplication

import Utilities
from Globals import isWindowsPlatform


def getHgExecutable():
    """
    Function to get the full path of the Mercurial executable.
    
    @return path of the Mercurial executable
    @rtype str
    """
    from Plugins.PluginVcsMercurial import VcsMercurialPlugin
    
    exe = VcsMercurialPlugin.getPreferences("MercurialExecutablePath")
    if not exe:
        program = "hg"
        if isWindowsPlatform():
            program += ".exe"
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                exe = os.path.join(dirName, program)
            elif os.path.exists(os.path.join(dirName, "Scripts", program)):
                exe = os.path.join(dirName, "Scripts", program)
        else:
            dirName = os.path.dirname(sys.executable)
            if os.path.exists(os.path.join(dirName, program)):
                exe = os.path.join(dirName, program)
    
    if not exe:
        exe = program
    
    return exe


def getConfigPath():
    """
    Function to get the filename of the config file.
    
    @return filename of the config file
    @rtype str
    """
    if Utilities.isWindowsPlatform():
        userprofile = os.environ["USERPROFILE"]
        return os.path.join(userprofile, "Mercurial.ini")
    else:
        homedir = Utilities.getHomeDir()
        return os.path.join(homedir, ".hgrc")


def prepareProcess(proc, encoding="", language=""):
    """
    Function to prepare the given process.
    
    @param proc reference to the process to be prepared
    @type QProcess
    @param encoding encoding to be used by the process
    @type str
    @param language language to be set
    @type str
    """
    env = QProcessEnvironment.systemEnvironment()
    env.insert("HGPLAIN", '1')
    
    # set the encoding for the process
    if encoding:
        env.insert("HGENCODING", encoding)
    
    # set the language for the process
    if language:
        env.insert("LANGUAGE", language)
    
    proc.setProcessEnvironment(env)


def hgVersion(plugin):
    """
    Public method to determine the Mercurial version.
    
    @param plugin reference to the plugin object
    @type VcsMercurialPlugin
    @return tuple containing the Mercurial version as a string and as a tuple
        and an error message.
    @rtype tuple of str, tuple of int and str
    """
    versionStr = ""
    version = ()
    errorMsg = ""
    
    exe = getHgExecutable()
    
    args = ["version"]
    args.extend(plugin.getGlobalOptions())
    process = QProcess()
    process.start(exe, args)
    procStarted = process.waitForStarted(5000)
    if procStarted:
        finished = process.waitForFinished(30000)
        if finished and process.exitCode() == 0:
            output = str(process.readAllStandardOutput(),
                         plugin.getPreferences("Encoding"), 'replace')
            versionStr = output.splitlines()[0].split()[-1][0:-1]
            v = list(re.match(r'.*?(\d+)\.(\d+)\.?(\d+)?(\+[0-9a-f-]+)?',
                              versionStr).groups())
            if v[-1] is None:
                del v[-1]
            for i in range(3):
                try:
                    v[i] = int(v[i])
                except TypeError:
                    v[i] = 0
                except IndexError:
                    v.append(0)
            version = tuple(v)
        else:
            if finished:
                errorMsg = QCoreApplication.translate(
                    "HgUtilities",
                    "The hg process finished with the exit code {0}"
                ).format(process.exitCode())
            else:
                errorMsg = QCoreApplication.translate(
                    "HgUtilities",
                    "The hg process did not finish within 30s.")
    else:
        errorMsg = QCoreApplication.translate(
            "HgUtilities",
            "Could not start the hg executable.")
    
    return versionStr, version, errorMsg
