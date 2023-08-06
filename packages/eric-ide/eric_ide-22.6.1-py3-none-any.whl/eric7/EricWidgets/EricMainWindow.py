# -*- coding: utf-8 -*-

# Copyright (c) 2012 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a main window class with styling support.
"""

from PyQt6.QtWidgets import QMainWindow, QStyleFactory, QApplication

from .EricApplication import ericApp


class EricMainWindow(QMainWindow):
    """
    Class implementing a main window with styling support.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        
        self.defaultStyleName = QApplication.style().objectName()
    
    def setStyle(self, styleName, styleSheetFile):
        """
        Public method to set the style of the interface.
        
        @param styleName name of the style to set
        @type str
        @param styleSheetFile name of a style sheet file to read to overwrite
            defaults of the given style
        @type str
        """
        # step 1: set the style
        style = None
        if styleName != "System" and styleName in QStyleFactory.keys():
            # __IGNORE_WARNING_Y118__
            style = QStyleFactory.create(styleName)
        if style is None:
            style = QStyleFactory.create(self.defaultStyleName)
        if style is not None:
            QApplication.setStyle(style)
        
        # step 2: set a style sheet
        ericApp().setStyleSheetFile(styleSheetFile)
