# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to change the default size settings of the Source
Outline pane.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QAbstractButton, QDialog, QDialogButtonBox

from .Ui_EditorOutlineSizesDialog import Ui_EditorOutlineSizesDialog


class EditorOutlineSizesDialog(QDialog, Ui_EditorOutlineSizesDialog):
    """
    Class implementing a dialog to change the default size settings of the
    Source Outline pane.
    """
    def __init__(self, currentWidth, defaultWidth, defaultStepSize,
                 parent=None):
        """
        Constructor
        
        @param currentWidth value of the current width
        @type int
        @param defaultWidth value of the default width
        @type int
        @param defaultStepSize value of the step size
        @type int
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__defaultWidth = defaultWidth
        self.__defaultStepSize = defaultStepSize
        
        self.sourceOutlineWidthSpinBox.setValue(currentWidth)
        self.sourceOutlineWidthStepSpinBox.setValue(defaultStepSize)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    @pyqtSlot(QAbstractButton)
    def on_buttonBox_clicked(self, button):
        """
        Private slot to handle the selection of a dialog button.
        
        @param button reference to the clicked button
        @type QAbstractButton
        """
        if button is self.buttonBox.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ):
            self.sourceOutlineWidthSpinBox.setValue(self.__defaultWidth)
            self.sourceOutlineWidthStepSpinBox.setValue(self.__defaultStepSize)
    
    def getSizes(self):
        """
        Public method to retrieve the entered values.
        
        @return tuple containing the values of the default width and step size
        @rtype tuple of (int, int)
        """
        return (
            self.sourceOutlineWidthSpinBox.value(),
            self.sourceOutlineWidthStepSpinBox.value()
        )
