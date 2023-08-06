# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2019 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing the Interface configuration page (variant for web browser).
"""

import glob
import os

from PyQt6.QtCore import QTranslator
from PyQt6.QtWidgets import QStyleFactory

from EricWidgets.EricPathPicker import EricPathPickerModes
from EricWidgets.EricApplication import ericApp

from .ConfigurationPageBase import ConfigurationPageBase
from .Ui_InterfaceLightPage import Ui_InterfaceLightPage

import Preferences
import Utilities

from eric7config import getConfig


class InterfaceLightPage(ConfigurationPageBase, Ui_InterfaceLightPage):
    """
    Class implementing the Interface configuration page (variant for generic
    use).
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.setupUi(self)
        self.setObjectName("InterfacePage")
        
        self.styleSheetPicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.styleSheetPicker.setFilters(self.tr(
            "Qt Style Sheets (*.qss);;Cascading Style Sheets (*.css);;"
            "All files (*)"))
        self.styleSheetPicker.setDefaultDirectory(getConfig("ericStylesDir"))
        
        styleIconsPath = ericApp().getStyleIconsPath()
        self.styleIconsPathPicker.setMode(
            EricPathPickerModes.DIRECTORY_SHOW_FILES_MODE)
        self.styleIconsPathPicker.setDefaultDirectory(styleIconsPath)
        
        # set initial values
        self.__populateStyleCombo()
        self.__populateLanguageCombo()
        
        self.styleSheetPicker.setText(Preferences.getUI("StyleSheet"))
        self.styleIconsPathPicker.setText(Preferences.getUI("StyleIconsPath"))
    
    def save(self):
        """
        Public slot to save the Interface configuration.
        """
        # save the style settings
        styleIndex = self.styleComboBox.currentIndex()
        style = self.styleComboBox.itemData(styleIndex)
        Preferences.setUI("Style", style)
        Preferences.setUI(
            "StyleSheet",
            self.styleSheetPicker.text())
        Preferences.setUI(
            "StyleIconsPath",
            self.styleIconsPathPicker.text())
        
        # save the language settings
        uiLanguageIndex = self.languageComboBox.currentIndex()
        uiLanguage = (
            self.languageComboBox.itemData(uiLanguageIndex)
            if uiLanguageIndex else
            None
        )
        Preferences.setUILanguage(uiLanguage)
    
    def __populateStyleCombo(self):
        """
        Private method to populate the style combo box.
        """
        curStyle = Preferences.getUI("Style")
        styles = sorted(QStyleFactory.keys())
        self.styleComboBox.addItem(self.tr('System'), "System")
        for style in styles:
            self.styleComboBox.addItem(style, style)
        currentIndex = self.styleComboBox.findData(curStyle)
        if currentIndex == -1:
            currentIndex = 0
        self.styleComboBox.setCurrentIndex(currentIndex)
    
    def __populateLanguageCombo(self):
        """
        Private method to initialize the language combo box.
        """
        self.languageComboBox.clear()
        
        fnlist = (
            glob.glob("eric7_*.qm") +
            glob.glob(os.path.join(
                getConfig('ericTranslationsDir'), "eric7_*.qm")) +
            glob.glob(os.path.join(Utilities.getConfigDir(), "eric7_*.qm"))
        )
        locales = {}
        for fn in fnlist:
            locale = os.path.basename(fn)[6:-3]
            if locale not in locales:
                translator = QTranslator()
                translator.load(fn)
                locales[locale] = (
                    translator.translate(
                        "InterfacePage", "English",
                        "Translate this with your language") +
                    " ({0})".format(locale)
                )
        localeList = sorted(locales.keys())
        try:
            uiLanguage = Preferences.getUILanguage()
            if uiLanguage == "None" or uiLanguage is None:
                currentIndex = 0
            elif uiLanguage == "System":
                currentIndex = 1
            else:
                currentIndex = localeList.index(uiLanguage) + 2
        except ValueError:
            currentIndex = 0
        self.languageComboBox.clear()
        
        self.languageComboBox.addItem("English (default)", "None")
        self.languageComboBox.addItem(self.tr('System'), "System")
        for locale in localeList:
            self.languageComboBox.addItem(locales[locale], locale)
        self.languageComboBox.setCurrentIndex(currentIndex)


def create(dlg):
    """
    Module function to create the configuration page.
    
    @param dlg reference to the configuration dialog
    @return reference to the instantiated page (ConfigurationPageBase)
    """
    page = InterfaceLightPage()
    return page
