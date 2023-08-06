# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to search for text in files.
"""

import os
import re
import time

from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QPoint, QUrl
from PyQt6.QtGui import QCursor, QDesktopServices, QImageReader
from PyQt6.QtWidgets import (
    QWidget, QApplication, QMenu, QTreeWidgetItem, QComboBox, QDialog,
    QDialogButtonBox, QVBoxLayout
)

from EricWidgets.EricApplication import ericApp
from EricWidgets import EricMessageBox
from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_FindFileWidget import Ui_FindFileWidget

import Preferences
import UI.PixmapCache
import Utilities


class FindFileWidget(QWidget, Ui_FindFileWidget):
    """
    Class implementing a widget to search for text in files and replace it
    with some other text.
    
    The occurrences found are displayed in a tree showing the file name,
    the line number and the text found. The file will be opened upon a double
    click onto the respective entry of the list. If the widget is in replace
    mode the line below shows the text after replacement. Replacements can
    be authorized by ticking them on. Pressing the replace button performs
    all ticked replacement operations.
    
    @signal sourceFile(str, int, str, int, int) emitted to open a source file
        at a specificline
    @signal designerFile(str) emitted to open a Qt-Designer file
    @signal linguistFile(str) emitted to open a Qt-Linguist (*.ts) file
    @signal trpreview([str]) emitted to preview Qt-Linguist (*.qm) files
    @signal pixmapFile(str) emitted to open a pixmap file
    @signal svgFile(str) emitted to open a SVG file
    @signal umlFile(str) emitted to open an eric UML file
    """
    sourceFile = pyqtSignal(str, int, str, int, int)
    designerFile = pyqtSignal(str)
    linguistFile = pyqtSignal(str)
    trpreview = pyqtSignal(list)
    pixmapFile = pyqtSignal(str)
    svgFile = pyqtSignal(str)
    umlFile = pyqtSignal(str)
    
    lineRole = Qt.ItemDataRole.UserRole + 1
    startRole = Qt.ItemDataRole.UserRole + 2
    endRole = Qt.ItemDataRole.UserRole + 3
    replaceRole = Qt.ItemDataRole.UserRole + 4
    md5Role = Qt.ItemDataRole.UserRole + 5
    
    def __init__(self, project, parent=None):
        """
        Constructor
        
        @param project reference to the project object
        @type Project
        @param parent parent widget of this dialog (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.layout().setContentsMargins(0, 3, 0, 0)
        
        self.caseToolButton.setIcon(UI.PixmapCache.getIcon("caseSensitive"))
        self.wordToolButton.setIcon(UI.PixmapCache.getIcon("wholeWord"))
        self.regexpToolButton.setIcon(UI.PixmapCache.getIcon("regexp"))
        
        self.dirPicker.setMode(EricPathPickerModes.DIRECTORY_MODE)
        self.dirPicker.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        self.dirPicker.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon)
        
        self.stopButton.setEnabled(False)
        self.stopButton.clicked.connect(self.__stopSearch)
        self.stopButton.setIcon(UI.PixmapCache.getIcon("stopLoading"))
        self.stopButton.setAutoDefault(False)
        
        self.findButton.setEnabled(False)
        self.findButton.clicked.connect(self.__doSearch)
        self.findButton.setIcon(UI.PixmapCache.getIcon("find"))
        self.findButton.setAutoDefault(False)
        
        self.clearButton.setEnabled(False)
        self.clearButton.clicked.connect(self.__clearResults)
        self.clearButton.setIcon(UI.PixmapCache.getIcon("clear"))
        self.clearButton.setAutoDefault(False)
        
        self.replaceButton.setIcon(UI.PixmapCache.getIcon("editReplace"))
        self.replaceButton.setAutoDefault(False)
        
        self.modeToggleButton.clicked.connect(self.__toggleReplaceMode)
        
        self.findProgressLabel.setMaximumWidth(550)
        
        self.searchHistory = Preferences.toList(
            Preferences.getSettings().value(
                "FindFileWidget/SearchHistory"))
        self.findtextCombo.lineEdit().setClearButtonEnabled(True)
        self.findtextCombo.lineEdit().returnPressed.connect(self.__doSearch)
        self.findtextCombo.setCompleter(None)
        self.findtextCombo.addItems(self.searchHistory)
        self.findtextCombo.setEditText("")
        
        self.replaceHistory = Preferences.toList(
            Preferences.getSettings().value(
                "FindFileWidget/ReplaceHistory"))
        self.replacetextCombo.lineEdit().setClearButtonEnabled(True)
        self.replacetextCombo.lineEdit().returnPressed.connect(self.__doSearch)
        self.replacetextCombo.setCompleter(None)
        self.replacetextCombo.addItems(self.replaceHistory)
        self.replacetextCombo.setEditText("")
        
        self.dirHistory = Preferences.toList(
            Preferences.getSettings().value(
                "FindFileWidget/DirectoryHistory"))
        self.dirPicker.addItems(self.dirHistory)
        self.dirPicker.setText("")
        
        self.excludeHiddenCheckBox.setChecked(Preferences.toBool(
            Preferences.getSettings().value(
                "FindFileWidget/ExcludeHidden", True)
        ))
        
        # ensure the file type tab is the current one
        self.fileOptionsWidget.setCurrentWidget(self.fileTypeTab)
        
        self.project = project
        self.project.projectOpened.connect(self.__projectOpened)
        self.project.projectClosed.connect(self.__projectClosed)
        
        self.__standardListFont = self.findList.font()
        self.findList.headerItem().setText(self.findList.columnCount(), "")
        self.findList.header().setSortIndicator(0, Qt.SortOrder.AscendingOrder)
        self.__section0Size = self.findList.header().sectionSize(0)
        self.findList.setExpandsOnDoubleClick(False)

        # Qt Designer form files
        self.filterForms = r'.*\.ui$'
        self.formsExt = ['*.ui']
        
        # Corba interface files
        self.filterInterfaces = r'.*\.idl$'
        self.interfacesExt = ['*.idl']
        
        # Protobuf protocol files
        self.filterProtocols = r'.*\.proto$'
        self.protocolsExt = ['*.proto']
        
        # Qt resources files
        self.filterResources = r'.*\.qrc$'
        self.resourcesExt = ['*.qrc']
        
        self.__cancelSearch = False
        self.__lastFileItem = None
        self.__populating = False
        
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenuRequested)
        
        self.__replaceMode = True
        self.__toggleReplaceMode()
    
    def __createItem(self, file, line, text, start, end, replTxt="", md5=""):
        """
        Private method to create an entry in the file list.
        
        @param file filename of file
        @type str
        @param line line number
        @type int
        @param text text found
        @type str
        @param start start position of match
        @type int
        @param end end position of match
        @type int
        @param replTxt text with replacements applied (defaults to "")
        @type str (optional)
        @param md5 MD5 hash of the file (defaults to "")
        @type str (optional)
        """
        if self.__lastFileItem is None:
            # It's a new file
            self.__lastFileItem = QTreeWidgetItem(self.findList, [file])
            self.__lastFileItem.setFirstColumnSpanned(True)
            self.__lastFileItem.setExpanded(True)
            if self.__replaceMode:
                self.__lastFileItem.setFlags(
                    self.__lastFileItem.flags() |
                    Qt.ItemFlag.ItemIsUserCheckable |
                    Qt.ItemFlag.ItemIsAutoTristate)
            self.__lastFileItem.setData(0, self.md5Role, md5)
        
        itm = QTreeWidgetItem(self.__lastFileItem)
        itm.setTextAlignment(0, Qt.AlignmentFlag.AlignRight)
        itm.setData(0, Qt.ItemDataRole.DisplayRole, line)
        itm.setData(1, Qt.ItemDataRole.DisplayRole, text)
        itm.setData(0, self.lineRole, line)
        itm.setData(0, self.startRole, start)
        itm.setData(0, self.endRole, end)
        itm.setData(0, self.replaceRole, replTxt)
        if self.__replaceMode:
            itm.setFlags(itm.flags() |
                         Qt.ItemFlag.ItemIsUserCheckable)
            itm.setCheckState(0, Qt.CheckState.Checked)
            self.replaceButton.setEnabled(True)
    
    def activate(self, replaceMode=False, txt="", searchDir="",
                 openFiles=False):
        """
        Public method to activate the widget with a given mode, a text
        to search for and some search parameters.
        
        @param replaceMode flag indicating replacement mode (defaults to False)
        @type bool (optional)
        @param txt text to be searched for (defaults to "")
        @type str (optional)
        @param searchDir directory to search in (defaults to "")
        @type str (optional)
        @param openFiles flag indicating to operate on open files only
            (defaults to False)
        @type bool (optional)
        """
        if self.project.isOpen():
            self.projectButton.setEnabled(True)
            self.projectButton.setChecked(True)
        else:
            self.projectButton.setEnabled(False)
            self.dirButton.setChecked(True)
            
        self.findtextCombo.setEditText(txt)
        self.findtextCombo.lineEdit().selectAll()
        self.findtextCombo.setFocus()
        
        if self.__replaceMode != replaceMode:
            self.__toggleReplaceMode()
        
        if searchDir:
            self.__setSearchDirectory(searchDir)
        if openFiles:
            self.__setOpenFiles()
    
    @pyqtSlot()
    def __toggleReplaceMode(self):
        """
        Private slot to toggle the dialog mode.
        """
        self.__replaceMode = not self.__replaceMode
        
        # change some interface elements and properties
        self.findList.clear()
        self.clearButton.setEnabled(False)
        
        if self.__replaceMode:
            self.replaceButton.show()
            self.replaceLabel.show()
            self.replacetextCombo.show()
            
            self.replaceButton.setEnabled(False)
            self.replacetextCombo.setEditText("")
            
            font = Preferences.getEditorOtherFonts("MonospacedFont")
            self.findList.setFont(font)
            
            self.modeToggleButton.setIcon(UI.PixmapCache.getIcon("1uparrow"))
        else:
            self.replaceLabel.hide()
            self.replacetextCombo.hide()
            self.replaceButton.hide()
            
            self.findList.setFont(self.__standardListFont)
            
            self.modeToggleButton.setIcon(UI.PixmapCache.getIcon("1downarrow"))
    
    @pyqtSlot()
    def __projectOpened(self):
        """
        Private slot to react to the opening of a project.
        """
        self.projectButton.setEnabled(True)
        self.projectButton.setChecked(True)
    
    @pyqtSlot()
    def __projectClosed(self):
        """
        Private slot to react to the closing of a project.
        """
        self.projectButton.setEnabled(False)
        if self.projectButton.isChecked():
            self.dirButton.setChecked(True)
    
    @pyqtSlot(str)
    def on_findtextCombo_editTextChanged(self, text):
        """
        Private slot to handle the editTextChanged signal of the find
        text combo.
        
        @param text (ignored)
        """
        self.__enableFindButton()
    
    @pyqtSlot(str)
    def on_replacetextCombo_editTextChanged(self, text):
        """
        Private slot to handle the editTextChanged signal of the replace
        text combo.
        
        @param text (ignored)
        """
        self.__enableFindButton()
    
    @pyqtSlot(str)
    def on_dirPicker_editTextChanged(self, text):
        """
        Private slot to handle the textChanged signal of the directory
        picker.
        
        @param text (ignored)
        """
        self.__enableFindButton()
    
    @pyqtSlot()
    def on_projectButton_clicked(self):
        """
        Private slot to handle the selection of the 'Project' radio button.
        """
        self.__enableFindButton()
    
    @pyqtSlot()
    def on_dirButton_clicked(self):
        """
        Private slot to handle the selection of the 'Directory' radio button.
        """
        self.__enableFindButton()
    
    @pyqtSlot()
    def on_openFilesButton_clicked(self):
        """
        Private slot to handle the selection of the 'Open Files' radio button.
        """
        self.__enableFindButton()
    
    @pyqtSlot()
    def on_filterCheckBox_clicked(self):
        """
        Private slot to handle the selection of the file filter check box.
        """
        self.__enableFindButton()
    
    @pyqtSlot(str)
    def on_filterEdit_textEdited(self, text):
        """
        Private slot to handle the textChanged signal of the file filter edit.
        
        @param text (ignored)
        """
        self.__enableFindButton()
    
    @pyqtSlot()
    def __enableFindButton(self):
        """
        Private slot called to enable the find button.
        """
        if (
            self.findtextCombo.currentText() == "" or
            (self.dirButton.isChecked() and
             (self.dirPicker.currentText() == "" or
              not os.path.exists(os.path.abspath(
                self.dirPicker.currentText())))) or
            (self.filterCheckBox.isChecked() and
             self.filterEdit.text() == "")
        ):
            self.findButton.setEnabled(False)
        else:
            self.findButton.setEnabled(True)
    
    def __stripEol(self, txt):
        """
        Private method to strip the eol part.
        
        @param txt line of text that should be treated
        @type str
        @return text with eol stripped
        @rtype str
        """
        return txt.replace("\r", "").replace("\n", "")
    
    @pyqtSlot()
    def __stopSearch(self):
        """
        Private slot to handle the stop button being pressed.
        """
        self.__cancelSearch = True
    
    @pyqtSlot()
    def __doSearch(self):
        """
        Private slot to handle the find button being pressed.
        """
        if (
            self.__replaceMode and
            not ericApp().getObject("ViewManager").checkAllDirty()
        ):
            return
        
        self.__cancelSearch = False
        
        if self.filterCheckBox.isChecked():
            fileFilter = self.filterEdit.text()
            fileFilterList = [
                "^{0}$".format(filter.replace(".", r"\.").replace("*", ".*"))
                for filter in fileFilter.split(";")
            ]
            filterRe = re.compile("|".join(fileFilterList))
        
        if self.projectButton.isChecked():
            if self.filterCheckBox.isChecked():
                files = [
                    self.project.getRelativePath(file)
                    for file in
                    self.__getFileList(
                        self.project.getProjectPath(),
                        filterRe,
                        excludeHiddenDirs=self.excludeHiddenCheckBox
                        .isChecked(),
                    )
                ]
            else:
                files = []
                if self.sourcesCheckBox.isChecked():
                    files += self.project.pdata["SOURCES"]
                if self.formsCheckBox.isChecked():
                    files += self.project.pdata["FORMS"]
                if self.interfacesCheckBox.isChecked():
                    files += self.project.pdata["INTERFACES"]
                if self.protocolsCheckBox.isChecked():
                    files += self.project.pdata["PROTOCOLS"]
                if self.resourcesCheckBox.isChecked():
                    files += self.project.pdata["RESOURCES"]
        elif self.dirButton.isChecked():
            if not self.filterCheckBox.isChecked():
                filters = []
                if (
                    self.project.isOpen() and
                    os.path.abspath(self.dirPicker.currentText()).startswith(
                        self.project.getProjectPath())
                ):
                    if self.sourcesCheckBox.isChecked():
                        filters.extend([
                            "^{0}$".format(
                                assoc.replace(".", r"\.").replace("*", ".*")
                            ) for assoc in
                            self.project.getFiletypeAssociations("SOURCES")
                        ])
                    if self.formsCheckBox.isChecked():
                        filters.extend([
                            "^{0}$".format(
                                assoc.replace(".", r"\.").replace("*", ".*")
                            ) for assoc in
                            self.project.getFiletypeAssociations("FORMS")
                        ])
                    if self.interfacesCheckBox.isChecked():
                        filters.extend([
                            "^{0}$".format(
                                assoc.replace(".", r"\.").replace("*", ".*")
                            ) for assoc in
                            self.project.getFiletypeAssociations("INTERFACES")
                        ])
                    if self.protocolsCheckBox.isChecked():
                        filters.extend([
                            "^{0}$".format(
                                assoc.replace(".", r"\.").replace("*", ".*")
                            ) for assoc in
                            self.project.getFiletypeAssociations("PROTOCOLS")
                        ])
                    if self.resourcesCheckBox.isChecked():
                        filters.extend([
                            "^{0}$".format(
                                assoc.replace(".", r"\.").replace("*", ".*")
                            ) for assoc in
                            self.project.getFiletypeAssociations("RESOURCES")
                        ])
                else:
                    if self.sourcesCheckBox.isChecked():
                        filters.extend([
                            "^{0}$".format(
                                assoc.replace(".", r"\.").replace("*", ".*"))
                            for assoc in list(
                                Preferences.getEditorLexerAssocs().keys())
                            if assoc not in
                            self.formsExt + self.interfacesExt +
                            self.protocolsExt + self.resourcesExt
                        ])
                    if self.formsCheckBox.isChecked():
                        filters.append(self.filterForms)
                    if self.interfacesCheckBox.isChecked():
                        filters.append(self.filterInterfaces)
                    if self.protocolsCheckBox.isChecked():
                        filters.append(self.filterProtocols)
                    if self.resourcesCheckBox.isChecked():
                        filters.append(self.filterResources)
                filterString = "|".join(filters)
                filterRe = re.compile(filterString)
            files = self.__getFileList(
                os.path.abspath(self.dirPicker.currentText()),
                filterRe,
                excludeHiddenDirs=self.excludeHiddenCheckBox.isChecked(),
                excludeHiddenFiles=self.excludeHiddenCheckBox.isChecked(),
            )
        elif self.openFilesButton.isChecked():
            vm = ericApp().getObject("ViewManager")
            vm.checkAllDirty()
            files = vm.getOpenFilenames()
        
        self.findList.clear()
        QApplication.processEvents()
        self.findProgress.setMaximum(len(files))
        
        # retrieve the values
        reg = self.regexpToolButton.isChecked()
        wo = self.wordToolButton.isChecked()
        cs = self.caseToolButton.isChecked()
        ct = self.findtextCombo.currentText()
        txt = ct if reg else re.escape(ct)
        if wo:
            txt = "\\b{0}\\b".format(txt)
        flags = re.UNICODE
        if not cs:
            flags |= re.IGNORECASE
        try:
            search = re.compile(txt, flags)
        except re.error as why:
            EricMessageBox.critical(
                self,
                self.tr("Invalid search expression"),
                self.tr("""<p>The search expression is not valid.</p>"""
                        """<p>Error: {0}</p>""").format(str(why)))
            self.stopButton.setEnabled(False)
            self.findButton.setEnabled(True)
            return
        # reset the findtextCombo
        if ct in self.searchHistory:
            self.searchHistory.remove(ct)
        self.searchHistory.insert(0, ct)
        self.findtextCombo.clear()
        self.findtextCombo.addItems(self.searchHistory)
        Preferences.getSettings().setValue(
            "FindFileWidget/SearchHistory",
            self.searchHistory[:30])
        Preferences.getSettings().setValue(
            "FindFileWidget/ExcludeHidden",
            self.excludeHiddenCheckBox.isChecked())
        
        if self.__replaceMode:
            replTxt = self.replacetextCombo.currentText()
            if replTxt in self.replaceHistory:
                self.replaceHistory.remove(replTxt)
            self.replaceHistory.insert(0, replTxt)
            self.replacetextCombo.clear()
            self.replacetextCombo.addItems(self.replaceHistory)
            Preferences.getSettings().setValue(
                "FindFileWidget/ReplaceHistory",
                self.replaceHistory[:30])
        
        if self.dirButton.isChecked():
            searchDir = self.dirPicker.currentText()
            if searchDir in self.dirHistory:
                self.dirHistory.remove(searchDir)
            self.dirHistory.insert(0, searchDir)
            self.dirPicker.clear()
            self.dirPicker.addItems(self.dirHistory)
            self.dirPicker.setText(self.dirHistory[0])
            Preferences.getSettings().setValue(
                "FindFileWidget/DirectoryHistory",
                self.dirHistory[:30])
        
        # set the button states
        self.stopButton.setEnabled(True)
        self.findButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        
        # now go through all the files
        self.__populating = True
        self.findList.setUpdatesEnabled(False)
        occurrences = 0
        fileOccurrences = 0
        for progress, file in enumerate(files, start=1):
            self.__lastFileItem = None
            found = False
            if self.__cancelSearch:
                break
            
            fn = (
                os.path.join(self.project.getProjectPath(), file)
                if self.projectButton.isChecked() else
                file
            )
            # read the file and split it into textlines
            try:
                text, encoding, hashStr = Utilities.readEncodedFileWithHash(fn)
                lines = text.splitlines(True)
            except (UnicodeError, OSError):
                self.findProgress.setValue(progress)
                continue
            
            now = time.monotonic()
            # now perform the search and display the lines found
            for count, line in enumerate(lines, start=1):
                if self.__cancelSearch:
                    break
                
                contains = search.search(line)
                if contains:
                    occurrences += 1
                    found = True
                    start = contains.start()
                    end = contains.end()
                    if self.__replaceMode:
                        rline = search.sub(replTxt, line)
                    else:
                        rline = ""
                    line = self.__stripEol(line)
                    if len(line) > 1024:
                        line = "{0} ...".format(line[:1024])
                    if self.__replaceMode:
                        if len(rline) > 1024:
                            rline = "{0} ...".format(line[:1024])
                        line = "- {0}\n+ {1}".format(
                            line, self.__stripEol(rline))
                    self.__createItem(file, count, line, start, end,
                                      rline, hashStr)
                
                if time.monotonic() - now > 0.01:
                    QApplication.processEvents()
                    now = time.monotonic()
            
            if found:
                fileOccurrences += 1
            self.findProgress.setValue(progress)
        
        if not files:
            self.findProgress.setMaximum(1)
            self.findProgress.setValue(1)
        
        resultFormat = self.tr("{0} / {1}", "occurrences / files")
        self.findProgressLabel.setPath(resultFormat.format(
            self.tr("%n occurrence(s)", "", occurrences),
            self.tr("%n file(s)", "", fileOccurrences)))
        
        self.findList.setUpdatesEnabled(True)
        self.findList.sortItems(self.findList.sortColumn(),
                                self.findList.header().sortIndicatorOrder())
        self.findList.resizeColumnToContents(1)
        if self.__replaceMode:
            self.findList.header().resizeSection(0, self.__section0Size + 30)
        self.findList.header().setStretchLastSection(True)
        self.__populating = False
        
        self.stopButton.setEnabled(False)
        self.findButton.setEnabled(True)
        self.clearButton.setEnabled(self.findList.topLevelItemCount() != 0)
    
    @pyqtSlot()
    def __clearResults(self):
        """
        Private slot to clear the current search results.
        """
        self.findList.clear()
        self.replaceButton.setEnabled(False)
        self.clearButton.setEnabled(False)
        self.findProgressLabel.setPath("")
        self.findProgress.setValue(0)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_findList_itemDoubleClicked(self, itm, column):
        """
        Private slot to handle the double click on a file item.
        
        It emits a signal depending on the file extension.
        
        @param itm the double clicked tree item
        @type QTreeWidgetItem
        @param column column that was double clicked (ignored)
        @type int
        """
        if itm.parent():
            file = itm.parent().text(0)
            line = itm.data(0, self.lineRole)
            start = itm.data(0, self.startRole)
            end = itm.data(0, self.endRole)
        else:
            file = itm.text(0)
            line = 1
            start = 0
            end = 0
        
        fileName = (
            os.path.join(self.project.getProjectPath(), file)
            if self.project.isOpen() else
            file
        )
        fileExt = os.path.splitext(fileName)[1]
        
        if fileExt == ".ui":
            self.designerFile.emit(fileName)
        elif fileExt == ".ts":
            self.linguistFile.emit(fileName)
        elif fileExt == ".qm":
            self.trpreview.emit([fileName])
        elif fileExt in (".egj", ".e5g"):
            self.umlFile.emit(fileName)
        elif fileExt == ".svg":
            self.svgFile.emit(fileName)
        elif fileExt[1:] in QImageReader.supportedImageFormats():
            self.pixmapFile.emit(fileName)
        else:
            if Utilities.MimeTypes.isTextFile(fileName):
                self.sourceFile.emit(fileName, line, "", start, end)
            else:
                QDesktopServices.openUrl(QUrl(fileName))
    
    def __getFileList(self, path, filterRe, excludeHiddenDirs=False,
                      excludeHiddenFiles=False):
        """
        Private method to get a list of files to search.
        
        @param path the root directory to search in
        @type str
        @param filterRe regular expression defining the filter
            criteria
        @type regexp object
        @param excludeHiddenDirs flag indicating to exclude hidden directories
        @type bool
        @param excludeHiddenFiles flag indicating to exclude hidden files
        @type bool
        @return list of files to be processed
        @rtype list of str
        """
        path = os.path.abspath(path)
        files = []
        for dirname, dirs, filenames in os.walk(path):
            files.extend([
                os.path.join(dirname, f) for f in filenames
                if (not (excludeHiddenFiles and f.startswith(".")) and
                    re.match(filterRe, f))
            ])
            if excludeHiddenDirs:
                for d in dirs[:]:
                    if d .startswith("."):
                        dirs.remove(d)
        return files
    
    def __setSearchDirectory(self, searchDir):
        """
        Private slot to set the name of the directory to search in.
        
        @param searchDir name of the directory to search in
        @type str
        """
        self.dirButton.setChecked(True)
        self.dirPicker.setEditText(Utilities.toNativeSeparators(searchDir))
    
    @pyqtSlot()
    def __setOpenFiles(self):
        """
        Private slot to set the mode to search in open files.
        """
        self.openFilesButton.setChecked(True)
    
    @pyqtSlot()
    def on_replaceButton_clicked(self):
        """
        Private slot to perform the requested replace actions.
        """
        self.findProgress.setMaximum(self.findList.topLevelItemCount())
        self.findProgress.setValue(0)
        
        for index in range(self.findList.topLevelItemCount()):
            itm = self.findList.topLevelItem(index)
            if itm.checkState(0) in [Qt.CheckState.PartiallyChecked,
                                     Qt.CheckState.Checked]:
                file = itm.text(0)
                origHash = itm.data(0, self.md5Role)
                
                if self.projectButton.isChecked():
                    fn = os.path.join(self.project.getProjectPath(), file)
                else:
                    fn = file
                
                # read the file and split it into textlines
                try:
                    text, encoding, hashStr = (
                        Utilities.readEncodedFileWithHash(fn)
                    )
                    lines = text.splitlines(True)
                except (UnicodeError, OSError) as err:
                    EricMessageBox.critical(
                        self,
                        self.tr("Replace in Files"),
                        self.tr(
                            """<p>Could not read the file <b>{0}</b>."""
                            """ Skipping it.</p><p>Reason: {1}</p>""")
                        .format(fn, str(err))
                    )
                    self.findProgress.setValue(index)
                    continue
                
                # Check the original and the current hash. Skip the file,
                # if hashes are different.
                if origHash != hashStr:
                    EricMessageBox.critical(
                        self,
                        self.tr("Replace in Files"),
                        self.tr(
                            """<p>The current and the original hash of the"""
                            """ file <b>{0}</b> are different. Skipping it."""
                            """</p><p>Hash 1: {1}</p><p>Hash 2: {2}</p>""")
                        .format(fn, origHash, hashStr)
                    )
                    self.findProgress.setValue(index)
                    continue
                
                # replace the lines authorized by the user
                for cindex in range(itm.childCount()):
                    citm = itm.child(cindex)
                    if citm.checkState(0) == Qt.CheckState.Checked:
                        line = citm.data(0, self.lineRole)
                        rline = citm.data(0, self.replaceRole)
                        lines[line - 1] = rline
                
                # write the file
                txt = "".join(lines)
                try:
                    Utilities.writeEncodedFile(fn, txt, encoding)
                except (OSError, Utilities.CodingError, UnicodeError) as err:
                    EricMessageBox.critical(
                        self,
                        self.tr("Replace in Files"),
                        self.tr(
                            """<p>Could not save the file <b>{0}</b>."""
                            """ Skipping it.</p><p>Reason: {1}</p>""")
                        .format(fn, str(err))
                    )
            
            self.findProgress.setValue(index + 1)
        
        self.findProgressLabel.setPath("")
        
        self.findList.clear()
        self.replaceButton.setEnabled(False)
        self.findButton.setEnabled(True)
        self.clearButton.setEnabled(False)
    
    @pyqtSlot(QPoint)
    def __contextMenuRequested(self, pos):
        """
        Private slot to handle the context menu request.
        
        @param pos position the context menu shall be shown
        @type QPoint
        """
        menu = QMenu(self)
        
        menu.addAction(self.tr("Open"), self.__openFile)
        menu.addAction(self.tr("Copy Path to Clipboard"),
                       self.__copyToClipboard)
        
        menu.exec(QCursor.pos())
    
    @pyqtSlot()
    def __openFile(self):
        """
        Private slot to open the currently selected entry.
        """
        itm = self.findList.selectedItems()[0]
        self.on_findList_itemDoubleClicked(itm, 0)
    
    @pyqtSlot()
    def __copyToClipboard(self):
        """
        Private slot to copy the path of an entry to the clipboard.
        """
        itm = self.findList.selectedItems()[0]
        fn = itm.parent().text(0) if itm.parent() else itm.text(0)
        
        cb = QApplication.clipboard()
        cb.setText(fn)


class FindFileDialog(QDialog):
    """
    Class implementing a dialog to search for text in files and replace it
    with some other text.
    
    The occurrences found are displayed in a tree showing the file name,
    the line number and the text found. The file will be opened upon a double
    click onto the respective entry of the list. If the widget is in replace
    mode the line below shows the text after replacement. Replacements can
    be authorized by ticking them on. Pressing the replace button performs
    all ticked replacement operations.
    
    @signal sourceFile(str, int, str, int, int) emitted to open a source file
        at a specificline
    @signal designerFile(str) emitted to open a Qt-Designer file
    @signal linguistFile(str) emitted to open a Qt-Linguist (*.ts) file
    @signal trpreview([str]) emitted to preview Qt-Linguist (*.qm) files
    @signal pixmapFile(str) emitted to open a pixmap file
    @signal svgFile(str) emitted to open a SVG file
    @signal umlFile(str) emitted to open an eric UML file
    """
    sourceFile = pyqtSignal(str, int, str, int, int)
    designerFile = pyqtSignal(str)
    linguistFile = pyqtSignal(str)
    trpreview = pyqtSignal(list)
    pixmapFile = pyqtSignal(str)
    svgFile = pyqtSignal(str)
    umlFile = pyqtSignal(str)
    
    def __init__(self, project, parent=None):
        """
        Constructor
        
        @param project reference to the project object
        @type Project
        @param parent parent widget of this dialog (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Window)
        
        self.__layout = QVBoxLayout()
        
        self.__findWidget = FindFileWidget(project, self)
        self.__layout.addWidget(self.__findWidget)
        
        self.__buttonBox = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close,
            Qt.Orientation.Horizontal,
            self
        )
        self.__buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setAutoDefault(False)
        self.__layout.addWidget(self.__buttonBox)
        
        self.setLayout(self.__layout)
        self.resize(600, 800)
        
        # connect the widgets
        self.__findWidget.sourceFile.connect(self.sourceFile)
        self.__findWidget.designerFile.connect(self.designerFile)
        self.__findWidget.linguistFile.connect(self.linguistFile)
        self.__findWidget.trpreview.connect(self.trpreview)
        self.__findWidget.pixmapFile.connect(self.pixmapFile)
        self.__findWidget.svgFile.connect(self.svgFile)
        self.__findWidget.umlFile.connect(self.umlFile)
        
        self.__buttonBox.accepted.connect(self.accept)
        self.__buttonBox.rejected.connect(self.reject)
    
    def activate(self, replaceMode=False, txt="", searchDir="",
                 openFiles=False):
        """
        Public method to activate the dialog with a given mode, a text
        to search for and some search parameters.
        
        @param replaceMode flag indicating replacement mode (defaults to False)
        @type bool (optional)
        @param txt text to be searched for (defaults to "")
        @type str (optional)
        @param searchDir directory to search in (defaults to "")
        @type str (optional)
        @param openFiles flag indicating to operate on open files only
            (defaults to False)
        @type bool (optional)
        """
        self.__findWidget.activate(replaceMode=replaceMode, txt=txt,
                                   searchDir=searchDir, openFiles=openFiles)
        
        self.raise_()
        self.activateWindow()
        self.show()
