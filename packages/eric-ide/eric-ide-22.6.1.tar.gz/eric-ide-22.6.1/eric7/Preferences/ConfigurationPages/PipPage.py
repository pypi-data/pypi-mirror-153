# -*- coding: utf-8 -*-

# Copyright (c) 2015 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Package implementing the pip configuration page.
"""

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_PipPage import Ui_PipPage

from PipInterface.Pip import Pip

import Preferences


class PipPage(ConfigurationPageBase, Ui_PipPage):
    """
    Class implementing the pip configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("PipPage")
        
        self.indexLabel.setText(self.tr(
            '<b>Note:</b> Leave empty to use the default index URL ('
            '<a href="{0}">{0}</a>).'
        ).format(Pip.DefaultPyPiUrl))
        self.safetyDbMirrorLabel.setText(self.tr(
            '<b>Note:</b> Leave empty to use the default Safety DB URL ({0}).'
        ).format(Preferences.Prefs.pipDefaults["VulnerabilityDbMirror"]))
        
        # set initial values
        self.indexEdit.setText(Preferences.getPip("PipSearchIndex"))
        
        safetyDbUrl = Preferences.getPip("VulnerabilityDbMirror")
        if (
            safetyDbUrl ==
            Preferences.Prefs.pipDefaults["VulnerabilityDbMirror"]
        ):
            safetyDbUrl = ""
        self.safetyDbMirrorEdit.setText(safetyDbUrl)
        self.validitySpinBox.setValue(
            Preferences.getPip("VulnerabilityDbCacheValidity") // 3600)
        # seconds converted to hours
        
        self.noCondaCheckBox.setChecked(
            Preferences.getPip("ExcludeCondaEnvironments"))
    
    def save(self):
        """
        Public slot to save the pip configuration.
        """
        safetyDbUrl = self.safetyDbMirrorEdit.text().strip()
        if not safetyDbUrl:
            safetyDbUrl = Preferences.Prefs.pipDefaults[
                "VulnerabilityDbMirror"]
        safetyDbUrl = safetyDbUrl.replace("\\", "/")
        if not safetyDbUrl.endswith("/"):
            safetyDbUrl += "/"
        
        Preferences.setPip("PipSearchIndex",
                           self.indexEdit.text().strip())
        
        Preferences.setPip("VulnerabilityDbMirror", safetyDbUrl)
        Preferences.setPip("VulnerabilityDbCacheValidity",
                           self.validitySpinBox.value() * 3600)
        # hours converted to seconds
        
        Preferences.setPip("ExcludeCondaEnvironments",
                           self.noCondaCheckBox.isChecked())


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = PipPage()
    return page
