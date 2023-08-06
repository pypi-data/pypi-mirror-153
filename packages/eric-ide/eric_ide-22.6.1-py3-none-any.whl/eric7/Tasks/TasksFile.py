# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a class representing the tasks JSON file.
"""

import json
import time

from PyQt6.QtCore import QObject

from EricWidgets import EricMessageBox
from EricGui.EricOverrideCursor import EricOverridenCursor
from EricWidgets.EricApplication import ericApp

import Preferences

from .Task import TaskType, TaskPriority


class TasksFile(QObject):
    """
    Class representing the tasks JSON file.
    """
    def __init__(self, isGlobal: bool, parent: QObject = None):
        """
        Constructor
        
        @param isGlobal flag indicating a file for global tasks
        @type bool
        @param parent reference to the parent object (defaults to None)
        @type QObject (optional)
        """
        super().__init__(parent)
        self.__isGlobal = isGlobal
    
    def writeFile(self, filename: str) -> bool:
        """
        Public method to write the tasks data to a tasks JSON file.
        
        @param filename name of the tasks file
        @type str
        @return flag indicating a successful write
        @rtype bool
        """
        # prepare the tasks data dictionary
        # step 0: header
        tasksDict = {}
        if self.__isGlobal:
            tasksDict["header"] = {
                "comment": "eric tasks file",
                "saved": time.strftime('%Y-%m-%d, %H:%M:%S'),
                "warning": (
                    "This file was generated automatically, do not edit."
                ),
            }
            # step 1: project scan filter
            tasksDict["ProjectScanFilter"] = ""
            
            # step 2: tasks
            tasksDict["Tasks"] = [
                task.toDict()
                for task in ericApp().getObject("TaskViewer").getGlobalTasks()
            ]
        else:
            tasksDict["header"] = {
                "comment": "eric tasks file for project {0}".format(
                    ericApp().getObject("Project").getProjectName()),
                "warning": (
                    "This file was generated automatically, do not edit."
                ),
            }
            if Preferences.getProject("TimestampFile"):
                tasksDict["header"]["saved"] = (
                    time.strftime('%Y-%m-%d, %H:%M:%S')
                )
            # step 1: project scan filter
            tasksDict["ProjectScanFilter"] = (
                ericApp().getObject("TaskViewer").getTasksScanFilter()
            )
            
            # step 2: tasks
            tasksDict["Tasks"] = [
                task.toDict()
                for task in ericApp().getObject("TaskViewer").getProjectTasks()
            ]
        
        try:
            jsonString = json.dumps(tasksDict, indent=2)
            with open(filename, "w") as f:
                f.write(jsonString)
        except (TypeError, OSError) as err:
            with EricOverridenCursor():
                EricMessageBox.critical(
                    None,
                    self.tr("Save Tasks"),
                    self.tr(
                        "<p>The tasks file <b>{0}</b> could not be"
                        " written.</p><p>Reason: {1}</p>"
                    ).format(filename, str(err))
                )
                return False
        
        return True
    
    def readFile(self, filename: str) -> bool:
        """
        Public method to read the tasks data from a task JSON file.
        
        @param filename name of the project file
        @type str
        @return flag indicating a successful read
        @rtype bool
        """
        try:
            with open(filename, "r") as f:
                jsonString = f.read()
            tasksDict = json.loads(jsonString)
        except (OSError, json.JSONDecodeError) as err:
            EricMessageBox.critical(
                None,
                self.tr("Read Tasks"),
                self.tr(
                    "<p>The tasks file <b>{0}</b> could not be read.</p>"
                    "<p>Reason: {1}</p>"
                ).format(filename, str(err))
            )
            return False
        
        viewer = ericApp().getObject("TaskViewer")
        if tasksDict["ProjectScanFilter"]:
            viewer.setTasksScanFilter(tasksDict["ProjectScanFilter"])
        
        addedTasks = []
        for task in tasksDict["Tasks"]:
            addedTask = viewer.addTask(
                task["summary"], priority=TaskPriority(task["priority"]),
                filename=task["filename"], lineno=task["lineno"],
                completed=task["completed"], _time=task["created"],
                isProjectTask=not self.__isGlobal,
                taskType=TaskType(task["type"]),
                description=task["description"], uid=task["uid"],
                parentTask=task["parent_uid"])
            if addedTask:
                addedTasks.append((addedTask, task["expanded"]))
        
        for task, expanded in addedTasks:
            task.setExpanded(expanded)
        
        return True
