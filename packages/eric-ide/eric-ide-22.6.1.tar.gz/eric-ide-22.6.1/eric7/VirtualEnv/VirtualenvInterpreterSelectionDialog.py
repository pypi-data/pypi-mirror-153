# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the interpreter for a virtual
environment.
"""

import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_VirtualenvInterpreterSelectionDialog import (
    Ui_VirtualenvInterpreterSelectionDialog
)

import Globals


class VirtualenvInterpreterSelectionDialog(
        QDialog, Ui_VirtualenvInterpreterSelectionDialog):
    """
    Class implementing a dialog to enter the interpreter for a virtual
    environment.
    """
    def __init__(self, venvName, venvDirectory, parent=None):
        """
        Constructor
        
        @param venvName name for the virtual environment
        @type str
        @param venvDirectory directory of the virtual environment
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.pythonExecPicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.pythonExecPicker.setWindowTitle(
            self.tr("Python Interpreter"))
        
        self.nameEdit.setText(venvName)
        
        if venvDirectory:
            # try to determine a Python interpreter name
            if Globals.isWindowsPlatform():
                candidates = (
                    os.path.join(venvDirectory, "Scripts", "python.exe"),
                    os.path.join(venvDirectory, "python.exe"),
                )
            else:
                candidates = (
                    os.path.join(venvDirectory, "bin", "python3"),
                )
            for py in candidates:
                if os.path.exists(py):
                    self.pythonExecPicker.setText(py)
                    break
            else:
                self.pythonExecPicker.setText(venvDirectory)
        else:
            self.pythonExecPicker.setText(venvDirectory)
    
    def __updateOK(self):
        """
        Private method to update the enabled status of the OK button.
        """
        interpreterPath = self.pythonExecPicker.text()
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(interpreterPath) and
            os.path.isfile(interpreterPath) and
            os.access(interpreterPath, os.X_OK)
        )
    
    @pyqtSlot(str)
    def on_pythonExecPicker_textChanged(self, txt):
        """
        Private slot to handle changes of the entered Python interpreter path.
        
        @param txt entered Python interpreter path
        @type str
        """
        self.__updateOK()
    
    def getData(self):
        """
        Public method to get the entered data.
        
        @return path of the selected Python interpreter
        @rtype str
        """
        return self.pythonExecPicker.text()
