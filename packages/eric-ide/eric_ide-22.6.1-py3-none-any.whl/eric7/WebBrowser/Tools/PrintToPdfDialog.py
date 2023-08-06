# -*- coding: utf-8 -*-

# Copyright (c) 2016 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to enter the data for printing a web page to PDF.
"""

import os

from PyQt6.QtCore import pyqtSlot, QMarginsF, QStandardPaths
from PyQt6.QtGui import QPageLayout, QPageSize
from PyQt6.QtPrintSupport import QPrinter, QPageSetupDialog
from PyQt6.QtWidgets import QDialog

from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_PrintToPdfDialog import Ui_PrintToPdfDialog


class PrintToPdfDialog(QDialog, Ui_PrintToPdfDialog):
    """
    Class implementing a dialog to enter the data for printing a web page to
    PDF.
    """
    def __init__(self, filePath, parent=None):
        """
        Constructor
        
        @param filePath path of the file to write into
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.pdfFilePicker.setMode(
            EricPathPickerModes.SAVE_FILE_OVERWRITE_MODE)
        self.pdfFilePicker.setFilters(self.tr(
            "PDF Files (*.pdf);;"
            "All Files (*)"))
        if not os.path.isabs(filePath):
            documentsPath = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation)
            if documentsPath:
                filePath = os.path.join(documentsPath, filePath)
            else:
                filePath = os.path.abspath(filePath)
        self.pdfFilePicker.setText(filePath, toNative=True)
        
        self.__currentPageLayout = QPageLayout(
            QPageSize(QPageSize.PageSizeId.A4),
            QPageLayout.Orientation.Portrait,
            QMarginsF(0.0, 0.0, 0.0, 0.0))
        
        self.__updatePageLayoutLabel()
    
    @pyqtSlot()
    def on_pageLayoutButton_clicked(self):
        """
        Private slot to define the page layout.
        """
        printer = QPrinter()
        printer.setPageLayout(self.__currentPageLayout)
        
        dlg = QPageSetupDialog(printer, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.__currentPageLayout = printer.pageLayout()
            self.__updatePageLayoutLabel()
    
    def __updatePageLayoutLabel(self):
        """
        Private method to update the page layout label.
        """
        orientation = (
            self.tr("Portrait")
            if (self.__currentPageLayout.orientation() ==
                QPageLayout.Orientation.Portrait) else
            self.tr("Landscape")
        )
        self.pageLayoutLabel.setText(
            self.tr("{0}, {1}", "page size, page orientation").format(
                self.__currentPageLayout.pageSize().name(),
                orientation))
    
    def getData(self):
        """
        Public method to get the dialog data.
        
        @return tuple containing the file path and the page layout
        @rtype tuple of str and QPageLayout
        """
        return (
            self.pdfFilePicker.text(toNative=True),
            self.__currentPageLayout,
        )
