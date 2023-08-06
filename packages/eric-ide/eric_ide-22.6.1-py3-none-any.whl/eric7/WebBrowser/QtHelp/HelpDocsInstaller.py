# -*- coding: utf-8 -*-

# Copyright (c) 2009 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a thread class populating and updating the QtHelp
documentation database.
"""

import os

from PyQt6.QtCore import (
    pyqtSignal, QThread, Qt, QMutex, QDateTime, QDir, QLibraryInfo, QFileInfo
)
from PyQt6.QtHelp import QHelpEngineCore

from eric7config import getConfig

from Globals import qVersionTuple


class HelpDocsInstaller(QThread):
    """
    Class implementing the worker thread populating and updating the QtHelp
    documentation database.
    
    @signal errorMessage(str) emitted, if an error occurred during
        the installation of the documentation
    @signal docsInstalled(bool) emitted after the installation has finished
    """
    errorMessage = pyqtSignal(str)
    docsInstalled = pyqtSignal(bool)
    
    def __init__(self, collection):
        """
        Constructor
        
        @param collection full pathname of the collection file
        @type str
        """
        super().__init__()
        
        self.__abort = False
        self.__collection = collection
        self.__mutex = QMutex()
    
    def stop(self):
        """
        Public slot to stop the installation procedure.
        """
        if not self.isRunning():
            return
        
        self.__mutex.lock()
        self.__abort = True
        self.__mutex.unlock()
        self.wait()
    
    def installDocs(self):
        """
        Public method to start the installation procedure.
        """
        self.start(QThread.Priority.LowPriority)
    
    def run(self):
        """
        Public method executed by the thread.
        """
        engine = QHelpEngineCore(self.__collection)
        changes = False
        
        qt5Docs = [
            "activeqt", "qdoc", "qmake", "qt3d", "qt3drenderer",
            "qtandroidextras", "qtassistant", "qtbluetooth", "qtcanvas3d",
            "qtcharts", "qtcmake", "qtconcurrent", "qtcore", "qtdatavis3d",
            "qtdatavisualization", "qtdbus", "qtdesigner",
            "qtdistancefieldgenerator", "qtdoc", "qtenginio",
            "qtenginiooverview", "qtenginoqml", "qtgamepad",
            "qtgraphicaleffects", "qtgui", "qthelp", "qtimageformats",
            "qtlabscalendar", "qtlabsplatform", "qtlabscontrols", "qtlinguist",
            "qtlocation", "qtlottieanimation", "qtmaxextras", "qtmultimedia",
            "qtmultimediawidgets", "qtnetwork", "qtnetworkauth", "qtnfc",
            "qtopengl", "qtplatformheaders", "qtpositioning", "qtprintsupport",
            "qtpurchasing", "qtqml", "qtqmlmodels", "qtqmltest", "qtquick",
            "qtquick3d", "qtquickcontrols", "qtquickcontrols1",
            "qtquickdialogs", "qtquickextras", "qtquicklayouts",
            "qtquicktimeline", "qtremoteobjects", "qtscript", "qtscripttools",
            "qtscxml", "qtsensors", "qtserialbus", "qtserialport",
            "qtshadertools", "qtspeech", "qtsql", "qtsvg", "qttest",
            "qttestlib", "qtuitools", "qtvirtualkeyboard",
            "qtwaylandcompositor", "qtwebchannel", "qtwebengine",
            "qtwebenginewidgets", "qtwebkit", "qtwebkitexamples",
            "qtwebsockets", "qtwebview", "qtwidgets", "qtwinextras",
            "qtx11extras", "qtxml", "qtxmlpatterns"]
        for qtDocs, version in [(qt5Docs, 5)]:
            for doc in qtDocs:
                changes |= self.__installQtDoc(doc, version, engine)
                self.__mutex.lock()
                if self.__abort:
                    engine = None
                    self.__mutex.unlock()
                    return
                self.__mutex.unlock()
        
        changes |= self.__installEric7Doc(engine)
        engine = None
        del engine
        self.docsInstalled.emit(changes)
    
    def __installQtDoc(self, name, version, engine):
        """
        Private method to install/update a Qt help document.
        
        @param name name of the Qt help document
        @type str
        @param version Qt version of the help documents
        @type int
        @param engine reference to the help engine
        @type QHelpEngineCore
        @return flag indicating success
        @rtype bool
        """
        versionKey = "qt_version_{0}@@{1}".format(version, name)
        info = engine.customValue(versionKey, "")
        lst = info.split('|')
        
        dt = QDateTime()
        if len(lst) and lst[0]:
            dt = QDateTime.fromString(lst[0], Qt.DateFormat.ISODate)
        
        qchFile = ""
        if len(lst) == 2:
            qchFile = lst[1]
        
        if version == 5:
            docsPath = QLibraryInfo.path(
                QLibraryInfo.LibraryPath.DocumentationPath)
            if (
                not os.path.isdir(docsPath) or
                len(QDir(docsPath).entryList(["*.qch"])) == 0
            ):
                docsPathList = QDir.fromNativeSeparators(docsPath).split("/")
                docsPath = os.sep.join(
                    docsPathList[:-3] +
                    ["Docs", "Qt-{0}.{1}".format(*qVersionTuple())])
            docsPath = QDir(docsPath)
        else:
            # unsupported Qt version
            return False
        
        files = docsPath.entryList(["*.qch"])
        if not files:
            engine.setCustomValue(
                versionKey,
                QDateTime().toString(Qt.DateFormat.ISODate) + '|')
            return False
        
        for f in files:
            if f.startswith(name + "."):
                fi = QFileInfo(docsPath.absolutePath() + QDir.separator() + f)
                namespace = QHelpEngineCore.namespaceName(
                    fi.absoluteFilePath())
                if not namespace:
                    continue
                
                if (
                    dt.isValid() and
                    namespace in engine.registeredDocumentations() and
                    (fi.lastModified().toString(Qt.DateFormat.ISODate) ==
                     dt.toString(Qt.DateFormat.ISODate)) and
                    qchFile == fi.absoluteFilePath()
                ):
                    return False
                
                if namespace in engine.registeredDocumentations():
                    engine.unregisterDocumentation(namespace)
                
                if not engine.registerDocumentation(fi.absoluteFilePath()):
                    self.errorMessage.emit(
                        self.tr(
                            """<p>The file <b>{0}</b> could not be"""
                            """ registered. <br/>Reason: {1}</p>""")
                        .format(fi.absoluteFilePath, engine.error())
                    )
                    return False
                
                engine.setCustomValue(
                    versionKey,
                    fi.lastModified().toString(Qt.DateFormat.ISODate) + '|' +
                    fi.absoluteFilePath())
                return True
        
        return False
    
    def __installEric7Doc(self, engine):
        """
        Private method to install/update the eric help documentation.
        
        @param engine reference to the help engine
        @type QHelpEngineCore
        @return flag indicating success
        @rtype bool
        """
        versionKey = "eric7_ide"
        info = engine.customValue(versionKey, "")
        lst = info.split('|')
        
        dt = QDateTime()
        if len(lst) and lst[0]:
            dt = QDateTime.fromString(lst[0], Qt.DateFormat.ISODate)
        
        qchFile = ""
        if len(lst) == 2:
            qchFile = lst[1]
        
        docsPath = QDir(getConfig("ericDocDir") + QDir.separator() + "Help")
        
        files = docsPath.entryList(["*.qch"])
        if not files:
            engine.setCustomValue(
                versionKey, QDateTime().toString(Qt.DateFormat.ISODate) + '|')
            return False
        
        for f in files:
            if f == "source.qch":
                fi = QFileInfo(docsPath.absolutePath() + QDir.separator() + f)
                namespace = QHelpEngineCore.namespaceName(
                    fi.absoluteFilePath())
                if not namespace:
                    continue
                
                if (
                    dt.isValid() and
                    namespace in engine.registeredDocumentations() and
                    (fi.lastModified().toString(Qt.DateFormat.ISODate) ==
                     dt.toString(Qt.DateFormat.ISODate)) and
                    qchFile == fi.absoluteFilePath()
                ):
                    return False
                
                if namespace in engine.registeredDocumentations():
                    engine.unregisterDocumentation(namespace)
                
                if not engine.registerDocumentation(fi.absoluteFilePath()):
                    self.errorMessage.emit(
                        self.tr(
                            """<p>The file <b>{0}</b> could not be"""
                            """ registered. <br/>Reason: {1}</p>""")
                        .format(fi.absoluteFilePath, engine.error())
                    )
                    return False
                
                engine.setCustomValue(
                    versionKey,
                    fi.lastModified().toString(Qt.DateFormat.ISODate) + '|' +
                    fi.absoluteFilePath())
                return True
        
        return False
