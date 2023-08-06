# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a JSON based reader class.
"""

import json

from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtNetwork import QTcpServer, QHostAddress

from EricWidgets import EricMessageBox

import Preferences
import Utilities


class EricJsonReader(QTcpServer):
    """
    Class implementing a JSON based reader class.
    
    The reader is responsible for opening a socket to listen for writer
    connections.
    
    @signal dataReceived(object) emitted after a data object was received
    """
    dataReceived = pyqtSignal(object)
    
    def __init__(self, name="", ip=None, parent=None):
        """
        Constructor
        
        @param name name of the server (used for output only)
        @type str
        @param ip IP address to listen at
        @type str
        @param parent parent object
        @type QObject
        """
        super().__init__(parent)
        
        self.__name = name
        self.__connection = None
        
        # setup the network interface
        if ip is None:
            networkInterface = Preferences.getDebugger("NetworkInterface")
            if networkInterface == "all" or '.' in networkInterface:
                # IPv4
                self.__hostAddress = '127.0.0.1'
            else:
                # IPv6
                self.__hostAddress = '::1'
        else:
            self.__hostAddress = ip
        self.listen(QHostAddress(self.__hostAddress))

        self.newConnection.connect(self.handleNewConnection)
        
        ## Note: Need the port if writer is started external in debugger.
        print('JSON reader ({1}) listening on: {0:d}'   # __IGNORE_WARNING__
              .format(self.serverPort(), self.__name))
    
    def address(self):
        """
        Public method to get the host address.
        
        @return host address
        @rtype str
        """
        return self.__hostAddress
    
    def port(self):
        """
        Public method to get the port number to connect to.
        
        @return port number
        @rtype int
        """
        return self.serverPort()
    
    @pyqtSlot()
    def handleNewConnection(self):
        """
        Public slot for new incoming connections from a writer.
        """
        connection = self.nextPendingConnection()
        if not connection.isValid():
            return
        
        if self.__connection is not None:
            self.__connection.close()
        
        self.__connection = connection
        
        connection.readyRead.connect(self.__receiveJson)
        connection.disconnected.connect(self.__handleDisconnect)
    
    @pyqtSlot()
    def __handleDisconnect(self):
        """
        Private slot handling a disconnect of the writer.
        """
        if self.__connection is not None:
            self.__receiveJson()    # read all buffered data first
            self.__connection.close()
        
        self.__connection = None
    
    @pyqtSlot()
    def __receiveJson(self):
        """
        Private slot handling received data from the writer.
        """
        while self.__connection and self.__connection.canReadLine():
            dataStr = self.__connection.readLine()
            jsonLine = bytes(dataStr).decode("utf-8", 'backslashreplace')
            
            #- print("JSON Reader ({0}): {1}".format(self.__name, jsonLine))
            #- this is for debugging only
            
            try:
                data = json.loads(jsonLine.strip())
            except (TypeError, ValueError) as err:
                EricMessageBox.critical(
                    None,
                    self.tr("JSON Protocol Error"),
                    self.tr("""<p>The data received from the writer"""
                            """ could not be decoded. Please report"""
                            """ this issue with the received data to the"""
                            """ eric bugs email address.</p>"""
                            """<p>Error: {0}</p>"""
                            """<p>Data:<br/>{1}</p>""").format(
                        str(err), Utilities.html_encode(jsonLine.strip())),
                    EricMessageBox.Ok)
                return
            
            self.dataReceived.emit(data)
