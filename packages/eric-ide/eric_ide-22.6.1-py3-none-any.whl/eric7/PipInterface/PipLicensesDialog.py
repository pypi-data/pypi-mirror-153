# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the licenses of an environment.
"""

import os
import re

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QTreeWidgetItem

from EricGui.EricOverrideCursor import EricOverrideCursor
from EricWidgets import EricFileDialog, EricMessageBox

from .Ui_PipLicensesDialog import Ui_PipLicensesDialog


class PipLicensesDialog(QDialog, Ui_PipLicensesDialog):
    """
    Class implementing a dialog to show the licenses of an environment.
    """
    LicensesPackageColumn = 0
    LicensesVersionColumn = 1
    LicensesLicenseColumn = 2
    
    SummaryCountColumn = 0
    SummaryLicenseColumn = 1
    
    def __init__(self, pip, environment, localPackages=True, usersite=False,
                 parent=None):
        """
        Constructor
        
        @param pip reference to the pip interface object
        @type Pip
        @param environment name of the environment to show the licenses for
        @type str
        @param localPackages flag indicating to show the licenses for local
            packages only
        @type bool
        @param usersite flag indicating to show the licenses for packages
            installed in user-site directory only
        @type bool
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__pip = pip
        self.__environment = environment
        
        self.__allFilter = self.tr("<All>")
        
        self.__saveCSVButton = self.buttonBox.addButton(
            self.tr("Save as CSV..."), QDialogButtonBox.ButtonRole.ActionRole)
        self.__saveCSVButton.clicked.connect(self.__saveAsCSV)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Close).setDefault(True)
        
        self.localCheckBox.setChecked(localPackages)
        self.userCheckBox.setChecked(usersite)
        
        self.localCheckBox.toggled.connect(self.__refreshLicenses)
        self.userCheckBox.toggled.connect(self.__refreshLicenses)
        
        if environment:
            self.environmentLabel.setText("<b>{0}</b>".format(
                self.tr('Licenses of "{0}"').format(environment)
            ))
        else:
            # That should never happen; play it safe.
            self.environmentLabel.setText(self.tr("No environment specified."))
        
        self.licenseFilterComboBox.currentTextChanged.connect(
            self.__filterPackagesByLicense)
        
        self.__refreshLicenses()
        
    @pyqtSlot()
    def __refreshLicenses(self):
        """
        Private slot to refresh the license lists.
        """
        with EricOverrideCursor():
            self.licensesList.clear()
            self.summaryList.clear()
            self.licenseFilterComboBox.clear()
            
            licensesForFilter = set()
            
            # step 1: show the licenses per package
            self.licensesList.setUpdatesEnabled(False)
            licenses = self.__pip.getLicenses(
                self.__environment,
                localPackages=self.localCheckBox.isChecked(),
                usersite=self.userCheckBox.isChecked(),
            )
            for lic in licenses:
                QTreeWidgetItem(self.licensesList, [
                    lic["Name"],
                    lic["Version"],
                    lic["License"].replace("; ", "\n"),
                ])
            
            self.licensesList.sortItems(
                PipLicensesDialog.LicensesPackageColumn,
                Qt.SortOrder.AscendingOrder)
            for col in range(self.licensesList.columnCount()):
                self.licensesList.resizeColumnToContents(col)
            self.licensesList.setUpdatesEnabled(True)
            
            # step 2: show the licenses summary
            self.summaryList.setUpdatesEnabled(False)
            licenses = self.__pip.getLicensesSummary(
                self.__environment,
                localPackages=self.localCheckBox.isChecked(),
                usersite=self.userCheckBox.isChecked(),
            )
            for lic in licenses:
                QTreeWidgetItem(self.summaryList, [
                    "{0:4d}".format(lic["Count"]),
                    lic["License"].replace("; ", "\n"),
                ])
                licensesForFilter |= set(lic["License"].split("; "))
            
            self.summaryList.sortItems(
                PipLicensesDialog.SummaryLicenseColumn,
                Qt.SortOrder.AscendingOrder)
            for col in range(self.summaryList.columnCount()):
                self.summaryList.resizeColumnToContents(col)
            self.summaryList.setUpdatesEnabled(True)
            
            self.licenseFilterComboBox.addItems(
                [self.__allFilter] + sorted(licensesForFilter))
        
        enable = bool(self.licensesList.topLevelItemCount())
        self.__saveCSVButton.setEnabled(enable)
    
    @pyqtSlot(str)
    def __filterPackagesByLicense(self, licenseName):
        """
        Private slot to filter the list of packages by license.
        
        @param licenseName license name
        @type str
        """
        pattern = r"\b{0}".format(re.escape(licenseName))
        if not licenseName.endswith((")", "]", "}")):
            pattern += r"\b"
        regexp = re.compile(pattern)
        for row in range(self.licensesList.topLevelItemCount()):
            itm = self.licensesList.topLevelItem(row)
            if licenseName == self.__allFilter:
                itm.setHidden(False)
            else:
                itm.setHidden(
                    regexp.search(
                        itm.text(PipLicensesDialog.LicensesLicenseColumn)
                    ) is None
                )
    
    @pyqtSlot()
    def __saveAsCSV(self):
        """
        Private slot to save the license information as a CSV file.
        """
        import csv
        
        fileName, selectedFilter = EricFileDialog.getSaveFileNameAndFilter(
            self,
            self.tr("Save as CSV"),
            os.path.expanduser("~"),
            self.tr("CSV Files (*.csv);;All Files (*)"),
            None,
            EricFileDialog.DontConfirmOverwrite
        )
        if fileName:
            ext = os.path.splitext(fileName)[1]
            if not ext:
                ex = selectedFilter.split("(*")[1].split(")")[0]
                if ex:
                    fileName += ex
            
            try:
                with open(fileName, "w", newline="",
                          encoding="utf-8") as csvFile:
                    fieldNames = ["Name", "Version", "License"]
                    writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
                    
                    writer.writeheader()
                    for row in range(self.licensesList.topLevelItemCount()):
                        itm = self.licensesList.topLevelItem(row)
                        writer.writerow({
                            "Name": itm.text(0),
                            "Version": itm.text(1),
                            "License": itm.text(2),
                        })
            except OSError as err:
                EricMessageBox.critical(
                    self,
                    self.tr("Save as CSV"),
                    self.tr(
                        """<p>The license information could not be saved"""
                        """ into the CSV file <b>{0}</b>.</p>"""
                        """<p>Reason: {1}</p>"""
                    ).format(fileName, str(err))
                )
