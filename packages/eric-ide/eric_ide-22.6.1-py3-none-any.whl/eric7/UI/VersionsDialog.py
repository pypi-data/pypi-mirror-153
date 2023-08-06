# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show the versions of various components.
"""

import sys

from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from EricGui.EricOverrideCursor import EricOverrideCursor
from EricWidgets.EricApplication import ericApp
from EricWidgets import EricMessageBox

from .Ui_VersionsDialog import Ui_VersionsDialog


class VersionsDialog(QDialog, Ui_VersionsDialog):
    """
    Class implementing a dialog to show the versions of various components.
    """
    def __init__(self, parent, title, text):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type UserInterface
        @param title dialog title
        @type str
        @param text versions text to be shown
        @type str
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__ui = parent
        icon = QGuiApplication.windowIcon().pixmap(64, 64)
        
        self.setWindowTitle(title)
        self.iconLabel.setPixmap(icon)
        self.textLabel.setText(text)
        
        self.__checkUpdateButton = self.buttonBox.addButton(
            self.tr("Check for Upgrades..."),
            QDialogButtonBox.ButtonRole.ActionRole
        )
        self.__checkUpdateButton.clicked.connect(self.__checkForUpdate)
        
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setDefault(True)
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setFocus(
                Qt.FocusReason.OtherFocusReason)
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
        
        self.exec()
    
    @pyqtSlot()
    def __checkForUpdate(self):
        """
        Private slot to check, if updates of PyQt6 packages or the eric-ide
        package are available.
        """
        msg = ""
        
        pip = ericApp().getObject("Pip")
        venvManager = ericApp().getObject("VirtualEnvManager")
        
        environmentName = (
            venvManager.environmentForInterpreter(sys.executable)[0]
            # just the name is needed
        )
        
        if environmentName:
            with EricOverrideCursor():
                pyqtUpdateAvailable = pip.checkPackageOutdated(
                    "pyqt6", environmentName)[0]
                ericUpdateAvailable = pip.checkPackageOutdated(
                    "eric-ide", environmentName)[0]
            
            if pyqtUpdateAvailable or ericUpdateAvailable:
                self.buttonBox.removeButton(self.__checkUpdateButton)
                self.__checkUpdateButton = None
            else:
                msg = self.tr("No upgrades available.")
            
            if ericUpdateAvailable:
                self.__upgradeEricButton = self.buttonBox.addButton(
                    self.tr("Upgrade eric7..."),
                    QDialogButtonBox.ButtonRole.ActionRole
                )
                self.__upgradeEricButton.clicked.connect(self.__ui.upgradeEric)
                msg += self.tr(
                    "<p>An upgrade of <b>eric7</b> is available.</p>")
            
            if pyqtUpdateAvailable:
                self.__upgradePyQtButton = self.buttonBox.addButton(
                    self.tr("Upgrade PyQt6..."),
                    QDialogButtonBox.ButtonRole.ActionRole
                )
                self.__upgradePyQtButton.clicked.connect(self.__ui.upgradePyQt)
                msg += self.tr(
                    "<p>An upgrade of <b>PyQt6</b> is available.</p>")
            
            if ericUpdateAvailable and pyqtUpdateAvailable:
                self.__upgradeBothButton = self.buttonBox.addButton(
                    self.tr("Upgrade Both..."),
                    QDialogButtonBox.ButtonRole.ActionRole
                )
                self.__upgradeBothButton.clicked.connect(
                    self.__ui.upgradeEricPyQt)
            
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Ok).setDefault(True)
            self.buttonBox.button(
                QDialogButtonBox.StandardButton.Ok).setFocus(
                    Qt.FocusReason.OtherFocusReason)
            
            EricMessageBox.information(
                self,
                self.tr("Check for Upgrades"),
                msg
            )
