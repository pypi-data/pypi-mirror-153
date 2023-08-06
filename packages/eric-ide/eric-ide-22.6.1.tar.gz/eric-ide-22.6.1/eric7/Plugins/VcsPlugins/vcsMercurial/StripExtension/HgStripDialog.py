# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data to strip changesets.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from .Ui_HgStripDialog import Ui_HgStripDialog


class HgStripDialog(QDialog, Ui_HgStripDialog):
    """
    Class implementing a dialog to enter the data to strip changesets.
    """
    def __init__(self, tagsList, branchesList, bookmarksList=None, rev="",
                 parent=None):
        """
        Constructor
        
        @param tagsList list of tags
        @type list of str
        @param branchesList list of branches
        @type list of str
        @param bookmarksList list of bookmarks
        @type list of str
        @param rev revision to strip from
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.tagCombo.addItems(sorted(tagsList))
        self.branchCombo.addItems(["default"] + sorted(branchesList))
        if bookmarksList is not None:
            self.bookmarkCombo.addItems([""] + sorted(bookmarksList))
        self.idEdit.setText(rev)
        
        # connect various radio buttons and input fields
        self.numberButton.toggled.connect(self.__updateOK)
        self.idButton.toggled.connect(self.__updateOK)
        self.tagButton.toggled.connect(self.__updateOK)
        self.branchButton.toggled.connect(self.__updateOK)
        self.expressionButton.toggled.connect(self.__updateOK)
        
        self.numberSpinBox.valueChanged.connect(self.__updateOK)
        
        self.idEdit.textChanged.connect(self.__updateOK)
        self.expressionEdit.textChanged.connect(self.__updateOK)
        
        self.tagCombo.editTextChanged.connect(self.__updateOK)
        self.branchCombo.editTextChanged.connect(self.__updateOK)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
        
        self.__updateOK()
        
        self.idEdit.setFocus()
    
    @pyqtSlot()
    def __updateOK(self):
        """
        Private slot to update the OK button.
        """
        enabled = True
        if self.numberButton.isChecked():
            enabled = enabled and self.numberSpinBox.value() >= 0
        elif self.idButton.isChecked():
            enabled = enabled and bool(self.idEdit.text())
        elif self.tagButton.isChecked():
            enabled = enabled and bool(self.tagCombo.currentText())
        elif self.branchButton.isChecked():
            enabled = enabled and bool(self.branchCombo.currentText())
        elif self.expressionButton.isChecked():
            enabled = enabled and bool(self.expressionEdit.text())
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enabled)
    
    def __getRevision(self):
        """
        Private method to generate the revision.
        
        @return revision
        @rtype str
        """
        if self.numberButton.isChecked():
            return "rev({0})".format(self.numberSpinBox.value())
        elif self.idButton.isChecked():
            return "id({0})".format(self.idEdit.text())
        elif self.tagButton.isChecked():
            return self.tagCombo.currentText()
        elif self.branchButton.isChecked():
            return self.branchCombo.currentText()
        elif self.expressionButton.isChecked():
            return self.expressionEdit.text()
        else:
            # should not happen
            return ""
    
    def getData(self):
        """
        Public method to retrieve the data for the strip action.
        
        @return tuple with the revision, a bookmark name, a flag indicating
            to enforce the strip action, a flag indicating to omit the creation
            of backup bundles and a flag indicating to not modify the working
            directory
        @rtype tuple (str, str, bool, bool, bool)
        """
        return (
            self.__getRevision(),
            self.bookmarkCombo.currentText(),
            self.forceCheckBox.isChecked(),
            self.noBackupCheckBox.isChecked(),
            self.keepCheckBox.isChecked(),
        )
