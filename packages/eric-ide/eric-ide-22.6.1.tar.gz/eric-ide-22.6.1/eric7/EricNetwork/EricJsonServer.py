# -*- coding: utf-8 -*-

# Copyright (c) 2017 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the JSON based server base class.
"""

import contextlib
import json

from PyQt6.QtCore import (
    pyqtSlot, QProcess, QProcessEnvironment, QCoreApplication, QEventLoop,
    QTimer, QThread
)
from PyQt6.QtNetwork import QTcpServer, QHostAddress

from EricWidgets import EricMessageBox

import Preferences
import Utilities


class EricJsonServer(QTcpServer):
    """
    Class implementing a JSON based server base class.
    """
    def __init__(self, name="", multiplex=False, parent=None):
        """
        Constructor
        
        @param name name of the server (used for output only)
        @type str
        @param multiplex flag indicating a multiplexing server
        @type bool
        @param parent parent object
        @type QObject
        """
        super().__init__(parent)
        
        self.__name = name
        self.__multiplex = multiplex
        if self.__multiplex:
            self.__clientProcesses = {}
            self.__connections = {}
        else:
            self.__clientProcess = None
            self.__connection = None
        
        # setup the network interface
        networkInterface = Preferences.getDebugger("NetworkInterface")
        if networkInterface == "all" or '.' in networkInterface:
            # IPv4
            self.__hostAddress = '127.0.0.1'
        else:
            # IPv6
            self.__hostAddress = '::1'
        self.listen(QHostAddress(self.__hostAddress))

        self.newConnection.connect(self.handleNewConnection)
        
        ## Note: Need the port if client is started external in debugger.
        print('JSON server ({1}) listening on: {0:d}'   # __IGNORE_WARNING__
              .format(self.serverPort(), self.__name))
    
    @pyqtSlot()
    def handleNewConnection(self):
        """
        Public slot for new incoming connections from a client.
        """
        connection = self.nextPendingConnection()
        if not connection.isValid():
            return
        
        if self.__multiplex:
            if not connection.waitForReadyRead(3000):
                return
            idString = bytes(connection.readLine()).decode(
                "utf-8", 'backslashreplace').strip()
            if idString in self.__connections:
                self.__connections[idString].close()
            self.__connections[idString] = connection
        else:
            idString = ""
            if self.__connection is not None:
                self.__connection.close()
            
            self.__connection = connection
        
        connection.readyRead.connect(
            lambda: self.__receiveJson(idString))
        connection.disconnected.connect(
            lambda: self.__handleDisconnect(idString))
    
    @pyqtSlot()
    def __handleDisconnect(self, idString):
        """
        Private slot handling a disconnect of the client.
        
        @param idString id of the connection been disconnected
        @type str
        """
        if idString:
            if idString in self.__connections:
                self.__connections[idString].close()
                del self.__connections[idString]
        else:
            if self.__connection is not None:
                self.__connection.close()
            
            self.__connection = None
    
    def connectionNames(self):
        """
        Public method to get the list of active connection names.
        
        If this is not a multiplexing server, an empty list is returned.
        
        @return list of active connection names
        @rtype list of str
        """
        if self.__multiplex:
            return list(self.__connections.keys())
        else:
            return []
    
    @pyqtSlot()
    def __receiveJson(self, idString):
        """
        Private slot handling received data from the client.
        
        @param idString id of the connection
        @type str
        """
        if idString:
            try:
                connection = self.__connections[idString]
            except KeyError:
                connection = None
        else:
            connection = self.__connection
        
        while connection and connection.canReadLine():
            data = connection.readLine()
            jsonLine = bytes(data).decode("utf-8", 'backslashreplace')
            
            #- print("JSON Server ({0}): {1}".format(self.__name, jsonLine))
            #- this is for debugging only
            
            try:
                clientDict = json.loads(jsonLine.strip())
            except (TypeError, ValueError) as err:
                EricMessageBox.critical(
                    None,
                    self.tr("JSON Protocol Error"),
                    self.tr("""<p>The response received from the client"""
                            """ could not be decoded. Please report"""
                            """ this issue with the received data to the"""
                            """ eric bugs email address.</p>"""
                            """<p>Error: {0}</p>"""
                            """<p>Data:<br/>{1}</p>""").format(
                        str(err), Utilities.html_encode(jsonLine.strip())),
                    EricMessageBox.Ok)
                return
            
            self.handleCall(clientDict["method"], clientDict["params"])
    
    def sendJson(self, command, params, flush=False, idString=""):
        """
        Public method to send a single command to a client.
        
        @param command command name to be sent
        @type str
        @param params dictionary of named parameters for the command
        @type dict
        @param flush flag indicating to flush the data to the socket
        @type bool
        @param idString id of the connection to send data to
        @type str
        """
        commandDict = {
            "jsonrpc": "2.0",
            "method": command,
            "params": params,
        }
        cmd = json.dumps(commandDict) + '\n'
        
        if idString:
            try:
                connection = self.__connections[idString]
            except KeyError:
                connection = None
        else:
            connection = self.__connection
        
        if connection is not None:
            data = cmd.encode('utf8', 'backslashreplace')
            length = "{0:09d}".format(len(data))
            connection.write(length.encode() + data)
            if flush:
                connection.flush()
    
    def startClient(self, interpreter, clientScript, clientArgs, idString="",
                    environment=None):
        """
        Public method to start a client process.
        
        @param interpreter interpreter to be used for the client
        @type str
        @param clientScript path to the client script
        @type str
        @param clientArgs list of arguments for the client
        @param idString id of the client to be started
        @type str
        @param environment dictionary of environment settings to pass
        @type dict
        @return flag indicating a successful client start and the exit code
            in case of an issue
        @rtype bool, int
        """
        if interpreter == "" or not Utilities.isinpath(interpreter):
            return False
        
        exitCode = None
        
        proc = QProcess()
        proc.setProcessChannelMode(
            QProcess.ProcessChannelMode.ForwardedChannels)
        if environment is not None:
            env = QProcessEnvironment()
            for key, value in list(environment.items()):
                env.insert(key, value)
            proc.setProcessEnvironment(env)
        args = [clientScript, self.__hostAddress, str(self.serverPort())]
        if idString:
            args.append(idString)
        args.extend(clientArgs)
        proc.start(interpreter, args)
        if not proc.waitForStarted(10000):
            proc = None
        
        if idString:
            self.__clientProcesses[idString] = proc
            if proc:
                timer = QTimer()
                timer.setSingleShot(True)
                timer.start(30000)           # 30s timeout
                while (
                    idString not in self.connectionNames() and
                    timer.isActive()
                ):
                    # Give the event loop the chance to process the new
                    # connection of the client (= slow start).
                    QCoreApplication.processEvents(
                        QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
                    QThread.msleep(100)
                    
                    # check if client exited prematurely
                    if proc.state() == QProcess.ProcessState.NotRunning:
                        exitCode = proc.exitCode()
                        proc = None
                        self.__clientProcesses[idString] = None
                        break
                    
                    QThread.msleep(500)
        else:
            if proc:
                timer = QTimer()
                timer.setSingleShot(True)
                timer.start(1000)           # 1s timeout
                while timer.isActive():
                    # check if client exited prematurely
                    QCoreApplication.processEvents(
                        QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
                    QThread.msleep(100)
                    if proc.state() == QProcess.ProcessState.NotRunning:
                        exitCode = proc.exitCode()
                        proc = None
                        break
            self.__clientProcess = proc
        
        return proc is not None, exitCode
    
    def stopClient(self, idString=""):
        """
        Public method to stop a client process.
        
        @param idString id of the client to be stopped
        @type str
        """
        self.sendJson("Exit", {}, flush=True, idString=idString)
        
        if idString:
            try:
                connection = self.__connections[idString]
            except KeyError:
                connection = None
        else:
            connection = self.__connection
        if connection is not None:
            connection.waitForDisconnected()
        
        if idString:
            with contextlib.suppress(KeyError):
                if self .__clientProcesses[idString] is not None:
                    self .__clientProcesses[idString].close()
                del self.__clientProcesses[idString]
        else:
            if self.__clientProcess is not None:
                self.__clientProcess.close()
                self.__clientProcess = None
    
    def stopAllClients(self):
        """
        Public method to stop all clients.
        """
        clientNames = self.connectionNames()[:]
        for clientName in clientNames:
            self.stopClient(clientName)
    
    #######################################################################
    ## The following methods should be overridden by derived classes
    #######################################################################
    
    def handleCall(self, method, params):
        """
        Public method to handle a method call from the client.
        
        Note: This is an empty implementation that must be overridden in
        derived classes.
        
        @param method requested method name
        @type str
        @param params dictionary with method specific parameters
        @type dict
        """
        pass
