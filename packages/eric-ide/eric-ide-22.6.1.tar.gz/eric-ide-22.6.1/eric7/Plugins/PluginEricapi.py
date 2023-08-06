# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Ericapi plugin.
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
name = "Ericapi Plugin"
author = "Detlev Offenbach <detlev@die-offenbachs.de>"
autoactivate = True
deactivateable = True
version = UI.Info.VersionOnly
className = "EricapiPlugin"
packageName = "__core__"
shortDescription = "Show the Ericapi dialogs."
longDescription = (
    """This plugin implements the Ericapi dialogs."""
    """ Ericapi is used to generate a QScintilla API file for Python and"""
    """ Ruby projects."""
)
pyqtApi = 2
# End-Of-Header

error = ""


def exeDisplayData():
    """
    Public method to support the display of some executable info.
    
    @return dictionary containing the data to query the presence of
        the executable
    """
    exe = 'eric7_api'
    if Utilities.isWindowsPlatform():
        exe = os.path.join(getConfig("bindir"), exe + '.cmd')
        if not os.path.exists(exe):
            exe = os.path.join(getConfig("bindir"), exe + '.bat')
    else:
        exe = os.path.join(getConfig("bindir"), exe)
    
    data = {
        "programEntry": True,
        "header": QCoreApplication.translate(
            "EricapiPlugin", "eric API File Generator"),
        "exe": exe,
        "versionCommand": '--version',
        "versionStartsWith": 'eric7_',
        "versionPosition": -3,
        "version": "",
        "versionCleanup": None,
    }
    
    return data


class EricapiPlugin(QObject):
    """
    Class implementing the Ericapi plugin.
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
                self.tr('Generate API file (eric7_api)'),
                self.tr('Generate &API file (eric7_api)'), 0, 0,
                self, 'doc_eric7_api')
            self.__projectAct.setStatusTip(self.tr(
                'Generate an API file using eric7_api'))
            self.__projectAct.setWhatsThis(self.tr(
                """<b>Generate API file</b>"""
                """<p>Generate an API file using eric7_api.</p>"""
            ))
            self.__projectAct.triggered.connect(self.__doEricapi)
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
    
    def __doEricapi(self):
        """
        Private slot to perform the eric7_api api generation.
        """
        from DocumentationPlugins.Ericapi.EricapiConfigDialog import (
            EricapiConfigDialog
        )
        eolTranslation = {
            '\r': 'cr',
            '\n': 'lf',
            '\r\n': 'crlf',
        }
        project = ericApp().getObject("Project")
        parms = project.getData('DOCUMENTATIONPARMS', "ERIC4API")
        dlg = EricapiConfigDialog(project, parms)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            args, parms = dlg.generateParameters()
            project.setData('DOCUMENTATIONPARMS', "ERIC4API", parms)
            
            # add parameter for the eol setting
            if not project.useSystemEol():
                args.append(
                    "--eol={0}".format(eolTranslation[project.getEolString()]))
            
            # now do the call
            from DocumentationPlugins.Ericapi.EricapiExecDialog import (
                EricapiExecDialog
            )
            dia = EricapiExecDialog("Ericapi")
            res = dia.start(args, project.ppath)
            if res:
                dia.exec()
            
            outputFileName = Utilities.toNativeSeparators(parms['outputFile'])
            
            # add output files to the project data, if they aren't in already
            for progLanguage in parms['languages']:
                if "%L" in outputFileName:
                    outfile = outputFileName.replace("%L", progLanguage)
                else:
                    if len(parms['languages']) == 1:
                        outfile = outputFileName
                    else:
                        root, ext = os.path.splitext(outputFileName)
                        outfile = "{0}-{1}{2}".format(
                            root, progLanguage.lower(), ext)
                
                outfile = project.getRelativePath(outfile)
                if outfile not in project.pdata['OTHERS']:
                    project.pdata['OTHERS'].append(outfile)
                    project.setDirty(True)
                    project.othersAdded(outfile)
