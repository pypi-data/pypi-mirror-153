# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select from a list of strings.
"""

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QAbstractItemView, QListWidgetItem
)

from .Ui_EricListSelectionDialog import Ui_EricListSelectionDialog


class EricListSelectionDialog(QDialog, Ui_EricListSelectionDialog):
    """
    Class implementing a dialog to select from a list of strings.
    """
    def __init__(self, entries,
                 selectionMode=QAbstractItemView.SelectionMode
                 .ExtendedSelection,
                 title="", message="", checkBoxSelection=False,
                 doubleClickOk=False, parent=None):
        """
        Constructor
        
        @param entries list of entries to select from
        @type list of str
        @param selectionMode selection mode for the list
        @type QAbstractItemView.SelectionMode
        @param title title of the dialog
        @type str
        @param message message to be show in the dialog
        @type str
        @param checkBoxSelection flag indicating to select items via their
            checkbox
        @type bool
        @param doubleClickOk flag indicating to accept the dialog upon a
            double click of an item (single selection only)
        @type bool
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        if title:
            self.setWindowTitle(title)
        if message:
            self.messageLabel.setText(message)
        
        self.__checkCount = 0
        self.__isCheckBoxSelection = checkBoxSelection
        if self.__isCheckBoxSelection:
            self.selectionList.setSelectionMode(
                QAbstractItemView.SelectionMode.NoSelection)
            for entry in entries:
                itm = QListWidgetItem(entry)
                itm.setFlags(Qt.ItemFlag.ItemIsUserCheckable |
                             Qt.ItemFlag.ItemIsEnabled)
                itm.setCheckState(Qt.CheckState.Unchecked)
                self.selectionList.addItem(itm)
        else:
            self.selectionList.setSelectionMode(selectionMode)
            self.selectionList.addItems(entries)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
    
    @pyqtSlot()
    def on_selectionList_itemSelectionChanged(self):
        """
        Private slot handling a change of the selection.
        """
        if not self.__isCheckBoxSelection:
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Ok).setEnabled(
                    len(self.selectionList.selectedItems()) > 0)
    
    def on_selectionList_itemChanged(self, itm):
        """
        Private slot handling a change of an item.
        
        @param itm reference to the changed item
        @type QListWidgetItem
        """
        if self.__isCheckBoxSelection:
            if itm.checkState() == Qt.CheckState.Checked:
                self.__checkCount += 1
            else:
                self.__checkCount -= 1
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Ok).setEnabled(
                self.__checkCount > 0)
    
    @pyqtSlot(QListWidgetItem)
    def on_selectionList_itemDoubleClicked(self, item):
        """
        Private slot handling double clicking an item.
        
        @param item double clicked item
        @type QListWidgetItem
        """
        if (
            not self.__isCheckBoxSelection and
            self.selectionList.selectionMode() ==
            QAbstractItemView.SelectionMode.SingleSelection
        ):
            self.accept()
    
    def getSelection(self):
        """
        Public method to retrieve the selected items.
        
        @return selected entries
        @rtype list of str
        """
        entries = []
        if self.__isCheckBoxSelection:
            for row in range(self.selectionList.count()):
                item = self.selectionList.item(row)
                if item.checkState() == Qt.CheckState.Checked:
                    entries.append(item.text())
        else:
            for item in self.selectionList.selectedItems():
                entries.append(item.text())
        return entries
