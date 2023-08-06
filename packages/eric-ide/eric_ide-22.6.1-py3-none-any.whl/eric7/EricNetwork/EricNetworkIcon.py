# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a statusbar icon tracking the network status.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtNetwork import QNetworkInformation
from PyQt6.QtWidgets import QLabel

import UI.PixmapCache
import Preferences


class EricNetworkIcon(QLabel):
    """
    Class implementing a statusbar icon tracking the network status.
    
    @signal onlineStateChanged(online) emitted to indicate a change of the
        network state
    @signal reachabilityStateChanged(reachability) emitted to indicate a
        change of the network reachability
    """
    onlineStateChanged = pyqtSignal(bool)
    reachabilityStateChanged = pyqtSignal(QNetworkInformation.Reachability)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        
        if (
            Preferences.getUI("DynamicOnlineCheck") and
            QNetworkInformation.load(QNetworkInformation.Feature.Reachability)
        ):
            self.__online = (
                QNetworkInformation.instance().reachability() ==
                QNetworkInformation.Reachability.Online
            )
            self.__reachabilityChanged(
                QNetworkInformation.instance().reachability())
            QNetworkInformation.instance().reachabilityChanged.connect(
                self.__reachabilityChanged)
        else:
            # assume to be 'always online' if no backend could be loaded or
            # dynamic online check is switched of
            self.__online = True
            self.__reachabilityChanged(QNetworkInformation.Reachability.Online)
    
    def __reachabilityChanged(self, reachability):
        """
        Private slot handling reachability state changes.
        
        @param reachability new reachability state
        @type QNetworkInformation.Reachability
        """
        online = reachability == QNetworkInformation.Reachability.Online
        tooltip = self.tr("<p>Shows the Internet reachability status<br/><br/>"
                          "<b>Internet:</b> {0}</p>")
        
        if online:
            self.setPixmap(UI.PixmapCache.getPixmap("network-online"))
            tooltip = tooltip.format(self.tr("Reachable"))
        else:
            self.setPixmap(UI.PixmapCache.getPixmap("network-offline"))
            tooltip = tooltip.format(self.tr("Not Reachable"))
        
        self.setToolTip(tooltip)
        
        if online != self.__online:
            self.__online = online
            self.onlineStateChanged.emit(online)
        
        self.reachabilityStateChanged.emit(reachability)
    
    def isOnline(self):
        """
        Public method to get the online state.
        
        @return online state
        @rtype bool
        """
        return self.__online
