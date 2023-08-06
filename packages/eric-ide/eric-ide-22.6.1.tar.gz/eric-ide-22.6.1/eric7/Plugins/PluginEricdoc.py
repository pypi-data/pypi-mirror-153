# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Ericdoc plugin.
"""

import os

from PyQt6.QtCore import QObject, QCoreApplication
from PyQt6.QtWidgets import QDialog

from EricWidgets.EricApplication import ericApp

from EricGui.EricAction import EricAction

import Utilities
import UI.Info

from eric7config import getConfig

# Start-Of-Header
name = "Ericdoc Plugin"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = UI.Info.VersionOnly
className = "EricdocPlugin"
packageName = "__core__"
shortDescription = "Show the Ericdoc dialogs."
longDescription = (
    """This plugin implements the Ericdoc dialogs."""
    """ Ericdoc is used to generate a source code documentation"""
    """ for Python and Ruby projects."""
)
pyqtApi = 2
# End-Of-Header

error = ""


def exeDisplayDataList():
    """
    Public method to support the display of some executable info.
    
    @return dictionary containing the data to query the presence of
        the executable
    """
    dataList = []
    
    # 1. eric7_doc
    exe = 'eric7_doc'
    if Utilities.isWindowsPlatform():
        exe = os.path.join(getConfig("bindir"), exe + '.cmd')
        if not os.path.exists(exe):
            exe = os.path.join(getConfig("bindir"), exe + '.bat')
    else:
        exe = os.path.join(getConfig("bindir"), exe)
    dataList.append({
        "programEntry": True,
        "header": QCoreApplication.translate(
            "EricdocPlugin", "eric Documentation Generator"),
        "exe": exe,
        "versionCommand": '--version',
        "versionStartsWith": 'eric7_',
        "versionPosition": -3,
        "version": "",
        "versionCleanup": None,
    })
    
    # 2. Qt Help Generator
    exe = os.path.join(
        Utilities.getQtBinariesPath(),
        Utilities.generateQtToolName('qhelpgenerator')
    )
    if Utilities.isWindowsPlatform():
        exe += '.exe'
    dataList.append({
        "programEntry": True,
        "header": QCoreApplication.translate(
            "EricdocPlugin", "Qt Help Tools"),
        "exe": exe,
        "versionCommand": '-v',
        "versionStartsWith": 'Qt',
        "versionPosition": -1,
        "version": "",
        "versionCleanup": (0, -1),
    })
    
    return dataList


class EricdocPlugin(QObject):
    """
    Class implementing the Ericdoc plugin.
    """
    def __init__(self, ui):
        """
        Constructor
        
        @param ui reference to the user interface object (UI.UserInterface)
        """
        super().__init__(ui)
        self.__ui = ui
        self.__initialize()
        
    def __initialize(self):
        """
        Private slot to (re)initialize the plugin.
        """
        self.__projectAct = None

    def activate(self):
        """
        Public method to activate this plugin.
        
        @return tuple of None and activation status (boolean)
        """
        menu = ericApp().getObject("Project").getMenu("Apidoc")
        if menu:
            self.__projectAct = EricAction(
                self.tr('Generate documentation (eric7_doc)'),
                self.tr('Generate &documentation (eric7_doc)'), 0, 0,
                self, 'doc_eric7_doc')
            self.__projectAct.setStatusTip(
                self.tr('Generate API documentation using eric7_doc'))
            self.__projectAct.setWhatsThis(self.tr(
                """<b>Generate documentation</b>"""
                """<p>Generate API documentation using eric7_doc.</p>"""
            ))
            self.__projectAct.triggered.connect(self.__doEricdoc)
            ericApp().getObject("Project").addEricActions([self.__projectAct])
            menu.addAction(self.__projectAct)
        
        ericApp().getObject("Project").showMenu.connect(self.__projectShowMenu)
        
        return None, True

    def deactivate(self):
        """
        Public method to deactivate this plugin.
        """
        ericApp().getObject("Project").showMenu.disconnect(
            self.__projectShowMenu)
        
        menu = ericApp().getObject("Project").getMenu("Apidoc")
        if menu:
            menu.removeAction(self.__projectAct)
            ericApp().getObject("Project").removeEricActions(
                [self.__projectAct])
        self.__initialize()
    
    def __projectShowMenu(self, menuName, menu):
        """
        Private slot called, when the the project menu or a submenu is
        about to be shown.
        
        @param menuName name of the menu to be shown (string)
        @param menu reference to the menu (QMenu)
        """
        if menuName == "Apidoc" and self.__projectAct is not None:
            self.__projectAct.setEnabled(
                ericApp().getObject("Project").getProjectLanguage() in
                ["Python", "Python3", "Ruby", "MicroPython"])
    
    def __doEricdoc(self):
        """
        Private slot to perform the eric7_doc api documentation generation.
        """
        from DocumentationPlugins.Ericdoc.EricdocConfigDialog import (
            EricdocConfigDialog
        )
        eolTranslation = {
            '\r': 'cr',
            '\n': 'lf',
            '\r\n': 'crlf',
        }
        project = ericApp().getObject("Project")
        parms = project.getData('DOCUMENTATIONPARMS', "ERIC4DOC")
        dlg = EricdocConfigDialog(project, parms)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            args, parms = dlg.generateParameters()
            project.setData('DOCUMENTATIONPARMS', "ERIC4DOC", parms)
            
            # add parameter for the eol setting
            if not project.useSystemEol():
                args.append(
                    "--eol={0}".format(eolTranslation[project.getEolString()]))
            
            # now do the call
            from DocumentationPlugins.Ericdoc.EricdocExecDialog import (
                EricdocExecDialog
            )
            dia = EricdocExecDialog("Ericdoc")
            res = dia.start(args, project.ppath)
            if res:
                dia.exec()
            
            outdir = Utilities.toNativeSeparators(parms['outputDirectory'])
            if outdir == '':
                outdir = 'doc'      # that is eric7_docs default output dir
                
            # add it to the project data, if it isn't in already
            outdir = project.getRelativePath(outdir)
            if outdir not in project.pdata['OTHERS']:
                project.pdata['OTHERS'].append(outdir)
                project.setDirty(True)
                project.othersAdded(outdir)
            
            if parms['qtHelpEnabled']:
                outdir = Utilities.toNativeSeparators(
                    parms['qtHelpOutputDirectory'])
                if outdir == '':
                    outdir = 'help'
                    # that is eric7_docs default QtHelp output dir
                    
                # add it to the project data, if it isn't in already
                outdir = project.getRelativePath(outdir)
                if outdir not in project.pdata['OTHERS']:
                    project.pdata['OTHERS'].append(outdir)
                    project.setDirty(True)
                    project.othersAdded(outdir)
