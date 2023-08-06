#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
eric Virtual Environment Manager.

This is the main Python script to manage Python Virtual Environments from
outside of the IDE.
"""

import sys
import os

sys.path.insert(1, os.path.dirname(__file__))

for arg in sys.argv[:]:
    if arg.startswith("--config="):
        import Globals
        configDir = arg.replace("--config=", "")
        Globals.setConfigDir(configDir)
        sys.argv.remove(arg)
    elif arg.startswith("--settings="):
        from PyQt6.QtCore import QSettings
        settingsDir = os.path.expanduser(arg.replace("--settings=", ""))
        if not os.path.isdir(settingsDir):
            os.makedirs(settingsDir)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, settingsDir)
        sys.argv.remove(arg)

from Globals import AppInfo

from Toolbox import Startup


def createMainWidget(argv):
    """
    Function to create the main widget.
    
    @param argv list of commandline parameters
    @type list of str
    @return reference to the main widget
    @rtype QWidget
    """
    from VirtualEnv.VirtualenvManagerWidgets import VirtualenvManagerWindow
    return VirtualenvManagerWindow(None)


def main():
    """
    Main entry point into the application.
    """
    from PyQt6.QtGui import QGuiApplication
    QGuiApplication.setDesktopFileName("eric7_virtualenv.desktop")
    
    options = [
        ("--config=configDir",
         "use the given directory as the one containing the config files"),
        ("--settings=settingsDir",
         "use the given directory to store the settings files"),
    ]
    appinfo = AppInfo.makeAppInfo(
        sys.argv,
        "eric Virtualenv Manager",
        "",
        "Utility to manage Python Virtual Environments.",
        options
    )
    res = Startup.simpleAppStartup(
        sys.argv, appinfo, createMainWidget)
    sys.exit(res)

if __name__ == '__main__':
    main()
