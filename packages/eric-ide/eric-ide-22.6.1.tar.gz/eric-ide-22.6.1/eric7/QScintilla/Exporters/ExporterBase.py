# -*- coding: utf-8 -*-

# Copyright (c) 2007 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the exporter base class.
"""

from PyQt6.QtCore import QFileInfo, QObject, QCoreApplication

from EricWidgets import EricMessageBox, EricFileDialog

import Utilities


class ExporterBase(QObject):
    """
    Class implementing the exporter base class.
    """
    def __init__(self, editor, parent=None):
        """
        Constructor
        
        @param editor reference to the editor object (QScintilla.Editor.Editor)
        @param parent parent object of the exporter (QObject)
        """
        super().__init__(parent)
        self.editor = editor
    
    def _getFileName(self, fileFilter):
        """
        Protected method to get the file name of the export file from the user.
        
        @param fileFilter the filter string to be used (string). The filter for
            "All Files (*)" is appended by this method.
        @return file name entered by the user (string)
        """
        fileFilter += ";;"
        fileFilter += QCoreApplication.translate('Exporter', "All Files (*)")
        fn, selectedFilter = EricFileDialog.getSaveFileNameAndFilter(
            self.editor,
            QCoreApplication.translate('Exporter', "Export source"),
            "",
            fileFilter,
            "",
            EricFileDialog.DontConfirmOverwrite)
        
        if fn:
            ext = QFileInfo(fn).suffix()
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fn += ex
            if QFileInfo(fn).exists():
                res = EricMessageBox.yesNo(
                    self.editor,
                    QCoreApplication.translate(
                        'Exporter', "Export source"),
                    QCoreApplication.translate(
                        'Exporter',
                        "<p>The file <b>{0}</b> already exists."
                        " Overwrite it?</p>").format(fn),
                    icon=EricMessageBox.Warning)
                if not res:
                    return ""
            
            fn = Utilities.toNativeSeparators(fn)
        
        return fn
    
    def exportSource(self):
        """
        Public method performing the export.
        
        This method must be overridden by the real exporters.
        
        @exception NotImplementedError raised to indicate that this method
            must be implemented by a subclass
        """
        raise NotImplementedError
