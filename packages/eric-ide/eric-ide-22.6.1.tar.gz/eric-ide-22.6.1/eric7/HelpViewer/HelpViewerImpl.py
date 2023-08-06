# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the help viewer base class.
"""

from PyQt6.QtCore import pyqtSignal, QUrl


class HelpViewerImpl:
    """
    Class implementing the help viewer base class.
    
    This is the base class of help viewer implementations and defines the
    interface. Als subclasses must implement the these methods.
    
    @signal titleChanged() emitted to indicate a change of the page title
    @signal loadFinished(ok) emitted to indicate the completion of a page load
    @signal zoomChanged() emitted to indicate a change of the zoom level
    """
    titleChanged = pyqtSignal()
    loadFinished = pyqtSignal(bool)
    zoomChanged = pyqtSignal()
    
    def __init__(self, engine):
        """
        Constructor
        
        @param engine reference to the help engine
        @type QHelpEngine
        """
        self._engine = engine
    
    def setLink(self, url):
        """
        Public method to set the URL of the document to be shown.
        
        @param url URL of the document
        @type QUrl
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
    
    def link(self):
        """
        Public method to get the URL of the shown document.
        
        @return URL of the document
        @rtype QUrl
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return QUrl()
    
    def pageTitle(self):
        """
        Public method get the page title.
        
        @return page title
        @rtype str
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return ""
    
    def isEmptyPage(self):
        """
        Public method to check, if the current page is the empty page.
        
        @return flag indicating an empty page is loaded
        @rtype bool
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return False
    
    def gotoHistory(self, index):
        """
        Public method to step through the history.
        
        @param index history index (<0 backward, >0 forward)
        @type int
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
    
    def isBackwardAvailable(self):
        """
        Public method to check, if stepping backward through the history is
        available.
        
        @return flag indicating backward stepping is available
        @rtype bool
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return False
    
    def isForwardAvailable(self):
        """
        Public method to check, if stepping forward through the history is
        available.
        
        @return flag indicating forward stepping is available
        @rtype bool
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return False
    
    def scaleUp(self):
        """
        Public method to zoom in.
        
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
    
    def scaleDown(self):
        """
        Public method to zoom out.
        
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
    
    def setScale(self, scale):
        """
        Public method to set the zoom level.
        
        @param scale zoom level to set
        @type int
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
    
    def resetScale(self):
        """
        Public method to reset the zoom level.
        
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
    
    def scale(self):
        """
        Public method to get the zoom level.
        
        @return current zoom level
        @rtype int
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return 0
    
    def isScaleUpAvailable(self):
        """
        Public method to check, if the max. zoom level is reached.
        
        @return flag indicating scale up is available
        @rtype bool
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return False
    
    def isScaleDownAvailable(self):
        """
        Public method to check, if the min. zoom level is reached.
        
        @return flag indicating scale down is available
        @rtype bool
        @exception RuntimeError raised when not implemented
        """
        raise RuntimeError("Not implemented")
        return False
