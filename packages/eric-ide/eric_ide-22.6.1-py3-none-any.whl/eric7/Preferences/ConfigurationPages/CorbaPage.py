# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Corba configuration page.
"""

from EricWidgets.EricPathPicker import EricPathPickerModes

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_CorbaPage import Ui_CorbaPage

import Preferences


class CorbaPage(ConfigurationPageBase, Ui_CorbaPage):
    """
    Class implementing the Corba configuration page.
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("CorbaPage")
        
        self.idlPicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.idlPicker.setToolTip(self.tr(
            "Press to select the IDL compiler via a file selection dialog."))
        
        # set initial values
        self.idlPicker.setText(Preferences.getCorba("omniidl"))
        
    def save(self):
        """
        Public slot to save the Corba configuration.
        """
        Preferences.setCorba("omniidl", self.idlPicker.text())
    

def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = CorbaPage()
    return page
