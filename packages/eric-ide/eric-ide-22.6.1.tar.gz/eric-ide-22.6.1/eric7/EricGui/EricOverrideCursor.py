# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a context manager class for an override cursor and a
QProcess class controlling an override cursor.
"""

import contextlib

from PyQt6.QtCore import pyqtSlot, Qt, QProcess, QEventLoop
from PyQt6.QtGui import QCursor, QGuiApplication


class EricOverrideCursor(contextlib.AbstractContextManager):
    """
    Class implementing a context manager class for an override cursor.
    """
    def __init__(self, cursorShape=Qt.CursorShape.WaitCursor):
        """
        Constructor
        
        @param cursorShape shape of the override cursor
        @type Qt.CursorShape
        """
        self.__cursorShape = cursorShape
    
    def __enter__(self):
        """
        Special method called when entering the runtime ccontext.
        
        @return reference to the context manager object
        @rtype EricOverrideCursor
        """
        QGuiApplication.setOverrideCursor(QCursor(self.__cursorShape))
        QGuiApplication.processEvents(
            QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Special method called when exiting the runtime ccontext.
        
        @param exc_type type of an exception raised in the runtime context
        @param exc_value value of an exception raised in the runtime context
        @param traceback traceback of an exception raised in the runtime
            context
        @return always returns None to not suppress any exception
        @rtype None
        """
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.processEvents(
            QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
        
        return None     # __IGNORE_WARNING_M831__


class EricOverridenCursor(contextlib.AbstractContextManager):
    """
    Class implementing a context manager class for an overriden cursor.
    
    The cursor is reset upon entering the runtime context and restored
    upon exiting it.
    """
    def __init__(self):
        """
        Constructor
        """
        self.__cursorShape = None
    
    def __enter__(self):
        """
        Special method called when entering the runtime ccontext.
        
        @return reference to the context manager object
        @rtype EricOverrideCursor
        """
        cursor = QGuiApplication.overrideCursor()
        if cursor is not None:
            self.__cursorShape = cursor.shape()
            QGuiApplication.restoreOverrideCursor()
            QGuiApplication.processEvents(
                QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Special method called when exiting the runtime ccontext.
        
        @param exc_type type of an exception raised in the runtime context
        @param exc_value value of an exception raised in the runtime context
        @param traceback traceback of an exception raised in the runtime
            context
        @return always returns None to not suppress any exception
        @rtype None
        """
        if self.__cursorShape is not None:
            QGuiApplication.setOverrideCursor(QCursor(self.__cursorShape))
            QGuiApplication.processEvents(
                QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
        
        return None     # __IGNORE_WARNING_M831__


class EricOverrideCursorProcess(QProcess):
    """
    Class implementing a QProcess subclass controlling an override cursor.
    """
    def __init__(self, parent=None, cursorShape=Qt.CursorShape.WaitCursor):
        """
        Constructor
        
        @param parent reference to the parent object
        @type QObject
        @param cursorShape shape of the override cursor
        @type Qt.CursorShape
        """
        super().__init__(parent)
        
        self.__cursorShape = cursorShape
        
        self.started.connect(self.__processStarted)
        self.finished.connect(self.__processFinished)
    
    @pyqtSlot()
    def __processStarted(self):
        """
        Private slot setting the cursor after the process has started.
        """
        QGuiApplication.setOverrideCursor(QCursor(self.__cursorShape))
        QGuiApplication.processEvents(
            QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
    
    @pyqtSlot()
    def __processFinished(self):
        """
        Private slot resetting the cursor when the process finished.
        """
        QGuiApplication.restoreOverrideCursor()
        QGuiApplication.processEvents(
            QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
