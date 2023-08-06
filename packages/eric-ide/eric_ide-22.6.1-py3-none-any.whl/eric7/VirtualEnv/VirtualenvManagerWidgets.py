# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to manage the list of defined virtual
environments.
"""

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import (
    QWidget, QDialog, QDialogButtonBox, QTreeWidgetItem, QHeaderView,
    QVBoxLayout
)

from EricWidgets.EricPathPicker import EricPathPickerModes
from EricWidgets.EricMainWindow import EricMainWindow

from .Ui_VirtualenvManagerWidget import Ui_VirtualenvManagerWidget

import Utilities
import UI.PixmapCache


class VirtualenvManagerWidget(QWidget, Ui_VirtualenvManagerWidget):
    """
    Class implementing a widget to manage the list of defined virtual
    environments.
    """
    IsGlobalRole = Qt.ItemDataRole.UserRole + 1
    IsCondaRole = Qt.ItemDataRole.UserRole + 2
    IsRemoteRole = Qt.ItemDataRole.UserRole + 3
    ExecPathRole = Qt.ItemDataRole.UserRole + 4
    
    def __init__(self, manager, parent=None):
        """
        Constructor
        
        @param manager reference to the virtual environment manager
        @type VirtualenvManager
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__manager = manager
        
        self.addButton.setIcon(UI.PixmapCache.getIcon("plus"))
        self.newButton.setIcon(UI.PixmapCache.getIcon("new"))
        self.editButton.setIcon(UI.PixmapCache.getIcon("edit"))
        self.removeButton.setIcon(UI.PixmapCache.getIcon("minus"))
        self.removeAllButton.setIcon(UI.PixmapCache.getIcon("minus_3"))
        self.deleteButton.setIcon(UI.PixmapCache.getIcon("fileDelete"))
        self.deleteAllButton.setIcon(UI.PixmapCache.getIcon("fileDeleteList"))
        self.saveButton.setIcon(UI.PixmapCache.getIcon("fileSave"))
        
        baseDir = self.__manager.getVirtualEnvironmentsBaseDir()
        if not baseDir:
            baseDir = Utilities.getHomeDir()
        
        self.envBaseDirectoryPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.envBaseDirectoryPicker.setWindowTitle(
            self.tr("Virtualenv Base Directory"))
        self.envBaseDirectoryPicker.setText(baseDir)
        
        self.__populateVenvList()
        self.__updateButtons()
        
        self.venvList.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        
        self.__manager.virtualEnvironmentsListChanged.connect(self.__refresh)
    
    def __updateButtons(self):
        """
        Private method to update the enabled state of the various buttons.
        """
        selectedItemsCount = len(self.venvList.selectedItems())
        topLevelItemCount = self.venvList.topLevelItemCount()
        
        deletableSelectedItemCount = 0
        for itm in self.venvList.selectedItems():
            if (
                itm.text(0) != "<default>" and
                bool(itm.text(1)) and
                not itm.data(0, VirtualenvManagerWidget.IsGlobalRole) and
                not itm.data(0, VirtualenvManagerWidget.IsRemoteRole)
            ):
                deletableSelectedItemCount += 1
        
        deletableItemCount = 0
        for index in range(topLevelItemCount):
            itm = self.venvList.topLevelItem(index)
            if (
                itm.text(0) != "<default>" and
                bool(itm.text(1)) and
                not itm.data(0, VirtualenvManagerWidget.IsRemoteRole)
            ):
                deletableItemCount += 1
        
        canBeRemoved = (
            selectedItemsCount == 1 and
            self.venvList.selectedItems()[0].text(0) != "<default>"
        )
        canAllBeRemoved = (
            topLevelItemCount == 1 and
            self.venvList.topLevelItem(0).text(0) != "<default>"
        )
        
        self.editButton.setEnabled(selectedItemsCount == 1)
        
        self.removeButton.setEnabled(selectedItemsCount > 1 or canBeRemoved)
        self.removeAllButton.setEnabled(
            topLevelItemCount > 1 or canAllBeRemoved)
        
        self.deleteButton.setEnabled(deletableSelectedItemCount)
        self.deleteAllButton.setEnabled(deletableItemCount)
    
    @pyqtSlot()
    def on_addButton_clicked(self):
        """
        Private slot to add a new entry.
        """
        from .VirtualenvAddEditDialog import VirtualenvAddEditDialog
        dlg = VirtualenvAddEditDialog(
            self.__manager,
            baseDir=self.envBaseDirectoryPicker.text()
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (venvName, venvDirectory, venvInterpreter, isGlobal, isConda,
             isRemote, execPath) = dlg.getData()
            
            self.__manager.addVirtualEnv(
                venvName, venvDirectory, venvInterpreter, isGlobal, isConda,
                isRemote, execPath)
    
    @pyqtSlot()
    def on_newButton_clicked(self):
        """
        Private slot to create a new virtual environment.
        """
        self.__manager.createVirtualEnv(
            baseDir=self.envBaseDirectoryPicker.text())
    
    @pyqtSlot()
    def on_editButton_clicked(self):
        """
        Private slot to edit the selected entry.
        """
        selectedItem = self.venvList.selectedItems()[0]
        oldVenvName = selectedItem.text(0)
        
        from .VirtualenvAddEditDialog import VirtualenvAddEditDialog
        dlg = VirtualenvAddEditDialog(
            self.__manager, selectedItem.text(0),
            selectedItem.text(1), selectedItem.text(2),
            selectedItem.data(0, VirtualenvManagerWidget.IsGlobalRole),
            selectedItem.data(0, VirtualenvManagerWidget.IsCondaRole),
            selectedItem.data(0, VirtualenvManagerWidget.IsRemoteRole),
            selectedItem.data(0, VirtualenvManagerWidget.ExecPathRole),
            baseDir=self.envBaseDirectoryPicker.text()
        )
        if dlg.exec() == QDialog.DialogCode.Accepted:
            (venvName, venvDirectory, venvInterpreter, isGlobal, isConda,
             isRemote, execPath) = dlg.getData()
            if venvName != oldVenvName:
                self.__manager.renameVirtualEnv(
                    oldVenvName, venvName, venvDirectory, venvInterpreter,
                    isGlobal, isConda, isRemote, execPath)
            else:
                self.__manager.setVirtualEnv(
                    venvName, venvDirectory, venvInterpreter, isGlobal,
                    isConda, isRemote, execPath)
    
    @pyqtSlot()
    def on_removeButton_clicked(self):
        """
        Private slot to remove all selected entries from the list but keep
        their directories.
        """
        selectedVenvs = []
        for itm in self.venvList.selectedItems():
            selectedVenvs.append(itm.text(0))
        
        if selectedVenvs:
            self.__manager.removeVirtualEnvs(selectedVenvs)
    
    @pyqtSlot()
    def on_removeAllButton_clicked(self):
        """
        Private slot to remove all entries from the list but keep their
        directories.
        """
        venvNames = []
        for index in range(self.venvList.topLevelItemCount()):
            itm = self.venvList.topLevelItem(index)
            venvNames.append(itm.text(0))
        
        if venvNames:
            self.__manager.removeVirtualEnvs(venvNames)
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        """
        Private slot to delete all selected entries from the list and disk.
        """
        selectedVenvs = []
        for itm in self.venvList.selectedItems():
            selectedVenvs.append(itm.text(0))
        
        if selectedVenvs:
            self.__manager.deleteVirtualEnvs(selectedVenvs)
    
    @pyqtSlot()
    def on_deleteAllButton_clicked(self):
        """
        Private slot to delete all entries from the list and disk.
        """
        venvNames = []
        for index in range(self.venvList.topLevelItemCount()):
            itm = self.venvList.topLevelItem(index)
            venvNames.append(itm.text(0))
        
        if venvNames:
            self.__manager.deleteVirtualEnvs(venvNames)
    
    @pyqtSlot()
    def on_venvList_itemSelectionChanged(self):
        """
        Private slot handling a change of the selected items.
        """
        self.__updateButtons()
    
    @pyqtSlot()
    def __refresh(self):
        """
        Private slot to refresh the list of shown items.
        """
        # 1. remember selected entries
        selectedVenvs = []
        for itm in self.venvList.selectedItems():
            selectedVenvs.append(itm.text(0))
        
        # 2. clear the list
        self.venvList.clear()
        
        # 3. re-populate the list
        self.__populateVenvList()
        
        # 4. re-establish selection
        for venvName in selectedVenvs:
            itms = self.venvList.findItems(
                venvName, Qt.MatchFlag.MatchExactly, 0)
            if itms:
                itms[0].setSelected(True)
    
    def __populateVenvList(self):
        """
        Private method to populate the list of virtual environments.
        """
        environments = self.__manager.getEnvironmentEntries()
        for venvName in environments:
            itm = QTreeWidgetItem(self.venvList, [
                venvName,
                environments[venvName]["path"],
                environments[venvName]["interpreter"],
            ])
            itm.setData(0, VirtualenvManagerWidget.IsGlobalRole,
                        environments[venvName]["is_global"])
            itm.setData(0, VirtualenvManagerWidget.IsCondaRole,
                        environments[venvName]["is_conda"])
            itm.setData(0, VirtualenvManagerWidget.IsRemoteRole,
                        environments[venvName]["is_remote"])
            itm.setData(0, VirtualenvManagerWidget.ExecPathRole,
                        environments[venvName]["exec_path"])
            
            # show remote environments with underlined font
            if environments[venvName]["is_remote"]:
                font = itm.font(0)
                font.setUnderline(True)
                for column in range(itm.columnCount()):
                    itm.setFont(column, font)
            else:
                # local environments
                
                # show global environments with bold font
                if environments[venvName]["is_global"]:
                    font = itm.font(0)
                    font.setBold(True)
                    for column in range(itm.columnCount()):
                        itm.setFont(column, font)
                
                # show Anaconda environments with italic font
                if environments[venvName]["is_conda"]:
                    font = itm.font(0)
                    font.setItalic(True)
                    for column in range(itm.columnCount()):
                        itm.setFont(column, font)
        
        self.__resizeSections()
    
    def __resizeSections(self):
        """
        Private method to resize the sections of the environment list to their
        contents.
        """
        self.venvList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.venvList.header().setStretchLastSection(True)
    
    @pyqtSlot()
    def on_saveButton_clicked(self):
        """
        Private slot to save the base directory name.
        """
        baseDir = self.envBaseDirectoryPicker.text()
        self.__manager.setVirtualEnvironmentsBaseDir(baseDir)


class VirtualenvManagerDialog(QDialog):
    """
    Class implementing the virtual environments manager dialog variant.
    """
    def __init__(self, manager, parent=None):
        """
        Constructor
        
        @param manager reference to the virtual environment manager
        @type VirtualenvManager
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setSizeGripEnabled(True)
        
        self.__layout = QVBoxLayout(self)
        self.setLayout(self.__layout)
        
        self.cw = VirtualenvManagerWidget(manager, self)
        self.__layout.addWidget(self.cw)
        
        self.buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            Qt.Orientation.Horizontal,
            self)
        self.__layout.addWidget(self.buttonBox)
        
        self.resize(700, 500)
        self.setWindowTitle(self.tr("Manage Virtual Environments"))
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)


class VirtualenvManagerWindow(EricMainWindow):
    """
    Main window class for the standalone virtual environments manager.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget (QWidget)
        """
        super().__init__(parent)
        
        from VirtualEnv.VirtualenvManager import VirtualenvManager
        self.__virtualenvManager = VirtualenvManager(self)
        
        self.__centralWidget = QWidget(self)
        self.__layout = QVBoxLayout(self.__centralWidget)
        self.__centralWidget.setLayout(self.__layout)
        
        self.__virtualenvManagerWidget = VirtualenvManagerWidget(
            self.__virtualenvManager, self.__centralWidget)
        self.__layout.addWidget(self.__virtualenvManagerWidget)
        
        self.__buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            Qt.Orientation.Horizontal,
            self)
        self.__layout.addWidget(self.__buttonBox)
        
        self.setCentralWidget(self.__centralWidget)
        self.resize(700, 500)
        self.setWindowTitle(self.tr("Manage Virtual Environments"))
        
        self.__buttonBox.accepted.connect(self.close)
        self.__buttonBox.rejected.connect(self.close)
