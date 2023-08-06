# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the pip packages management widget.
"""

import textwrap
import os
import html.parser
import contextlib

from packaging.specifiers import SpecifierSet

from PyQt6.QtCore import pyqtSlot, Qt, QUrl, QUrlQuery
from PyQt6.QtGui import QIcon
from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import (
    QWidget, QToolButton, QApplication, QHeaderView, QTreeWidgetItem,
    QMenu, QDialog, QAbstractItemView
)

from EricWidgets.EricApplication import ericApp
from EricWidgets import EricMessageBox
from EricGui.EricOverrideCursor import EricOverrideCursor

from .PipVulnerabilityChecker import Package, VulnerabilityCheckError
from .Ui_PipPackagesWidget import Ui_PipPackagesWidget

import UI.PixmapCache
import Globals
import Preferences


class PypiSearchResultsParser(html.parser.HTMLParser):
    """
    Class implementing the parser for the PyPI search result page.
    """
    ClassPrefix = "package-snippet__"
    
    def __init__(self, data):
        """
        Constructor
        
        @param data data to be parsed
        @type str
        """
        super().__init__()
        self.__results = []
        self.__activeClass = None
        self.feed(data)
    
    def __getClass(self, attrs):
        """
        Private method to extract the class attribute out of the list of
        attributes.
        
        @param attrs list of tag attributes as (name, value) tuples
        @type list of tuple of (str, str)
        @return value of the 'class' attribute or None
        @rtype str
        """
        for name, value in attrs:
            if name == "class":
                return value
        
        return None
    
    def __getDate(self, attrs):
        """
        Private method to extract the datetime attribute out of the list of
        attributes and process it.
        
        @param attrs list of tag attributes as (name, value) tuples
        @type list of tuple of (str, str)
        @return value of the 'class' attribute or None
        @rtype str
        """
        for name, value in attrs:
            if name == "datetime":
                return value.split("T")[0]
        
        return None
    
    def handle_starttag(self, tag, attrs):
        """
        Public method to process the start tag.
        
        @param tag tag name (all lowercase)
        @type str
        @param attrs list of tag attributes as (name, value) tuples
        @type list of tuple of (str, str)
        """
        if tag == "a" and self.__getClass(attrs) == "package-snippet":
            self.__results.append({})
        
        if tag in ("span", "p"):
            tagClass = self.__getClass(attrs)
            if tagClass in (
                "package-snippet__name", "package-snippet__description",
                "package-snippet__version", "package-snippet__released",
                "package-snippet__created",
            ):
                self.__activeClass = tagClass
            else:
                self.__activeClass = None
        elif tag == "time":
            attributeName = self.__activeClass.replace(self.ClassPrefix, "")
            self.__results[-1][attributeName] = self.__getDate(attrs)
            self.__activeClass = None
        else:
            self.__activeClass = None
    
    def handle_data(self, data):
        """
        Public method process arbitrary data.
        
        @param data data to be processed
        @type str
        """
        if self.__activeClass is not None:
            attributeName = self.__activeClass.replace(self.ClassPrefix, "")
            self.__results[-1][attributeName] = data
    
    def handle_endtag(self, tag):
        """
        Public method to process the end tag.
        
        @param tag tag name (all lowercase)
        @type str
        """
        self.__activeClass = None
    
    def getResults(self):
        """
        Public method to get the extracted search results.
        
        @return extracted result data
        @rtype list of dict
        """
        return self.__results


class PipPackagesWidget(QWidget, Ui_PipPackagesWidget):
    """
    Class implementing the pip packages management widget.
    """
    ShowProcessGeneralMode = 0
    ShowProcessClassifiersMode = 1
    ShowProcessEntryPointsMode = 2
    ShowProcessFilesListMode = 3
    
    SearchVersionRole = Qt.ItemDataRole.UserRole + 1
    VulnerabilityRole = Qt.ItemDataRole.UserRole + 2
    
    PackageColumn = 0
    InstalledVersionColumn = 1
    AvailableVersionColumn = 2
    VulnerabilityColumn = 3
    
    DepPackageColumn = 0
    DepInstalledVersionColumn = 1
    DepRequiredVersionColumn = 2
    
    def __init__(self, pip, parent=None):
        """
        Constructor
        
        @param pip reference to the global pip interface
        @type Pip
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.layout().setContentsMargins(0, 3, 0, 0)
        
        self.viewToggleButton.setIcon(UI.PixmapCache.getIcon("viewListTree"))
        
        self.pipMenuButton.setObjectName(
            "pip_supermenu_button")
        self.pipMenuButton.setIcon(UI.PixmapCache.getIcon("superMenu"))
        self.pipMenuButton.setToolTip(self.tr("pip Menu"))
        self.pipMenuButton.setPopupMode(
            QToolButton.ToolButtonPopupMode.InstantPopup)
        self.pipMenuButton.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.pipMenuButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pipMenuButton.setAutoRaise(True)
        self.pipMenuButton.setShowMenuInside(True)
        
        self.refreshButton.setIcon(
            UI.PixmapCache.getIcon("reload"))
        self.upgradeButton.setIcon(
            UI.PixmapCache.getIcon("1uparrow"))
        self.upgradeAllButton.setIcon(
            UI.PixmapCache.getIcon("2uparrow"))
        self.uninstallButton.setIcon(
            UI.PixmapCache.getIcon("minus"))
        self.showPackageDetailsButton.setIcon(
            UI.PixmapCache.getIcon("info"))
        self.searchToggleButton.setIcon(
            UI.PixmapCache.getIcon("find"))
        self.searchButton.setIcon(
            UI.PixmapCache.getIcon("findNext"))
        self.searchMoreButton.setIcon(
            UI.PixmapCache.getIcon("plus"))
        self.installButton.setIcon(
            UI.PixmapCache.getIcon("plus"))
        self.installUserSiteButton.setIcon(
            UI.PixmapCache.getIcon("addUser"))
        self.showDetailsButton.setIcon(
            UI.PixmapCache.getIcon("info"))
        
        self.refreshDependenciesButton.setIcon(
            UI.PixmapCache.getIcon("reload"))
        self.showDepPackageDetailsButton.setIcon(
            UI.PixmapCache.getIcon("info"))
        
        self.__pip = pip
        
        self.packagesList.header().setSortIndicator(
            PipPackagesWidget.PackageColumn, Qt.SortOrder.AscendingOrder)
        self.dependenciesList.header().setSortIndicator(
            PipPackagesWidget.DepPackageColumn, Qt.SortOrder.AscendingOrder)
        
        self.__infoLabels = {
            "name": self.tr("Name:"),
            "version": self.tr("Version:"),
            "location": self.tr("Location:"),
            "requires": self.tr("Requires:"),
            "summary": self.tr("Summary:"),
            "home-page": self.tr("Homepage:"),
            "author": self.tr("Author:"),
            "author-email": self.tr("Author Email:"),
            "license": self.tr("License:"),
            "metadata-version": self.tr("Metadata Version:"),
            "installer": self.tr("Installer:"),
            "classifiers": self.tr("Classifiers:"),
            "entry-points": self.tr("Entry Points:"),
            "files": self.tr("Files:"),
        }
        self.infoWidget.setHeaderLabels(["Key", "Value"])
        self.dependencyInfoWidget.setHeaderLabels(["Key", "Value"])
        
        venvManager = ericApp().getObject("VirtualEnvManager")
        venvManager.virtualEnvironmentAdded.connect(
            self.on_refreshButton_clicked)
        venvManager.virtualEnvironmentRemoved.connect(
            self.on_refreshButton_clicked)
        self.__selectedEnvironment = None
        
        project = ericApp().getObject("Project")
        project.projectOpened.connect(
            self.__projectOpened)
        project.projectClosed.connect(
            self.__projectClosed)
        
        self.__initPipMenu()
        self.__populateEnvironments()
        self.__updateActionButtons()
        self.__updateDepActionButtons()
        
        self.statusLabel.hide()
        self.searchWidget.hide()
        self.__lastSearchPage = 0
        
        self.__queryName = []
        self.__querySummary = []
        
        self.__replies = []
        
        self.__packageDetailsDialog = None
        
        self.viewsStackWidget.setCurrentWidget(self.packagesPage)
    
    @pyqtSlot()
    def __projectOpened(self):
        """
        Private slot to handle the projectOpened signal.
        """
        projectVenv = self.__pip.getProjectEnvironmentString()
        if projectVenv:
            self.environmentsComboBox.insertItem(1, projectVenv)
    
    @pyqtSlot(bool)
    def __projectClosed(self, shutdown):
        """
        Private slot to handle the projectClosed signal.
        
        @param shutdown flag indicating the IDE shutdown
        @type bool
        """
        if not shutdown:
            # the project entry is always at index 1
            self.environmentsComboBox.removeItem(1)
    
    def __populateEnvironments(self):
        """
        Private method to get a list of environments and populate the selector.
        """
        self.environmentsComboBox.addItem("")
        projectVenv = self.__pip.getProjectEnvironmentString()
        if projectVenv:
            self.environmentsComboBox.addItem(projectVenv)
        self.environmentsComboBox.addItems(
            self.__pip.getVirtualenvNames(
                noRemote=True,
                noConda=Preferences.getPip("ExcludeCondaEnvironments")
            )
        )
    
    def __isPipAvailable(self):
        """
        Private method to check, if the pip package is available for the
        selected environment.
        
        @return flag indicating availability
        @rtype bool
        """
        available = False
        
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            available = (
                len(self.packagesList.findItems(
                    "pip",
                    Qt.MatchFlag.MatchExactly |
                    Qt.MatchFlag.MatchCaseSensitive)) == 1
            )
        
        return available
    
    def __availablePipVersion(self):
        """
        Private method to get the pip version of the selected environment.
        
        @return tuple containing the version number or tuple with all zeros
            in case pip is not available
        @rtype tuple of int
        """
        pipVersionTuple = (0, 0, 0)
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            pipList = self.packagesList.findItems(
                "pip",
                Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchCaseSensitive
            )
            if len(pipList) > 0:
                pipVersionTuple = Globals.versionToTuple(
                    pipList[0].text(PipPackagesWidget.InstalledVersionColumn))
        
        return pipVersionTuple
    
    def getPip(self):
        """
        Public method to get a reference to the pip interface object.
        
        @return reference to the pip interface object
        @rtype Pip
        """
        return self.__pip
    
    #######################################################################
    ## Slots handling widget signals below
    #######################################################################
    
    def __selectedUpdateableItems(self):
        """
        Private method to get a list of selected items that can be updated.
        
        @return list of selected items that can be updated
        @rtype list of QTreeWidgetItem
        """
        return [
            itm for itm in self.packagesList.selectedItems()
            if bool(itm.text(PipPackagesWidget.AvailableVersionColumn))
        ]
    
    def __allUpdateableItems(self):
        """
        Private method to get a list of all items that can be updated.
        
        @return list of all items that can be updated
        @rtype list of QTreeWidgetItem
        """
        updateableItems = []
        for index in range(self.packagesList.topLevelItemCount()):
            itm = self.packagesList.topLevelItem(index)
            if itm.text(PipPackagesWidget.AvailableVersionColumn):
                updateableItems.append(itm)
        
        return updateableItems
    
    def __updateActionButtons(self):
        """
        Private method to set the state of the action buttons.
        """
        if self.__isPipAvailable():
            self.upgradeButton.setEnabled(
                bool(self.__selectedUpdateableItems()))
            self.uninstallButton.setEnabled(
                bool(self.packagesList.selectedItems()))
            self.upgradeAllButton.setEnabled(
                bool(self.__allUpdateableItems()))
            self.showPackageDetailsButton.setEnabled(
                len(self.packagesList.selectedItems()) == 1)
        else:
            self.upgradeButton.setEnabled(False)
            self.uninstallButton.setEnabled(False)
            self.upgradeAllButton.setEnabled(False)
            self.showPackageDetailsButton.setEnabled(False)
    
    def __refreshPackagesList(self):
        """
        Private method to refresh the packages list.
        """
        self.packagesList.clear()
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            interpreter = self.__pip.getVirtualenvInterpreter(venvName)
            if interpreter:
                self.statusLabel.show()
                self.statusLabel.setText(
                    self.tr("Getting installed packages..."))
                
                with EricOverrideCursor():
                    # 1. populate with installed packages
                    self.packagesList.setUpdatesEnabled(False)
                    installedPackages = self.__pip.getInstalledPackages(
                        venvName,
                        localPackages=self.localCheckBox.isChecked(),
                        notRequired=self.notRequiredCheckBox.isChecked(),
                        usersite=self.userCheckBox.isChecked(),
                    )
                    for package, version in installedPackages:
                        QTreeWidgetItem(self.packagesList,
                                        [package, version, "", ""])
                    self.packagesList.setUpdatesEnabled(True)
                    self.statusLabel.setText(
                        self.tr("Getting outdated packages..."))
                    QApplication.processEvents()
                    
                    # 2. update with update information
                    self.packagesList.setUpdatesEnabled(False)
                    outdatedPackages = self.__pip.getOutdatedPackages(
                        venvName,
                        localPackages=self.localCheckBox.isChecked(),
                        notRequired=self.notRequiredCheckBox.isChecked(),
                        usersite=self.userCheckBox.isChecked(),
                    )
                    for package, _version, latest in outdatedPackages:
                        items = self.packagesList.findItems(
                            package,
                            Qt.MatchFlag.MatchExactly |
                            Qt.MatchFlag.MatchCaseSensitive
                        )
                        if items:
                            itm = items[0]
                            itm.setText(
                                PipPackagesWidget.AvailableVersionColumn,
                                latest)
                    
                    self.packagesList.sortItems(
                        PipPackagesWidget.PackageColumn,
                        Qt.SortOrder.AscendingOrder)
                    for col in range(self.packagesList.columnCount()):
                        self.packagesList.resizeColumnToContents(col)
                    self.packagesList.setUpdatesEnabled(True)
                    
                    # 3. update with vulnerability information
                    if self.vulnerabilityCheckBox.isChecked():
                        self.__updateVulnerabilityData()
                self.statusLabel.hide()
        
        self.__updateActionButtons()
        self.__updateSearchActionButtons()
        self.__updateSearchButton()
        self.__updateSearchMoreButton(False)
    
    @pyqtSlot(str)
    def on_environmentsComboBox_currentTextChanged(self, name):
        """
        Private slot handling the selection of a Python environment.
        
        @param name name of the selected Python environment
        @type str
        """
        if name != self.__selectedEnvironment:
            if self.viewToggleButton.isChecked():
                self.__refreshDependencyTree()
            else:
                self.__refreshPackagesList()
            self.__selectedEnvironment = name
    
    @pyqtSlot()
    def on_localCheckBox_clicked(self):
        """
        Private slot handling the switching of the local mode.
        """
        self.__refreshPackagesList()
    
    @pyqtSlot()
    def on_notRequiredCheckBox_clicked(self):
        """
        Private slot handling the switching of the 'not required' mode.
        """
        self.__refreshPackagesList()
    
    @pyqtSlot()
    def on_userCheckBox_clicked(self):
        """
        Private slot handling the switching of the 'user-site' mode.
        """
        self.__refreshPackagesList()
    
    def __showPackageInformation(self, packageName, infoWidget):
        """
        Private method to show information for a package.
        
        @param packageName name of the package
        @type str
        @param infoWidget reference to the widget to contain the information
        @type QTreeWidget
        """
        environment = self.environmentsComboBox.currentText()
        interpreter = self.__pip.getVirtualenvInterpreter(environment)
        if not interpreter:
            return
        
        args = ["-m", "pip", "show"]
        if self.verboseCheckBox.isChecked():
            args.append("--verbose")
        if self.installedFilesCheckBox.isChecked():
            args.append("--files")
        args.append(packageName)
        
        with EricOverrideCursor():
            success, output = self.__pip.runProcess(args, interpreter)
            
            if success and output:
                mode = self.ShowProcessGeneralMode
                for line in output.splitlines():
                    line = line.rstrip()
                    if line != "---":
                        if mode != self.ShowProcessGeneralMode:
                            if line[0] == " ":
                                QTreeWidgetItem(
                                    infoWidget,
                                    [" ", line.strip()])
                            else:
                                mode = self.ShowProcessGeneralMode
                        if mode == self.ShowProcessGeneralMode:
                            try:
                                label, info = line.split(": ", 1)
                            except ValueError:
                                label = line[:-1]
                                info = ""
                            label = label.lower()
                            if label in self.__infoLabels:
                                QTreeWidgetItem(
                                    infoWidget,
                                    [self.__infoLabels[label], info])
                            if label == "files":
                                mode = self.ShowProcessFilesListMode
                            elif label == "classifiers":
                                mode = self.ShowProcessClassifiersMode
                            elif label == "entry-points":
                                mode = self.ShowProcessEntryPointsMode
                infoWidget.scrollToTop()
            
            header = infoWidget.header()
            header.setStretchLastSection(False)
            header.resizeSections(QHeaderView.ResizeMode.ResizeToContents)
            if (
                header.sectionSize(0) + header.sectionSize(1) <
                header.width()
            ):
                header.setStretchLastSection(True)
    
    @pyqtSlot()
    def on_packagesList_itemSelectionChanged(self):
        """
        Private slot reacting on a change of selected items.
        """
        if len(self.packagesList.selectedItems()) == 0:
            self.infoWidget.clear()
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_packagesList_itemPressed(self, item, column):
        """
        Private slot reacting on a package item being pressed.
        
        @param item reference to the pressed item
        @type QTreeWidgetItem
        @param column pressed column
        @type int
        """
        self.infoWidget.clear()
        
        if item is not None:
            if (
                column == PipPackagesWidget.VulnerabilityColumn and
                bool(item.text(PipPackagesWidget.VulnerabilityColumn))
            ):
                self.__showVulnerabilityInformation(
                    item.text(PipPackagesWidget.PackageColumn),
                    item.text(PipPackagesWidget.InstalledVersionColumn),
                    item.data(PipPackagesWidget.VulnerabilityColumn,
                              PipPackagesWidget.VulnerabilityRole)
                )
            else:
                self.__showPackageInformation(
                    item.text(PipPackagesWidget.PackageColumn),
                    self.infoWidget
                )
        
        self.__updateActionButtons()
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_packagesList_itemActivated(self, item, column):
        """
        Private slot reacting on a package item being activated.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column activated column
        @type int
        """
        packageName = item.text(PipPackagesWidget.PackageColumn)
        upgradable = bool(item.text(PipPackagesWidget.AvailableVersionColumn))
        if column == PipPackagesWidget.InstalledVersionColumn:
            # show details for installed version
            packageVersion = item.text(
                PipPackagesWidget.InstalledVersionColumn)
        else:
            # show details for available version or installed one
            if item.text(PipPackagesWidget.AvailableVersionColumn):
                packageVersion = item.text(
                    PipPackagesWidget.AvailableVersionColumn)
            else:
                packageVersion = item.text(
                    PipPackagesWidget.InstalledVersionColumn)
        
        self.__showPackageDetails(packageName, packageVersion,
                                  upgradable=upgradable)
    
    @pyqtSlot(bool)
    def on_verboseCheckBox_clicked(self, checked):
        """
        Private slot to handle a change of the verbose package information
        checkbox.
        
        @param checked state of the checkbox
        @type bool
        """
        self.on_packagesList_itemPressed(self.packagesList.currentItem(),
                                         self.packagesList.currentColumn())
    
    @pyqtSlot(bool)
    def on_installedFilesCheckBox_clicked(self, checked):
        """
        Private slot to handle a change of the installed files information
        checkbox.
        
        @param checked state of the checkbox
        @type bool
        """
        self.on_packagesList_itemPressed(self.packagesList.currentItem(),
                                         self.packagesList.currentColumn())
    
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """
        Private slot to refresh the display.
        """
        currentEnvironment = self.environmentsComboBox.currentText()
        self.environmentsComboBox.clear()
        self.packagesList.clear()
        
        with EricOverrideCursor():
            self.__populateEnvironments()
            
            index = self.environmentsComboBox.findText(
                currentEnvironment,
                Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchCaseSensitive
            )
            if index != -1:
                self.environmentsComboBox.setCurrentIndex(index)
        
        self.__updateActionButtons()
    
    @pyqtSlot()
    def on_upgradeButton_clicked(self):
        """
        Private slot to upgrade selected packages of the selected environment.
        """
        packages = [itm.text(PipPackagesWidget.PackageColumn)
                    for itm in self.__selectedUpdateableItems()]
        if packages:
            self.executeUpgradePackages(packages)
    
    @pyqtSlot()
    def on_upgradeAllButton_clicked(self):
        """
        Private slot to upgrade all packages of the selected environment.
        """
        packages = [itm.text(PipPackagesWidget.PackageColumn)
                    for itm in self.__allUpdateableItems()]
        if packages:
            self.executeUpgradePackages(packages)
    
    @pyqtSlot()
    def on_uninstallButton_clicked(self):
        """
        Private slot to remove selected packages of the selected environment.
        """
        packages = [itm.text(PipPackagesWidget.PackageColumn)
                    for itm in self.packagesList.selectedItems()]
        self.executeUninstallPackages(packages)
    
    def executeUninstallPackages(self, packages):
        """
        Public method to uninstall the given list of packages.
        
        @param packages list of package names to be uninstalled
        @type list of str
        """
        if packages:
            ok = self.__pip.uninstallPackages(
                packages,
                venvName=self.environmentsComboBox.currentText())
            if ok:
                self.on_refreshButton_clicked()
    
    def executeUpgradePackages(self, packages):
        """
        Public method to execute the pip upgrade command.
        
        @param packages list of package names to be upgraded
        @type list of str
        """
        ok = self.__pip.upgradePackages(
            packages, venvName=self.environmentsComboBox.currentText(),
            userSite=self.userCheckBox.isChecked())
        if ok:
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def on_showPackageDetailsButton_clicked(self):
        """
        Private slot to show information for the selected package.
        """
        item = self.packagesList.selectedItems()[0]
        if item:
            packageName = item.text(PipPackagesWidget.PackageColumn)
            upgradable = bool(item.text(
                PipPackagesWidget.AvailableVersionColumn))
            # show details for available version or installed one
            if item.text(PipPackagesWidget.AvailableVersionColumn):
                packageVersion = item.text(
                    PipPackagesWidget.AvailableVersionColumn)
            else:
                packageVersion = item.text(
                    PipPackagesWidget.InstalledVersionColumn)
            
            self.__showPackageDetails(packageName, packageVersion,
                                      upgradable=upgradable)
    
    #######################################################################
    ## Search widget related methods below
    #######################################################################
    
    def __updateSearchActionButtons(self):
        """
        Private method to update the action button states of the search widget.
        """
        installEnable = (
            len(self.searchResultList.selectedItems()) > 0 and
            self.environmentsComboBox.currentIndex() > 0 and
            self.__isPipAvailable()
        )
        self.installButton.setEnabled(installEnable)
        self.installUserSiteButton.setEnabled(installEnable)
        
        self.showDetailsButton.setEnabled(
            len(self.searchResultList.selectedItems()) == 1 and
            self.__isPipAvailable()
        )
    
    def __updateSearchButton(self):
        """
        Private method to update the state of the search button.
        """
        self.searchButton.setEnabled(
            bool(self.searchEditName.text()) and
            self.__isPipAvailable()
        )
    
    def __updateSearchMoreButton(self, enable):
        """
        Private method to update the state of the search more button.
        
        @param enable flag indicating the desired enable state
        @type bool
        """
        self.searchMoreButton.setEnabled(
            enable and
            bool(self.searchEditName.text()) and
            self.__isPipAvailable()
        )
    
    @pyqtSlot(bool)
    def on_searchToggleButton_toggled(self, checked):
        """
        Private slot to togle the search widget.
        
        @param checked state of the search widget button
        @type bool
        """
        self.searchWidget.setVisible(checked)
        
        if checked:
            self.searchEditName.setFocus(Qt.FocusReason.OtherFocusReason)
            self.searchEditName.selectAll()
            
            self.__updateSearchActionButtons()
            self.__updateSearchButton()
            self.__updateSearchMoreButton(False)
    
    @pyqtSlot(str)
    def on_searchEditName_textChanged(self, txt):
        """
        Private slot handling a change of the search term.
        
        @param txt search term
        @type str
        """
        self.__updateSearchButton()
    
    @pyqtSlot()
    def on_searchEditName_returnPressed(self):
        """
        Private slot initiating a search via a press of the Return key.
        """
        if (
            bool(self.searchEditName.text()) and
            self.__isPipAvailable()
        ):
            self.__searchFirst()
    
    @pyqtSlot()
    def on_searchButton_clicked(self):
        """
        Private slot handling a press of the search button.
        """
        self.__searchFirst()
    
    @pyqtSlot()
    def on_searchMoreButton_clicked(self):
        """
        Private slot handling a press of the search more button.
        """
        self.__search(self.__lastSearchPage + 1)
    
    @pyqtSlot()
    def on_searchResultList_itemSelectionChanged(self):
        """
        Private slot handling changes of the search result selection.
        """
        self.__updateSearchActionButtons()
    
    def __searchFirst(self):
        """
        Private method to perform the search for packages.
        """
        self.searchResultList.clear()
        self.searchInfoLabel.clear()
        
        self.__updateSearchMoreButton(False)
        
        self.__search()
    
    def __search(self, page=1):
        """
        Private method to perform the search by calling the PyPI search URL.
        
        @param page search page to retrieve (defaults to 1)
        @type int (optional)
        """
        self.__lastSearchPage = page
        
        self.searchButton.setEnabled(False)
        
        searchTerm = self.searchEditName.text().strip()
        searchTerm = bytes(QUrl.toPercentEncoding(searchTerm)).decode()
        urlQuery = QUrlQuery()
        urlQuery.addQueryItem("q", searchTerm)
        urlQuery.addQueryItem("page", str(page))
        url = QUrl(self.__pip.getIndexUrlSearch())
        url.setQuery(urlQuery)
        
        request = QNetworkRequest(QUrl(url))
        request.setAttribute(
            QNetworkRequest.Attribute.CacheLoadControlAttribute,
            QNetworkRequest.CacheLoadControl.AlwaysNetwork)
        reply = self.__pip.getNetworkAccessManager().get(request)
        reply.finished.connect(
            lambda: self.__searchResponse(reply))
        self.__replies.append(reply)
    
    def __searchResponse(self, reply):
        """
        Private method to extract the search result data from the response.
        
        @param reply reference to the reply object containing the data
        @type QNetworkReply
        """
        if reply in self.__replies:
            self.__replies.remove(reply)
        
        urlQuery = QUrlQuery(reply.url())
        searchTerm = urlQuery.queryItemValue("q")
        
        if reply.error() != QNetworkReply.NetworkError.NoError:
            EricMessageBox.warning(
                None,
                self.tr("Search PyPI"),
                self.tr(
                    "<p>Received an error while searching for <b>{0}</b>.</p>"
                    "<p>Error: {1}</p>"
                ).format(searchTerm, reply.errorString())
            )
            reply.deleteLater()
            return
        
        data = bytes(reply.readAll()).decode()
        reply.deleteLater()
        
        results = PypiSearchResultsParser(data).getResults()
        if results:
            # PyPI returns max. 20 entries per page
            if len(results) < 20:
                msg = self.tr("%n package(s) found.", "",
                              (self.__lastSearchPage - 1) * 20 + len(results))
                self.__updateSearchMoreButton(False)
            else:
                msg = self.tr("Showing first {0} packages found.").format(
                    self.__lastSearchPage * 20)
                self.__updateSearchMoreButton(True)
            self.searchInfoLabel.setText(msg)
            lastItem = self.searchResultList.topLevelItem(
                self.searchResultList.topLevelItemCount() - 1)
        else:
            self.__updateSearchMoreButton(False)
            if self.__lastSearchPage == 1:
                EricMessageBox.warning(
                    self,
                    self.tr("Search PyPI"),
                    self.tr("""<p>There were no results for <b>{0}</b>.</p>""")
                    .format(searchTerm)
                )
                self.searchInfoLabel.setText(
                    self.tr("""<p>There were no results for <b>{0}</b>.</p>""")
                    .format(searchTerm)
                )
            else:
                EricMessageBox.warning(
                    self,
                    self.tr("Search PyPI"),
                    self.tr("""<p>There were no more results for"""
                            """ <b>{0}</b>.</p>""").format(searchTerm)
                )
            lastItem = None
        
        wrapper = textwrap.TextWrapper(width=80)
        for result in results:
            try:
                description = "\n".join([
                    wrapper.fill(line) for line in
                    result['description'].strip().splitlines()
                ])
            except KeyError:
                description = ""
            date = (
                result["released"]
                if "released" in result else
                result["created"]
            )
            itm = QTreeWidgetItem(
                self.searchResultList, [
                    result['name'].strip(),
                    result['version'],
                    date.strip(),
                    description,
                ])
            itm.setData(0, self.SearchVersionRole, result['version'])
        
        if lastItem:
            self.searchResultList.scrollToItem(
                lastItem,
                QAbstractItemView.ScrollHint.PositionAtTop)
        
        header = self.searchResultList.header()
        header.setStretchLastSection(False)
        header.resizeSections(QHeaderView.ResizeMode.ResizeToContents)
        headerSize = 0
        for col in range(header.count()):
            headerSize += header.sectionSize(col)
        if headerSize < header.width():
            header.setStretchLastSection(True)
        
        self.__finishSearch()
    
    def __finishSearch(self):
        """
        Private slot performing the search finishing actions.
        """
        self.__updateSearchActionButtons()
        self.__updateSearchButton()
        
        self.searchEditName.setFocus(Qt.FocusReason.OtherFocusReason)
    
    @pyqtSlot()
    def on_installButton_clicked(self):
        """
        Private slot to handle pressing the Install button..
        """
        packages = [
            itm.text(0).strip()
            for itm in self.searchResultList.selectedItems()
        ]
        self.executeInstallPackages(packages)
    
    @pyqtSlot()
    def on_installUserSiteButton_clicked(self):
        """
        Private slot to handle pressing the Install to User-Site button..
        """
        packages = [
            itm.text(0).strip()
            for itm in self.searchResultList.selectedItems()
        ]
        self.executeInstallPackages(packages, userSite=True)
    
    def executeInstallPackages(self, packages, userSite=False):
        """
        Public method to install the given list of packages.
        
        @param packages list of package names to be installed
        @type list of str
        @param userSite flag indicating to install to the user directory
        @type bool
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName and packages:
            self.__pip.installPackages(packages, venvName=venvName,
                                       userSite=userSite)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def on_showDetailsButton_clicked(self):
        """
        Private slot to handle pressing the Show Details button.
        """
        self.__showSearchedDetails()
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_searchResultList_itemActivated(self, item, column):
        """
        Private slot reacting on an search result item activation.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column activated column
        @type int
        """
        self.__showSearchedDetails(item)
    
    def __showSearchedDetails(self, item=None):
        """
        Private slot to show details about the selected search result package.
        
        @param item reference to the search result item to show details for
        @type QTreeWidgetItem
        """
        self.showDetailsButton.setEnabled(False)
        
        if not item:
            item = self.searchResultList.selectedItems()[0]
        
        packageVersion = item.data(0, self.SearchVersionRole)
        packageName = item.text(0)
        
        self.__showPackageDetails(packageName, packageVersion,
                                  installable=True)
    
    def __showPackageDetails(self, packageName, packageVersion,
                             upgradable=False, installable=False):
        """
        Private method to populate the package details dialog.
        
        @param packageName name of the package to show details for
        @type str
        @param packageVersion version of the package
        @type str
        @param upgradable flag indicating that the package may be upgraded
            (defaults to False)
        @type bool (optional)
        @param installable flag indicating that the package may be installed
            (defaults to False)
        @type bool (optional)
        """
        with EricOverrideCursor():
            packageData = self.__pip.getPackageDetails(
                packageName, packageVersion)
        
        if packageData:
            from .PipPackageDetailsDialog import PipPackageDetailsDialog
            
            self.showDetailsButton.setEnabled(True)
            
            if installable:
                buttonsMode = PipPackageDetailsDialog.ButtonInstall
            elif upgradable:
                buttonsMode = (
                    PipPackageDetailsDialog.ButtonRemove |
                    PipPackageDetailsDialog.ButtonUpgrade
                )
            else:
                buttonsMode = PipPackageDetailsDialog.ButtonRemove
            
            if self.__packageDetailsDialog is not None:
                self.__packageDetailsDialog.close()
            
            self.__packageDetailsDialog = (
                PipPackageDetailsDialog(packageData, buttonsMode=buttonsMode,
                                        parent=self)
            )
            self.__packageDetailsDialog.show()
        else:
            EricMessageBox.warning(
                self,
                self.tr("Search PyPI"),
                self.tr("""<p>No package details info for <b>{0}</b>"""
                        """ available.</p>""").format(packageName))
    
    #######################################################################
    ## Menu related methods below
    #######################################################################
        
    def __initPipMenu(self):
        """
        Private method to create the super menu and attach it to the super
        menu button.
        """
        self.__pipMenu = QMenu()
        self.__installPipAct = self.__pipMenu.addAction(
            self.tr("Install Pip"),
            self.__installPip)
        self.__installPipUserAct = self.__pipMenu.addAction(
            self.tr("Install Pip to User-Site"),
            self.__installPipUser)
        self.__repairPipAct = self.__pipMenu.addAction(
            self.tr("Repair Pip"),
            self.__repairPip)
        self.__pipMenu.addSeparator()
        self.__installPackagesAct = self.__pipMenu.addAction(
            self.tr("Install Packages"),
            self.__installPackages)
        self.__installLocalPackageAct = self.__pipMenu.addAction(
            self.tr("Install Local Package"),
            self.__installLocalPackage)
        self.__pipMenu.addSeparator()
        self.__installRequirementsAct = self.__pipMenu.addAction(
            self.tr("Install Requirements"),
            self.__installRequirements)
        self.__reinstallPackagesAct = self.__pipMenu.addAction(
            self.tr("Re-Install Selected Packages"),
            self.__reinstallPackages)
        self.__uninstallRequirementsAct = self.__pipMenu.addAction(
            self.tr("Uninstall Requirements"),
            self.__uninstallRequirements)
        self.__generateRequirementsAct = self.__pipMenu.addAction(
            self.tr("Generate Requirements..."),
            self.__generateRequirements)
        self.__pipMenu.addSeparator()
        self.__showLicensesDialogAct = self.__pipMenu.addAction(
            self.tr("Show Licenses..."),
            self.__showLicensesDialog)
        self.__pipMenu.addSeparator()
        self.__checkVulnerabilityAct = self.__pipMenu.addAction(
            self.tr("Check Vulnerabilities"),
            self.__updateVulnerabilityData)
        # updateVulnerabilityDbAct
        self.__pipMenu.addAction(
            self.tr("Update Vulnerability Database"),
            self.__updateVulnerabilityDbCache)
        self.__pipMenu.addSeparator()
        self.__cacheInfoAct = self.__pipMenu.addAction(
            self.tr("Show Cache Info..."),
            self.__showCacheInfo)
        self.__cacheShowListAct = self.__pipMenu.addAction(
            self.tr("Show Cached Files..."),
            self.__showCacheList)
        self.__cacheRemoveAct = self.__pipMenu.addAction(
            self.tr("Remove Cached Files..."),
            self.__removeCachedFiles)
        self.__cachePurgeAct = self.__pipMenu.addAction(
            self.tr("Purge Cache..."),
            self.__purgeCache)
        self.__pipMenu.addSeparator()
        # editUserConfigAct
        self.__pipMenu.addAction(
            self.tr("Edit User Configuration..."),
            self.__editUserConfiguration)
        self.__editVirtualenvConfigAct = self.__pipMenu.addAction(
            self.tr("Edit Environment Configuration..."),
            self.__editVirtualenvConfiguration)
        self.__pipMenu.addSeparator()
        # pipConfigAct
        self.__pipMenu.addAction(
            self.tr("Configure..."),
            self.__pipConfigure)

        self.__pipMenu.aboutToShow.connect(self.__aboutToShowPipMenu)
        
        self.pipMenuButton.setMenu(self.__pipMenu)
    
    def __aboutToShowPipMenu(self):
        """
        Private slot to set the action enabled status.
        """
        enable = bool(self.environmentsComboBox.currentText())
        enablePip = self.__isPipAvailable()
        enablePipCache = self.__availablePipVersion() >= (20, 1, 0)
        
        self.__installPipAct.setEnabled(not enablePip)
        self.__installPipUserAct.setEnabled(not enablePip)
        self.__repairPipAct.setEnabled(enablePip)
        
        self.__installPackagesAct.setEnabled(enablePip)
        self.__installLocalPackageAct.setEnabled(enablePip)
        self.__reinstallPackagesAct.setEnabled(enablePip)
        
        self.__installRequirementsAct.setEnabled(enablePip)
        self.__uninstallRequirementsAct.setEnabled(enablePip)
        self.__generateRequirementsAct.setEnabled(enablePip)
        
        self.__cacheInfoAct.setEnabled(enablePipCache)
        self.__cacheShowListAct.setEnabled(enablePipCache)
        self.__cacheRemoveAct.setEnabled(enablePipCache)
        self.__cachePurgeAct.setEnabled(enablePipCache)
        
        self.__editVirtualenvConfigAct.setEnabled(enable)
        
        self.__checkVulnerabilityAct.setEnabled(
            enable & self.vulnerabilityCheckBox.isEnabled())
        
        self.__showLicensesDialogAct.setEnabled(enable)
    
    @pyqtSlot()
    def __installPip(self):
        """
        Private slot to install pip into the selected environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.installPip(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __installPipUser(self):
        """
        Private slot to install pip into the user site for the selected
        environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.installPip(venvName, userSite=True)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __repairPip(self):
        """
        Private slot to repair the pip installation of the selected
        environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.repairPip(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __installPackages(self):
        """
        Private slot to install packages to be given by the user.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            from .PipPackagesInputDialog import PipPackagesInputDialog
            dlg = PipPackagesInputDialog(self, self.tr("Install Packages"))
            if dlg.exec() == QDialog.DialogCode.Accepted:
                packages, user = dlg.getData()
                self.executeInstallPackages(packages, userSite=user)
    
    @pyqtSlot()
    def __installLocalPackage(self):
        """
        Private slot to install a package available on local storage.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            from .PipFileSelectionDialog import PipFileSelectionDialog
            dlg = PipFileSelectionDialog(self, "package")
            if dlg.exec() == QDialog.DialogCode.Accepted:
                package, user = dlg.getData()
                if package and os.path.exists(package):
                    self.executeInstallPackages([package], userSite=user)
    
    @pyqtSlot()
    def __reinstallPackages(self):
        """
        Private slot to force a re-installation of the selected packages.
        """
        packages = [itm.text(PipPackagesWidget.PackageColumn)
                    for itm in self.packagesList.selectedItems()]
        venvName = self.environmentsComboBox.currentText()
        if venvName and packages:
            self.__pip.installPackages(packages, venvName=venvName,
                                       forceReinstall=True)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __installRequirements(self):
        """
        Private slot to install packages as given in a requirements file.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.installRequirements(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __uninstallRequirements(self):
        """
        Private slot to uninstall packages as given in a requirements file.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.uninstallRequirements(venvName)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def __generateRequirements(self):
        """
        Private slot to generate the contents for a requirements file.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            from .PipFreezeDialog import PipFreezeDialog
            self.__freezeDialog = PipFreezeDialog(self.__pip, self)
            self.__freezeDialog.show()
            self.__freezeDialog.start(venvName)
    
    @pyqtSlot()
    def __editUserConfiguration(self):
        """
        Private slot to edit the user configuration.
        """
        self.__editConfiguration()
    
    @pyqtSlot()
    def __editVirtualenvConfiguration(self):
        """
        Private slot to edit the configuration of the selected environment.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__editConfiguration(venvName=venvName)
    
    def __editConfiguration(self, venvName=""):
        """
        Private method to edit a configuration.
        
        @param venvName name of the environment to act upon
        @type str
        """
        from QScintilla.MiniEditor import MiniEditor
        if venvName:
            cfgFile = self.__pip.getVirtualenvConfig(venvName)
            if not cfgFile:
                return
        else:
            cfgFile = self.__pip.getUserConfig()
        cfgDir = os.path.dirname(cfgFile)
        if not cfgDir:
            EricMessageBox.critical(
                None,
                self.tr("Edit Configuration"),
                self.tr("""No valid configuration path determined."""
                        """ Aborting"""))
            return
        
        try:
            if not os.path.isdir(cfgDir):
                os.makedirs(cfgDir)
        except OSError:
            EricMessageBox.critical(
                None,
                self.tr("Edit Configuration"),
                self.tr("""No valid configuration path determined."""
                        """ Aborting"""))
            return
        
        if not os.path.exists(cfgFile):
            with contextlib.suppress(OSError), open(cfgFile, "w") as f:
                f.write("[global]\n")
        
        # check, if the destination is writeable
        if not os.access(cfgFile, os.W_OK):
            EricMessageBox.critical(
                None,
                self.tr("Edit Configuration"),
                self.tr("""No valid configuration path determined."""
                        """ Aborting"""))
            return
        
        self.__editor = MiniEditor(cfgFile, "Properties")
        self.__editor.show()
 
    def __pipConfigure(self):
        """
        Private slot to open the configuration page.
        """
        ericApp().getObject("UserInterface").showPreferences("pipPage")
    
    @pyqtSlot()
    def __showCacheInfo(self):
        """
        Private slot to show information about the cache.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.showCacheInfo(venvName)
    
    @pyqtSlot()
    def __showCacheList(self):
        """
        Private slot to show a list of cached files.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.cacheList(venvName)
    
    @pyqtSlot()
    def __removeCachedFiles(self):
        """
        Private slot to remove files from the pip cache.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.cacheRemove(venvName)
    
    @pyqtSlot()
    def __purgeCache(self):
        """
        Private slot to empty the pip cache.
        """
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            self.__pip.cachePurge(venvName)
    
    ##################################################################
    ## Interface to the vulnerability checks below
    ##################################################################
    
    @pyqtSlot(bool)
    def on_vulnerabilityCheckBox_clicked(self, checked):
        """
        Private slot handling a change of the automatic vulnerability checks.
        
        @param checked flag indicating the state of the check box
        @type bool
        """
        if checked:
            self.__updateVulnerabilityData(clearFirst=True)
    
    @pyqtSlot()
    def __clearVulnerabilityInfo(self):
        """
        Private slot to clear the vulnerability info.
        """
        for row in range(self.packagesList.topLevelItemCount()):
            itm = self.packagesList.topLevelItem(row)
            itm.setText(PipPackagesWidget.VulnerabilityColumn, "")
            itm.setToolTip(PipPackagesWidget.VulnerabilityColumn, "")
            itm.setIcon(PipPackagesWidget.VulnerabilityColumn, QIcon())
            itm.setData(PipPackagesWidget.VulnerabilityColumn,
                        PipPackagesWidget.VulnerabilityRole,
                        None)
    
    @pyqtSlot()
    def __updateVulnerabilityData(self, clearFirst=True):
        """
        Private slot to update the shown vulnerability info.
        
        @param clearFirst flag indicating to clear the vulnerability info first
            (defaults to True)
        @type bool (optional)
        """
        if clearFirst:
            self.__clearVulnerabilityInfo()
        
        packages = []
        for row in range(self.packagesList.topLevelItemCount()):
            itm = self.packagesList.topLevelItem(row)
            packages.append(Package(
                name=itm.text(PipPackagesWidget.PackageColumn),
                version=itm.text(PipPackagesWidget.InstalledVersionColumn)
            ))
        
        error, vulnerabilities = (
            self.__pip.getVulnerabilityChecker().check(packages)
        )
        if error == VulnerabilityCheckError.OK:
            for package in vulnerabilities:
                items = self.packagesList.findItems(
                    package,
                    Qt.MatchFlag.MatchExactly |
                    Qt.MatchFlag.MatchCaseSensitive
                )
                if items:
                    itm = items[0]
                    itm.setData(
                        PipPackagesWidget.VulnerabilityColumn,
                        PipPackagesWidget.VulnerabilityRole,
                        vulnerabilities[package]
                    )
                    affected = {v.spec for v in vulnerabilities[package]}
                    itm.setText(
                        PipPackagesWidget.VulnerabilityColumn,
                        ', '.join(affected)
                    )
                    itm.setIcon(
                        PipPackagesWidget.VulnerabilityColumn,
                        UI.PixmapCache.getIcon("securityLow")
                    )
        
        elif error in (VulnerabilityCheckError.FullDbUnavailable,
                       VulnerabilityCheckError.SummaryDbUnavailable):
            self.vulnerabilityCheckBox.setChecked(False)
            self.vulnerabilityCheckBox.setEnabled(False)
            self.packagesList.setColumnHidden(
                PipPackagesWidget.VulnerabilityColumn, True)
    
    @pyqtSlot()
    def __updateVulnerabilityDbCache(self):
        """
        Private slot to initiate an update of the local cache of the
        vulnerability database.
        """
        with EricOverrideCursor():
            self.__pip.getVulnerabilityChecker().updateVulnerabilityDb()
    
    def __showVulnerabilityInformation(self, packageName, packageVersion,
                                       vulnerabilities):
        """
        Private method to show the detected vulnerability data.
        
        @param packageName name of the package
        @type str
        @param packageVersion installed version number
        @type str
        @param vulnerabilities list of vulnerabilities
        @type list of Vulnerability
        """
        header = (
            self.tr("{0} {1}", "package name, package version")
            .format(packageName, packageVersion)
        )
        topItem = QTreeWidgetItem(self.infoWidget, [header])
        topItem.setFirstColumnSpanned(True)
        topItem.setExpanded(True)
        font = topItem.font(0)
        font.setBold(True)
        topItem.setFont(0, font)
        
        for vulnerability in vulnerabilities:
            title = (
                vulnerability.cve
                if vulnerability.cve else
                vulnerability.vulnerabilityId
            )
            titleItem = QTreeWidgetItem(topItem, [title])
            titleItem.setFirstColumnSpanned(True)
            titleItem.setExpanded(True)
            
            QTreeWidgetItem(
                titleItem,
                [self.tr("Affected Version:"), vulnerability.spec])
            itm = QTreeWidgetItem(
                titleItem,
                [self.tr("Advisory:"), vulnerability.advisory])
            itm.setToolTip(1, "<p>{0}</p>".format(
                vulnerability.advisory.replace("\r\n", "<br/>")
            ))
        
        self.infoWidget.scrollToTop()
        self.infoWidget.resizeColumnToContents(0)
        
        header = self.infoWidget.header()
        header.setStretchLastSection(True)
    
    #######################################################################
    ## Dependency tree related methods below
    #######################################################################
    
    @pyqtSlot(bool)
    def on_viewToggleButton_toggled(self, checked):
        """
        Private slot handling the view selection.
        
        @param checked state of the toggle button
        @type bool
        """
        if checked:
            self.viewsStackWidget.setCurrentWidget(
                self.dependenciesPage)
            self.__refreshDependencyTree()
        else:
            self.viewsStackWidget.setCurrentWidget(
                self.packagesPage)
            self.__refreshPackagesList()
    
    @pyqtSlot(bool)
    def on_requiresButton_toggled(self, checked):
        """
        Private slot handling the selection of the view type.
        
        @param checked state of the radio button (unused)
        @type bool
        """
        self.__refreshDependencyTree()
    
    @pyqtSlot()
    def on_localDepCheckBox_clicked(self):
        """
        Private slot handling the switching of the local mode.
        """
        self.__refreshDependencyTree()
    
    @pyqtSlot()
    def on_userDepCheckBox_clicked(self):
        """
        Private slot handling the switching of the 'user-site' mode.
        """
        self.__refreshDependencyTree()
    
    def __refreshDependencyTree(self):
        """
        Private method to refresh the dependency tree.
        """
        self.dependenciesList.clear()
        venvName = self.environmentsComboBox.currentText()
        if venvName:
            interpreter = self.__pip.getVirtualenvInterpreter(venvName)
            if interpreter:
                with EricOverrideCursor():
                    dependencies = self.__pip.getDependecyTree(
                        venvName,
                        localPackages=self.localDepCheckBox.isChecked(),
                        usersite=self.userDepCheckBox.isChecked(),
                        reverse=self.requiredByButton.isChecked(),
                    )
                    
                    self.dependenciesList.setUpdatesEnabled(False)
                    for dependency in dependencies:
                        self.__addDependency(dependency, self.dependenciesList)
                    
                    self.dependenciesList.sortItems(
                        PipPackagesWidget.DepPackageColumn,
                        Qt.SortOrder.AscendingOrder)
                    for col in range(self.dependenciesList.columnCount()):
                        self.dependenciesList.resizeColumnToContents(col)
                    self.dependenciesList.setUpdatesEnabled(True)
        
        self.__updateDepActionButtons()
    
    def __addDependency(self, dependency, parent):
        """
        Private method to add a dependency branch to a given parent.
        
        @param dependency dependency to be added
        @type dict
        @param parent reference to the parent item
        @type QTreeWidget or QTreeWidgetItem
        """
        itm = QTreeWidgetItem(parent, [
            dependency["package_name"],
            dependency["installed_version"],
            dependency["required_version"],
        ])
        itm.setExpanded(True)
        
        if dependency["required_version"].lower() != "any":
            spec = (
                "=={0}".format(dependency["required_version"])
                if dependency["required_version"][0] in "0123456789" else
                dependency["required_version"]
            )
            specifierSet = SpecifierSet(specifiers=spec)
            if not specifierSet.contains(dependency["installed_version"]):
                itm.setIcon(PipPackagesWidget.DepRequiredVersionColumn,
                            UI.PixmapCache.getIcon("warning"))
        
        if dependency["required_version"].lower() == "any":
            itm.setText(PipPackagesWidget.DepRequiredVersionColumn,
                        self.tr("any"))
        
        # recursively add sub-dependencies
        for dep in dependency["dependencies"]:
            self.__addDependency(dep, itm)
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_dependenciesList_itemActivated(self, item, column):
        """
        Private slot reacting on a package item of the dependency tree being
        activated.
        
        @param item reference to the activated item
        @type QTreeWidgetItem
        @param column activated column
        @type int
        """
        packageName = item.text(PipPackagesWidget.DepPackageColumn)
        packageVersion = item.text(
            PipPackagesWidget.DepInstalledVersionColumn)
        
        self.__showPackageDetails(packageName, packageVersion)
    
    @pyqtSlot()
    def on_dependenciesList_itemSelectionChanged(self):
        """
        Private slot reacting on a change of selected items of the dependency
        tree.
        """
        if len(self.dependenciesList.selectedItems()) == 0:
            self.dependencyInfoWidget.clear()
    
    @pyqtSlot(QTreeWidgetItem, int)
    def on_dependenciesList_itemPressed(self, item, column):
        """
        Private slot reacting on a package item of the dependency tree being
        pressed.
        
        @param item reference to the pressed item
        @type QTreeWidgetItem
        @param column pressed column
        @type int
        """
        self.dependencyInfoWidget.clear()
        
        if item is not None:
            self.__showPackageInformation(
                item.text(PipPackagesWidget.DepPackageColumn),
                self.dependencyInfoWidget
            )
        
        self.__updateDepActionButtons()
    
    @pyqtSlot()
    def on_refreshDependenciesButton_clicked(self):
        """
        Private slot to refresh the dependency tree.
        """
        currentEnvironment = self.environmentsComboBox.currentText()
        self.environmentsComboBox.clear()
        self.dependenciesList.clear()
        
        with EricOverrideCursor():
            self.__populateEnvironments()
            
            index = self.environmentsComboBox.findText(
                currentEnvironment,
                Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchCaseSensitive
            )
            if index != -1:
                self.environmentsComboBox.setCurrentIndex(index)
        
        self.__updateDepActionButtons()
    
    @pyqtSlot()
    def on_showDepPackageDetailsButton_clicked(self):
        """
        Private slot to show information for the selected package of the
        dependency tree.
        """
        item = self.dependenciesList.selectedItems()[0]
        if item:
            packageName = item.text(PipPackagesWidget.DepPackageColumn)
            packageVersion = item.text(
                PipPackagesWidget.DepInstalledVersionColumn)
            
            self.__showPackageDetails(packageName, packageVersion)
    
    def __updateDepActionButtons(self):
        """
        Private method to set the state of the dependency page action buttons.
        """
        self.showDepPackageDetailsButton.setEnabled(
            len(self.dependenciesList.selectedItems()) == 1 and
            self.__isPipAvailable()
        )
    
    ##################################################################
    ## Interface to show the licenses dialog below
    ##################################################################
    
    @pyqtSlot()
    def __showLicensesDialog(self):
        """
        Private slot to show a dialog with the licenses of the selected
        environment.
        """
        from .PipLicensesDialog import PipLicensesDialog
        
        environment = self.environmentsComboBox.currentText()
        localPackages = (
            self.localDepCheckBox.isChecked()
            if self.viewToggleButton.isChecked() else
            self.localCheckBox.isChecked()
        )
        usersite = (
            self.userDepCheckBox.isChecked()
            if self.viewToggleButton.isChecked() else
            self.userCheckBox.isChecked()
        )
        dlg = PipLicensesDialog(
            self.__pip,
            environment,
            localPackages=localPackages,
            usersite=usersite,
            parent=self
        )
        dlg.exec()
