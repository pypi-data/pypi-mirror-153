# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the commit message.
"""

from PyQt6.QtCore import pyqtSignal, Qt, pyqtSlot
from PyQt6.QtWidgets import QWidget, QDialogButtonBox

from EricWidgets.EricApplication import ericApp

from .Ui_SvnCommitDialog import Ui_SvnCommitDialog


class SvnCommitDialog(QWidget, Ui_SvnCommitDialog):
    """
    Class implementing a dialog to enter the commit message.
    
    @signal accepted() emitted, if the dialog was accepted
    @signal rejected() emitted, if the dialog was rejected
    """
    accepted = pyqtSignal()
    rejected = pyqtSignal()
    
    def __init__(self, vcs, parent=None):
        """
        Constructor
        
        @param vcs reference to the vcs object
        @param parent parent widget (QWidget)
        """
        super().__init__(parent, Qt.WindowType.Window)
        self.setupUi(self)
        
        self.__vcs = vcs
        
        project = ericApp().getObject("Project")
        pwl, pel = project.getProjectDictionaries()
        language = project.getProjectSpellLanguage()
        self.logEdit.setLanguageWithPWL(language, pwl or None, pel or None)
        
        if vcs.version < (1, 5, 0):
            self.changeListsGroup.hide()
        else:
            self.changeLists.addItems(sorted(vcs.svnGetChangelists()))
        
    def showEvent(self, evt):
        """
        Protected method called when the dialog is about to be shown.
        
        @param evt the event (QShowEvent)
        """
        commitMessages = self.__vcs.vcsCommitMessages()
        self.recentComboBox.clear()
        self.recentComboBox.addItem("")
        self.recentComboBox.addItems(commitMessages)
        
        self.logEdit.setFocus(Qt.FocusReason.OtherFocusReason)
        
    def logMessage(self):
        """
        Public method to retrieve the log message.
        
        @return the log message (string)
        """
        msg = self.logEdit.toPlainText()
        if msg:
            self.__vcs.vcsAddCommitMessage(msg)
        return msg
        
    def hasChangelists(self):
        """
        Public method to check, if the user entered some changelists.
        
        @return flag indicating availability of changelists (boolean)
        """
        return len(self.changeLists.selectedItems()) > 0
        
    def changelistsData(self):
        """
        Public method to retrieve the changelists data.
        
        @return tuple containing the changelists (list of strings) and a flag
            indicating to keep changelists (boolean)
        """
        slists = [line.text().strip()
                  for line in self.changeLists.selectedItems()
                  if line.text().strip() != ""]
        
        if len(slists) == 0:
            return [], False
        
        return slists, self.keepChangeListsCheckBox.isChecked()
        
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked (QAbstractButton)
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.logEdit.clear()
        
    def on_buttonBox_accepted(self):
        """
        Private slot called by the buttonBox accepted signal.
        """
        self.close()
        self.accepted.emit()
        
    def on_buttonBox_rejected(self):
        """
        Private slot called by the buttonBox rejected signal.
        """
        self.close()
        self.rejected.emit()
    
    @pyqtSlot(int)
    def on_recentComboBox_activated(self, index):
        """
        Private slot to select a commit message from recent ones.
        
        @param index index of the selected entry
        @type int
        """
        txt = self.recentComboBox.itemText(index)
        if txt:
            self.logEdit.setPlainText(txt)
