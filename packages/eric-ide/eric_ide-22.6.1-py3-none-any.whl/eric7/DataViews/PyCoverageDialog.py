# -*- coding: utf-8 -*-

# Copyright (c) 2003 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a Python code coverage dialog.
"""

import os
import time

from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QMenu, QHeaderView, QTreeWidgetItem,
    QApplication
)

from EricWidgets import EricMessageBox
from EricWidgets.EricApplication import ericApp

from .Ui_PyCoverageDialog import Ui_PyCoverageDialog

import Utilities
from coverage import Coverage
from coverage.misc import CoverageException


class PyCoverageDialog(QDialog, Ui_PyCoverageDialog):
    """
    Class implementing a dialog to display the collected code coverage data.
    
    @signal openFile(str) emitted to open the given file in an editor
    """
    openFile = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.summaryList.headerItem().setText(
            self.summaryList.columnCount(), "")
        self.resultList.headerItem().setText(self.resultList.columnCount(), "")
        
        self.cancelled = False
        self.path = '.'
        self.reload = False
        
        self.excludeList = ['# *pragma[: ]*[nN][oO] *[cC][oO][vV][eE][rR]']
        
        self.__reportsMenu = QMenu(self.tr("Create Report"), self)
        self.__reportsMenu.addAction(self.tr("HTML Report"), self.__htmlReport)
        self.__reportsMenu.addSeparator()
        self.__reportsMenu.addAction(self.tr("JSON Report"), self.__jsonReport)
        self.__reportsMenu.addAction(self.tr("LCOV Report"), self.__lcovReport)
        
        self.__menu = QMenu(self)
        self.__menu.addSeparator()
        self.openAct = self.__menu.addAction(
            self.tr("Open"), self.__openFile)
        self.__menu.addSeparator()
        self.__menu.addMenu(self.__reportsMenu)
        self.__menu.addSeparator()
        self.__menu.addAction(self.tr('Erase Coverage Info'), self.__erase)
        self.resultList.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.resultList.customContextMenuRequested.connect(
            self.__showContextMenu)
    
    def __format_lines(self, lines):
        """
        Private method to format a list of integers into string by coalescing
        groups.
        
        @param lines list of integers
        @type list of int
        @return string representing the list
        @rtype str
        """
        pairs = []
        lines.sort()
        maxValue = lines[-1]
        start = None
        
        i = lines[0]
        while i <= maxValue:
            try:
                if start is None:
                    start = i
                ind = lines.index(i)
                end = i
                i += 1
            except ValueError:
                pairs.append((start, end))
                start = None
                if ind + 1 >= len(lines):
                    break
                i = lines[ind + 1]
        if start:
            pairs.append((start, end))
        
        def stringify(pair):
            """
            Private helper function to generate a string representation of a
            pair.
            
            @param pair pair of integers
            @type tuple of (int, int
            @return representation of the pair
            @rtype str
            """
            start, end = pair
            if start == end:
                return "{0:d}".format(start)
            else:
                return "{0:d}-{1:d}".format(start, end)
        
        return ", ".join(map(stringify, pairs))
    
    def __createResultItem(self, file, statements, executed, coverage,
                           excluded, missing):
        """
        Private method to create an entry in the result list.
        
        @param file filename of file
        @type str
        @param statements number of statements
        @type int
        @param executed number of executed statements
        @type int
        @param coverage percent of coverage
        @type int
        @param excluded list of excluded lines
        @type str
        @param missing list of lines without coverage
        @type str
        """
        itm = QTreeWidgetItem(self.resultList, [
            file,
            str(statements),
            str(executed),
            "{0:.0f}%".format(coverage),
            excluded,
            missing
        ])
        for col in range(1, 4):
            itm.setTextAlignment(col, Qt.AlignmentFlag.AlignRight)
        if statements != executed:
            font = itm.font(0)
            font.setBold(True)
            for col in range(itm.columnCount()):
                itm.setFont(col, font)
    
    def start(self, cfn, fn):
        """
        Public slot to start the coverage data evaluation.
        
        @param cfn basename of the coverage file
        @type str
        @param fn file or list of files or directory to be checked
        @type str or list of str
        """
        # initialize the dialog
        self.resultList.clear()
        self.summaryList.clear()
        self.cancelled = False
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setDefault(True)
        
        self.__cfn = cfn
        self.__fn = fn
        
        self.cfn = (
            cfn
            if cfn.endswith(".coverage") else
            "{0}.coverage".format(os.path.splitext(cfn)[0])
        )
        
        if isinstance(fn, list):
            files = fn
            self.path = os.path.dirname(cfn)
        elif os.path.isdir(fn):
            files = Utilities.direntries(fn, True, '*.py', False)
            self.path = fn
        else:
            files = [fn]
            self.path = os.path.dirname(cfn)
        files.sort()
        
        cover = Coverage(data_file=self.cfn)
        cover.load()
        
        # set the exclude pattern
        self.excludeCombo.clear()
        self.excludeCombo.addItems(self.excludeList)
        
        self.checkProgress.setMaximum(len(files))
        QApplication.processEvents()
        
        total_statements = 0
        total_executed = 0
        total_exceptions = 0
        
        cover.exclude(self.excludeList[0])
        
        try:
            # disable updates of the list for speed
            self.resultList.setUpdatesEnabled(False)
            self.resultList.setSortingEnabled(False)
            
            # now go through all the files
            now = time.monotonic()
            for progress, file in enumerate(files, start=1):
                if self.cancelled:
                    return
                
                try:
                    statements, excluded, missing, readable = (
                        cover.analysis2(file)[1:])
                    readableEx = (excluded and self.__format_lines(excluded) or
                                  '')
                    n = len(statements)
                    m = n - len(missing)
                    pc = 100.0 * m / n if n > 0 else 100.0
                    self.__createResultItem(
                        file, str(n), str(m), pc, readableEx, readable)
                    
                    total_statements += n
                    total_executed += m
                except CoverageException:
                    total_exceptions += 1
                
                self.checkProgress.setValue(progress)
                if time.monotonic() - now > 0.01:
                    QApplication.processEvents()
                    now = time.monotonic()
        finally:
            # reenable updates of the list
            self.resultList.setSortingEnabled(True)
            self.resultList.setUpdatesEnabled(True)
            self.checkProgress.reset()
        
        # show summary info
        if len(files) > 1:
            if total_statements > 0:
                pc = 100.0 * total_executed / total_statements
            else:
                pc = 100.0
            itm = QTreeWidgetItem(self.summaryList, [
                str(total_statements),
                str(total_executed),
                "{0:.0f}%".format(pc)
            ])
            for col in range(0, 3):
                itm.setTextAlignment(col, Qt.AlignmentFlag.AlignRight)
        else:
            self.summaryGroup.hide()
        
        if total_exceptions:
            EricMessageBox.warning(
                self,
                self.tr("Parse Error"),
                self.tr("""%n file(s) could not be parsed. Coverage"""
                        """ info for these is not available.""", "",
                        total_exceptions))
        
        self.__finish()
    
    def __finish(self):
        """
        Private slot called when the action finished or the user pressed the
        button.
        """
        self.cancelled = True
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setEnabled(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel).setEnabled(False)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        QApplication.processEvents()
        self.resultList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.resultList.header().setStretchLastSection(True)
        self.summaryList.header().resizeSections(
            QHeaderView.ResizeMode.ResizeToContents)
        self.summaryList.header().setStretchLastSection(True)
    
    def on_buttonBox_clicked(self, button):
        """
        Private slot called by a button of the button box clicked.
        
        @param button button that was clicked
        @type QAbstractButton
        """
        if button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close
        ):
            self.close()
        elif button == self.buttonBox.button(
            QDialogButtonBox.StandardButton.Cancel
        ):
            self.__finish()
    
    def __showContextMenu(self, coord):
        """
        Private slot to show the context menu of the listview.
        
        @param coord position of the mouse pointer
        @type QPoint
        """
        itm = self.resultList.itemAt(coord)
        if itm:
            self.openAct.setEnabled(True)
        else:
            self.openAct.setEnabled(False)
        self.__reportsMenu.setEnabled(
            bool(self.resultList.topLevelItemCount()))
        self.__menu.popup(self.mapToGlobal(coord))
    
    def __openFile(self, itm=None):
        """
        Private slot to open the selected file.
        
        @param itm reference to the item to be opened
        @type QTreeWidgetItem
        """
        if itm is None:
            itm = self.resultList.currentItem()
        fn = itm.text(0)
        
        try:
            vm = ericApp().getObject("ViewManager")
            vm.openSourceFile(fn)
            editor = vm.getOpenEditor(fn)
            editor.codeCoverageShowAnnotations(coverageFile=self.cfn)
        except KeyError:
            self.openFile.emit(fn)
    
    def __prepareReportGeneration(self):
        """
        Private method to prepare a report generation.
        
        @return tuple containing a reference to the Coverage object and the
            list of files to report
        @rtype tuple of (Coverage, list of str)
        """
        count = self.resultList.topLevelItemCount()
        if count == 0:
            return None, []
        
        # get list of all filenames
        files = [
            self.resultList.topLevelItem(index).text(0)
            for index in range(count)
        ]
        
        cover = Coverage(data_file=self.cfn)
        cover.exclude(self.excludeList[0])
        cover.load()
        
        return cover, files
    
    @pyqtSlot()
    def __htmlReport(self):
        """
        Private slot to generate a HTML report of the shown data.
        """
        from .PyCoverageHtmlReportDialog import PyCoverageHtmlReportDialog
        
        dlg = PyCoverageHtmlReportDialog(os.path.dirname(self.cfn), self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            title, outputDirectory, extraCSS, openReport = dlg.getData()
            
            cover, files = self.__prepareReportGeneration()
            cover.html_report(morfs=files, directory=outputDirectory,
                              ignore_errors=True, extra_css=extraCSS,
                              title=title)
            
            if openReport:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.join(
                    outputDirectory, "index.html")))
    
    @pyqtSlot()
    def __jsonReport(self):
        """
        Private slot to generate a JSON report of the shown data.
        """
        from .PyCoverageJsonReportDialog import PyCoverageJsonReportDialog
        
        dlg = PyCoverageJsonReportDialog(os.path.dirname(self.cfn), self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            filename, compact = dlg.getData()
            cover, files = self.__prepareReportGeneration()
            cover.json_report(morfs=files, outfile=filename,
                              ignore_errors=True, pretty_print=not compact)
    
    @pyqtSlot()
    def __lcovReport(self):
        """
        Private slot to generate a LCOV report of the shown data.
        """
        from EricWidgets import EricPathPickerDialog
        from EricWidgets.EricPathPicker import EricPathPickerModes
        
        filename, ok = EricPathPickerDialog.getPath(
            self,
            self.tr("LCOV Report"),
            self.tr("Enter the path of the output file:"),
            mode=EricPathPickerModes.SAVE_FILE_ENSURE_EXTENSION_MODE,
            path=os.path.join(os.path.dirname(self.cfn), "coverage.lcov"),
            defaultDirectory=os.path.dirname(self.cfn),
            filters=self.tr("LCOV Files (*.lcov);;All Files (*)")
        )
        if ok:
            cover, files = self.__prepareReportGeneration()
            cover.lcov_report(morfs=files, outfile=filename,
                              ignore_errors=True)
    
    def __erase(self):
        """
        Private slot to handle the erase context menu action.
        
        This method erases the collected coverage data that is
        stored in the .coverage file.
        """
        cover = Coverage(data_file=self.cfn)
        cover.load()
        cover.erase()
        
        self.reloadButton.setEnabled(False)
        self.resultList.clear()
        self.summaryList.clear()
    
    @pyqtSlot()
    def on_reloadButton_clicked(self):
        """
        Private slot to reload the coverage info.
        """
        self.reload = True
        excludePattern = self.excludeCombo.currentText()
        if excludePattern in self.excludeList:
            self.excludeList.remove(excludePattern)
        self.excludeList.insert(0, excludePattern)
        self.start(self.__cfn, self.__fn)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_resultList_itemActivated(self, item, column):
        """
        Private slot to handle the activation of an item.
        
        @param item reference to the activated item (QTreeWidgetItem)
        @param column column the item was activated in (integer)
        """
        self.__openFile(item)
