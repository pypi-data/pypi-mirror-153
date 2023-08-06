# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Translations Properties dialog.
"""

import os

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QListWidgetItem, QDialog, QDialogButtonBox

from EricWidgets.EricCompleters import EricFileCompleter
from EricWidgets import EricFileDialog
from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_TranslationPropertiesDialog import Ui_TranslationPropertiesDialog

import Utilities


class TranslationPropertiesDialog(QDialog, Ui_TranslationPropertiesDialog):
    """
    Class implementing the Translations Properties dialog.
    """
    def __init__(self, project, new, parent):
        """
        Constructor
        
        @param project reference to the project object
        @param new flag indicating the generation of a new project
        @param parent parent widget of this dialog (QWidget)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.transPatternPicker.setMode(EricPathPickerModes.SAVE_FILE_MODE)
        self.transPatternPicker.setDefaultDirectory(project.ppath)
        self.transBinPathPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.transBinPathPicker.setDefaultDirectory(project.ppath)
        
        self.project = project
        self.parent = parent
        
        self.exceptionCompleter = EricFileCompleter(self.exceptionEdit)
        
        self.initFilters()
        if not new:
            self.initDialog()
        
    def initFilters(self):
        """
        Public method to initialize the filters.
        """
        patterns = {
            "SOURCES": [],
            "FORMS": [],
        }
        for pattern, filetype in list(self.project.pdata["FILETYPES"].items()):
            if filetype in patterns:
                patterns[filetype].append(pattern)
        self.filters = self.tr("Source Files ({0});;"
                               ).format(" ".join(patterns["SOURCES"]))
        self.filters += self.tr("Forms Files ({0});;"
                                ).format(" ".join(patterns["FORMS"]))
        self.filters += self.tr("All Files (*)")
        
    def initDialog(self):
        """
        Public method to initialize the dialogs data.
        """
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.transPatternPicker.setText(
            self.project.pdata["TRANSLATIONPATTERN"])
        self.transBinPathPicker.setText(
            self.project.pdata["TRANSLATIONSBINPATH"])
        self.exceptionsList.clear()
        for texcept in self.project.pdata["TRANSLATIONEXCEPTIONS"]:
            if texcept:
                self.exceptionsList.addItem(texcept)
        
    @pyqtSlot(str)
    def on_transPatternPicker_pathSelected(self, path):
        """
        Private slot handling the selection of a translation path.
        
        @param path selected path
        @type str
        """
        self.transPatternPicker.setText(self.project.getRelativePath(path))
        
    @pyqtSlot(str)
    def on_transPatternPicker_textChanged(self, txt):
        """
        Private slot to check the translation pattern for correctness.
        
        @param txt text of the transPatternPicker line edit (string)
        """
        self.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            "%language%" in txt)
        
    @pyqtSlot(str)
    def on_transBinPathPicker_pathSelected(self, path):
        """
        Private slot handling the selection of a binary translations path.
        
        @param path selected path
        @type str
        """
        self.transBinPathPicker.setText(self.project.getRelativePath(path))
        
    @pyqtSlot()
    def on_deleteExceptionButton_clicked(self):
        """
        Private slot to delete the currently selected entry of the listwidget.
        """
        row = self.exceptionsList.currentRow()
        itm = self.exceptionsList.takeItem(row)
        del itm
        row = self.exceptionsList.currentRow()
        self.on_exceptionsList_currentRowChanged(row)
        
    @pyqtSlot()
    def on_addExceptionButton_clicked(self):
        """
        Private slot to add the shown exception to the listwidget.
        """
        texcept = self.exceptionEdit.text()
        texcept = (
            texcept.replace(self.parent.getPPath() + os.sep, "")
            if self.project.ppath == '' else
            self.project.getRelativePath(texcept)
        )
        if texcept.endswith(os.sep):
            texcept = texcept[:-1]
        if texcept:
            QListWidgetItem(texcept, self.exceptionsList)
            self.exceptionEdit.clear()
        row = self.exceptionsList.currentRow()
        self.on_exceptionsList_currentRowChanged(row)
        
    @pyqtSlot()
    def on_exceptFileButton_clicked(self):
        """
        Private slot to select a file to exempt from translation.
        """
        texcept = EricFileDialog.getOpenFileName(
            self,
            self.tr("Exempt file from translation"),
            self.project.ppath,
            self.filters)
        if texcept:
            self.exceptionEdit.setText(Utilities.toNativeSeparators(texcept))
        
    @pyqtSlot()
    def on_exceptDirButton_clicked(self):
        """
        Private slot to select a file to exempt from translation.
        """
        texcept = EricFileDialog.getExistingDirectory(
            self,
            self.tr("Exempt directory from translation"),
            self.project.ppath,
            EricFileDialog.ShowDirsOnly)
        if texcept:
            self.exceptionEdit.setText(Utilities.toNativeSeparators(texcept))
        
    def on_exceptionsList_currentRowChanged(self, row):
        """
        Private slot to handle the currentRowChanged signal of the exceptions
        list.
        
        @param row the current row (integer)
        """
        if row == -1:
            self.deleteExceptionButton.setEnabled(False)
        else:
            self.deleteExceptionButton.setEnabled(True)
        
    def on_exceptionEdit_textChanged(self, txt):
        """
        Private slot to handle the textChanged signal of the exception edit.
        
        @param txt the text of the exception edit (string)
        """
        self.addExceptionButton.setEnabled(txt != "")
        
    def storeData(self):
        """
        Public method to store the entered/modified data.
        """
        tp = self.transPatternPicker.text()
        if tp:
            tp = self.project.getRelativePath(tp)
            self.project.pdata["TRANSLATIONPATTERN"] = tp
            self.project.translationsRoot = tp.split("%language%")[0]
        else:
            self.project.pdata["TRANSLATIONPATTERN"] = ""
        tp = self.transBinPathPicker.text()
        if tp:
            tp = self.project.getRelativePath(tp)
            self.project.pdata["TRANSLATIONSBINPATH"] = tp
        else:
            self.project.pdata["TRANSLATIONSBINPATH"] = ""
        exceptList = []
        for i in range(self.exceptionsList.count()):
            exceptList.append(self.exceptionsList.item(i).text())
        self.project.pdata["TRANSLATIONEXCEPTIONS"] = exceptList[:]
