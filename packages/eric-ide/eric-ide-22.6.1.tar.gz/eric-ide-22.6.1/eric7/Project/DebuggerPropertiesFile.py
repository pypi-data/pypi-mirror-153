# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the project debugger properties
JSON file.
"""

import json
import time
import typing

from PyQt6.QtCore import QObject

from EricWidgets import EricMessageBox
from EricGui.EricOverrideCursor import EricOverridenCursor

import Preferences

Project = typing.TypeVar("Project")


class DebuggerPropertiesFile(QObject):
    """
    Class representing the project debugger properties JSON file.
    """
    def __init__(self, project: Project, parent: QObject = None):
        """
        Constructor
        
        @param project reference to the project object
        @type Project
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super().__init__(parent)
        self.__project = project
    
    def writeFile(self, filename: str) -> bool:
        """
        Public method to write the project debugger properties data to a
        project debugger properties JSON file.
        
        @param filename name of the user project file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        debuggerPropertiesDict = {}
        debuggerPropertiesDict["header"] = {
            "comment": "eric debugger properties file for project {0}".format(
                self.__project.getProjectName()),
            "warning": "This file was generated automatically, do not edit.",
        }
        
        if Preferences.getProject("TimestampFile"):
            debuggerPropertiesDict["header"]["saved"] = (
                time.strftime('%Y-%m-%d, %H:%M:%S')
            )
        
        debuggerPropertiesDict["debug_properties"] = (
            self.__project.debugProperties
        )
        
        try:
            jsonString = json.dumps(debuggerPropertiesDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, OSError) as err:
            with EricOverridenCursor():
                EricMessageBox.critical(
                    None,
                    self.tr("Save Debugger Properties"),
                    self.tr(
                        "<p>The project debugger properties file"
                        " <b>{0}</b> could not be written.</p>"
                        "<p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the project debugger properties data from a
        project debugger properties JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            debuggerPropertiesDict = json.loads(jsonString)
        except (OSError, json.JSONDecodeError) as err:
            EricMessageBox.critical(
                None,
                self.tr("Read Debugger Properties"),
                self.tr(
                    "<p>The project debugger properties file <b>{0}</b>"
                    " could not be read.</p><p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        self.__project.debugProperties = (
            debuggerPropertiesDict["debug_properties"]
        )
        
        return True
