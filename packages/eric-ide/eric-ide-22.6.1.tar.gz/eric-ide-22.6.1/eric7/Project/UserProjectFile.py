# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the user project JSON file.
"""

import json
import time
import typing

from PyQt6.QtCore import QObject

from EricWidgets import EricMessageBox
from EricGui.EricOverrideCursor import EricOverridenCursor

import Preferences

Project = typing.TypeVar("Project")


class UserProjectFile(QObject):
    """
    Class representing the user project JSON file.
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
        Public method to write the user project data to a user project
        JSON file.
        
        @param filename name of the user project file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        userProjectDict = {}
        userProjectDict["header"] = {
            "comment": "eric user project file for project {0}".format(
                self.__project.getProjectName()),
        }
        
        if Preferences.getProject("TimestampFile"):
            userProjectDict["header"]["saved"] = (
                time.strftime('%Y-%m-%d, %H:%M:%S')
            )
        
        userProjectDict["user_data"] = self.__project.pudata
        
        try:
            jsonString = json.dumps(userProjectDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, OSError) as err:
            with EricOverridenCursor():
                EricMessageBox.critical(
                    None,
                    self.tr("Save User Project Properties"),
                    self.tr(
                        "<p>The user specific project properties file"
                        " <b>{0}</b> could not be written.</p>"
                        "<p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the user project data from a user project
        JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            userProjectDict = json.loads(jsonString)
        except (OSError, json.JSONDecodeError) as err:
            EricMessageBox.critical(
                None,
                self.tr("Read User Project Properties"),
                self.tr(
                    "<p>The user specific project properties file <b>{0}</b>"
                    " could not be read.</p><p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        self.__project.pudata = userProjectDict["user_data"]
        
        return True
