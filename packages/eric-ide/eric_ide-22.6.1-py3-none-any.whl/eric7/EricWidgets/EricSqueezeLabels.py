# -*- coding: utf-8 -*-

# Copyright (c) 2008 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing labels that squeeze their contents to fit the size of the
label.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from Utilities import compactPath


class EricSqueezeLabel(QLabel):
    """
    Class implementing a label that squeezes its contents to fit its size.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent Widget (QWidget)
        """
        super().__init__(parent)
        
        self.__text = ''
        self.__elided = ''
    
    def paintEvent(self, event):
        """
        Protected method called when some painting is required.
        
        @param event reference to the paint event (QPaintEvent)
        """
        fm = self.fontMetrics()
        try:
            pixelLength = fm.horizontalAdvance(self.__text)
        except AttributeError:
            pixelLength = fm.width(self.__text)
        if pixelLength > self.contentsRect().width():
            self.__elided = fm.elidedText(
                self.text(), Qt.TextElideMode.ElideMiddle, self.width())
            super().setText(self.__elided)
        else:
            super().setText(self.__text)
        super().paintEvent(event)
    
    def setText(self, txt):
        """
        Public method to set the label's text.
        
        @param txt the text to be shown (string)
        """
        self.__text = txt
        super().setText(self.__text)


class EricSqueezeLabelPath(QLabel):
    """
    Class implementing a label showing a file path compacted to fit its size.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent Widget (QWidget)
        """
        super().__init__(parent)
        
        self.__path = ''
        self.__surrounding = "{0}"
    
    def setSurrounding(self, surrounding):
        """
        Public method to set the surrounding of the path string.
        
        @param surrounding the a string containg placeholders for the path
            (string)
        """
        self.__surrounding = surrounding
        super().setText(
            self.__surrounding.format(self.__path))
    
    def setPath(self, path):
        """
        Public method to set the path of the label.
        
        @param path path to be shown (string)
        """
        self.__path = path
        super().setText(
            self.__surrounding.format(self.__path))
    
    def setTextPath(self, surrounding, path):
        """
        Public method to set the surrounding and the path of the label.
        
        @param surrounding the a string containg placeholders for the path
            (string)
        @param path path to be shown (string)
        """
        self.__surrounding = surrounding
        self.__path = path
        super().setText(
            self.__surrounding.format(self.__path))
    
    def paintEvent(self, event):
        """
        Protected method called when some painting is required.
        
        @param event reference to the paint event (QPaintEvent)
        """
        if self.length(self.__path) > self.contentsRect().width():
            super().setText(
                self.__surrounding.format(compactPath(self.__path,
                                          self.contentsRect().width(),
                                          self.length))
            )
        else:
            super().setText(
                self.__surrounding.format(self.__path))
        super().paintEvent(event)
    
    def length(self, txt):
        """
        Public method to return the length of a text in pixels.
        
        @param txt text to calculate the length for after wrapped (string)
        @return length of the wrapped text in pixels (integer)
        """
        fm = self.fontMetrics()
        try:
            return fm.horizontalAdvance(self.__surrounding.format(txt))
        except AttributeError:
            return fm.width(self.__surrounding.format(txt))
