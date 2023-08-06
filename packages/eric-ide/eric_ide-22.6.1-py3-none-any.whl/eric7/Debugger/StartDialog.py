# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Start Program dialog.
"""

import os

from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QComboBox, QInputDialog

from EricWidgets.EricPathPicker import EricPathPickerModes
from EricWidgets.EricApplication import ericApp

import Preferences


class StartDialog(QDialog):
    """
    Class implementing the Start Program dialog.
    
    It implements a dialog that is used to start an
    application for debugging. It asks the user to enter
    the commandline parameters, the working directory and
    whether exception reporting should be disabled.
    """
    def __init__(self, caption, lastUsedVenvName, argvList, wdList, envList,
                 exceptions,
                 parent=None, dialogType=0, modfuncList=None,
                 tracePython=False, autoClearShell=True, autoContinue=True,
                 enableMultiprocess=False, multiprocessNoDebugHistory=None,
                 configOverride=None,
                 forProject=False, scriptName="", scriptsList=None):
        """
        Constructor
        
        @param caption the caption to be displayed
        @type str
        @param lastUsedVenvName name of the most recently used virtual
            environment
        @type str
        @param argvList history list of command line arguments
        @type list of str
        @param wdList history list of working directories
        @type list of str
        @param envList history list of environment parameter settings
        @type list of str
        @param exceptions exception reporting flag
        @type bool
        @param parent parent widget of this dialog
        @type QWidget
        @param dialogType type of the start dialog
                <ul>
                <li>0 = start debug dialog</li>
                <li>1 = start run dialog</li>
                <li>2 = start coverage dialog</li>
                <li>3 = start profile dialog</li>
                </ul>
        @type int (0 to 3)
        @param modfuncList history list of module functions
        @type list of str
        @param tracePython flag indicating if the Python library should
            be traced as well
        @type bool
        @param autoClearShell flag indicating, that the interpreter window
            should be cleared automatically
        @type bool
        @param autoContinue flag indicating, that the debugger should not
            stop at the first executable line
        @type bool
        @param enableMultiprocess flag indicating the support for multi process
            debugging
        @type bool
        @param multiprocessNoDebugHistory list of lists with programs not to be
            debugged
        @type list of str
        @param configOverride dictionary containing the global config override
            data
        @type dict
        @param forProject flag indicating to get the parameters for a
            run/debug/... action for a project
        @type bool
        @param scriptName name of the script
        @type str
        @param scriptsList history list of script names
        @type list of str
        """
        super().__init__(parent)
        self.setModal(True)
        
        self.dialogType = dialogType
        if dialogType == 0:
            from .Ui_StartDebugDialog import Ui_StartDebugDialog
            self.ui = Ui_StartDebugDialog()
        elif dialogType == 1:
            from .Ui_StartRunDialog import Ui_StartRunDialog
            self.ui = Ui_StartRunDialog()
        elif dialogType == 2:
            from .Ui_StartCoverageDialog import Ui_StartCoverageDialog
            self.ui = Ui_StartCoverageDialog()
        elif dialogType == 3:
            from .Ui_StartProfileDialog import Ui_StartProfileDialog
            self.ui = Ui_StartProfileDialog()
        self.ui.setupUi(self)
        
        self.ui.venvComboBox.addItem("")
        self.ui.venvComboBox.addItems(
            sorted(ericApp().getObject("VirtualEnvManager")
                   .getVirtualenvNames()))
        
        self.ui.scriptnamePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.ui.scriptnamePicker.setDefaultDirectory(
            Preferences.getMultiProject("Workspace"))
        self.ui.scriptnamePicker.setInsertPolicy(
            QComboBox.InsertPolicy.InsertAtTop)
        self.ui.scriptnamePicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        self.ui.scriptnamePicker.setFilters(self.tr(
            "Python Files (*.py *.py3);;"
            "Python GUI Files (*.pyw *.pyw3);;"
            "All Files (*)"
        ))
        self.ui.scriptnamePicker.setEnabled(not forProject)
        
        self.ui.workdirPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.ui.workdirPicker.setDefaultDirectory(
            Preferences.getMultiProject("Workspace"))
        self.ui.workdirPicker.setInsertPolicy(
            QComboBox.InsertPolicy.InsertAtTop)
        self.ui.workdirPicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        
        self.clearButton = self.ui.buttonBox.addButton(
            self.tr("Clear Histories"), QDialogButtonBox.ButtonRole.ActionRole)
        self.editButton = self.ui.buttonBox.addButton(
            self.tr("Edit History"), QDialogButtonBox.ButtonRole.ActionRole)
        
        self.setWindowTitle(caption)
        self.ui.cmdlineCombo.clear()
        self.ui.cmdlineCombo.addItems(argvList)
        if len(argvList) > 0:
            self.ui.cmdlineCombo.setCurrentIndex(0)
        self.ui.workdirPicker.clear()
        self.ui.workdirPicker.addItems(wdList)
        if len(wdList) > 0:
            self.ui.workdirPicker.setCurrentIndex(0)
        self.ui.environmentCombo.clear()
        self.ui.environmentCombo.addItems(envList)
        self.ui.exceptionCheckBox.setChecked(exceptions)
        self.ui.clearShellCheckBox.setChecked(autoClearShell)
        self.ui.consoleCheckBox.setEnabled(
            Preferences.getDebugger("ConsoleDbgCommand") != "")
        self.ui.consoleCheckBox.setChecked(False)
        venvIndex = max(0, self.ui.venvComboBox.findText(lastUsedVenvName))
        self.ui.venvComboBox.setCurrentIndex(venvIndex)
        self.ui.globalOverrideGroup.setChecked(configOverride["enable"])
        self.ui.redirectCheckBox.setChecked(configOverride["redirect"])
        
        self.ui.scriptnamePicker.addItems(scriptsList)
        self.ui.scriptnamePicker.setText(scriptName)
        
        if dialogType == 0:        # start debug dialog
            enableMultiprocessGlobal = Preferences.getDebugger(
                "MultiProcessEnabled")
            self.ui.tracePythonCheckBox.setChecked(tracePython)
            self.ui.tracePythonCheckBox.show()
            self.ui.autoContinueCheckBox.setChecked(autoContinue)
            self.ui.multiprocessGroup.setEnabled(enableMultiprocessGlobal)
            self.ui.multiprocessGroup.setChecked(
                enableMultiprocess & enableMultiprocessGlobal)
            self.ui.multiprocessNoDebugCombo.clear()
            self.ui.multiprocessNoDebugCombo.setToolTip(self.tr(
                "Enter the list of programs or program patterns not to be"
                " debugged separated by '{0}'.").format(os.pathsep)
            )
            if multiprocessNoDebugHistory:
                self.ui.multiprocessNoDebugCombo.addItems(
                    multiprocessNoDebugHistory)
                self.ui.multiprocessNoDebugCombo.setCurrentIndex(0)
        
        if dialogType == 3:       # start coverage or profile dialog
            self.ui.eraseCheckBox.setChecked(True)
        
        self.__clearHistoryLists = False
        self.__historiesModified = False
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
        
    def on_modFuncCombo_editTextChanged(self):
        """
        Private slot to enable/disable the OK button.
        """
        self.ui.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setDisabled(
                self.ui.modFuncCombo.currentText() == "")
        
    def getData(self):
        """
        Public method to retrieve the data entered into this dialog.
        
        @return a tuple of virtual environment, script name, argv, workdir,
            environment, exceptions flag, clear interpreter flag and run in
            console flag
        @rtype tuple of (str, str, str, str, str, bool, bool, bool)
        """
        cmdLine = self.ui.cmdlineCombo.currentText()
        workdir = self.ui.workdirPicker.currentText(toNative=False)
        environment = self.ui.environmentCombo.currentText()
        venvName = self.ui.venvComboBox.currentText()
        scriptName = (
            self.ui.scriptnamePicker.currentText()
            if self.ui.scriptnamePicker.isEnabled() else
            ""
        )
        
        return (venvName,
                scriptName,
                cmdLine,
                workdir,
                environment,
                self.ui.exceptionCheckBox.isChecked(),
                self.ui.clearShellCheckBox.isChecked(),
                self.ui.consoleCheckBox.isChecked(),
                )
    
    def getGlobalOverrideData(self):
        """
        Public method to retrieve the global configuration override data
        entered into this dialog.
        
        @return dictionary containing a flag indicating to activate the global
            override and a flag indicating a redirect of stdin/stdout/stderr
        @rtype dict
        """
        return {
            "enable": self.ui.globalOverrideGroup.isChecked(),
            "redirect": self.ui.redirectCheckBox.isChecked(),
        }
    
    def getDebugData(self):
        """
        Public method to retrieve the debug related data entered into this
        dialog.
        
        @return a tuple of a flag indicating, if the Python library should be
            traced as well, a flag indicating, that the debugger should not
            stop at the first executable line, a flag indicating to support
            multi process debugging and a space separated list of programs not
            to be debugged
        @rtype tuple of (bool, bool, bool, str)
        """
        if self.dialogType == 0:
            return (self.ui.tracePythonCheckBox.isChecked(),
                    self.ui.autoContinueCheckBox.isChecked(),
                    self.ui.multiprocessGroup.isChecked(),
                    self.ui.multiprocessNoDebugCombo.currentText())
        else:
            return (False, False, False, "")
    
    def getCoverageData(self):
        """
        Public method to retrieve the coverage related data entered into this
        dialog.
        
        @return flag indicating erasure of coverage info
        @rtype bool
        """
        if self.dialogType == 2:
            return self.ui.eraseCheckBox.isChecked()
        else:
            return False
        
    def getProfilingData(self):
        """
        Public method to retrieve the profiling related data entered into this
        dialog.
        
        @return flag indicating erasure of profiling info
        @rtype bool
        """
        if self.dialogType == 3:
            return self.ui.eraseCheckBox.isChecked()
        else:
            return False
        
    def __clearHistories(self):
        """
        Private slot to clear the combo boxes lists and record a flag to
        clear the lists.
        """
        self.__clearHistoryLists = True
        self.__historiesModified = False    # clear catches it all
        
        cmdLine = self.ui.cmdlineCombo.currentText()
        workdir = self.ui.workdirPicker.currentText()
        environment = self.ui.environmentCombo.currentText()
        scriptName = self.ui.scriptnamePicker.currentText()
        
        self.ui.cmdlineCombo.clear()
        self.ui.workdirPicker.clear()
        self.ui.environmentCombo.clear()
        self.ui.scriptnamePicker.clear()
        
        self.ui.cmdlineCombo.addItem(cmdLine)
        self.ui.workdirPicker.addItem(workdir)
        self.ui.environmentCombo.addItem(environment)
        self.ui.scriptnamePicker.addItem("")
        self.ui.scriptnamePicker.setCurrentText(scriptName)
        
        if self.dialogType == 0:
            noDebugList = self.ui.multiprocessNoDebugCombo.currentText()
            self.ui.multiprocessNoDebugCombo.clear()
            self.ui.multiprocessNoDebugCombo.addItem(noDebugList)
    
    def __editHistory(self):
        """
        Private slot to edit a history list.
        """
        histories = [
            "",
            self.tr("Script Name"),
            self.tr("Script Parameters"),
            self.tr("Working Directory"),
            self.tr("Environment"),
        ]
        widgets = [
            None,
            self.ui.scriptnamePicker,
            self.ui.cmdlineCombo,
            self.ui.workdirPicker,
            self.ui.environmentCombo,
        ]
        if self.dialogType == 0:
            histories.append(self.tr("No Debug Programs"))
            widgets.append(self.ui.multiprocessNoDebugCombo)
        historyKind, ok = QInputDialog.getItem(
            self,
            self.tr("Edit History"),
            self.tr("Select the history list to be edited:"),
            histories,
            0, False)
        if ok and historyKind:
            history = []
            historiesIndex = histories.index(historyKind)
            if historiesIndex in (1, 3):
                picker = widgets[historiesIndex]
                history = picker.getPathItems()
            else:
                combo = widgets[historiesIndex]
                if combo:
                    history = [
                        combo.itemText(idx) for idx in range(combo.count())
                    ]
            
            if history:
                from .StartHistoryEditDialog import StartHistoryEditDialog
                dlg = StartHistoryEditDialog(history, self)
            if dlg.exec() == QDialog.DialogCode.Accepted:
                history = dlg.getHistory()
                combo = widgets[historiesIndex]
                if combo:
                    combo.clear()
                    combo.addItems(history)
                    
                    self.__historiesModified = True
    
    def historiesModified(self):
        """
        Public method to test for modified histories.
        
        @return flag indicating modified histories
        @rtype bool
        """
        return self.__historiesModified
    
    def clearHistories(self):
        """
        Public method to test, if histories shall be cleared.
        
        @return flag indicating histories shall be cleared
        @rtype bool
        """
        return self.__clearHistoryLists
    
    def getHistories(self):
        """
        Public method to get the lists of histories.
        
        @return tuple containing the histories of script names, command line
            arguments, working directories, environment settings and no debug
            programs lists
        @rtype tuple of five list of str
        """
        noDebugHistory = (
            [
                self.ui.multiprocessNoDebugCombo.itemText(index)
                for index in range(self.ui.multiprocessNoDebugCombo.count())
            ]
            if self.dialogType == 0 else
            None
        )
        return (
            self.ui.scriptnamePicker.getPathItems(),
            [self.ui.cmdlineCombo.itemText(index) for index in range(
                self.ui.cmdlineCombo.count())],
            self.ui.workdirPicker.getPathItems(),
            [self.ui.environmentCombo.itemText(index) for index in range(
                self.ui.environmentCombo.count())],
            noDebugHistory,
        )
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked
        @type QAbstractButton
        """
        if button == self.clearButton:
            self.__clearHistories()
        elif button == self.editButton:
            self.__editHistory()
