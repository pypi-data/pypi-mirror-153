# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to select the ESP chip type and the firmware to
be flashed.
"""

import os

from PyQt6.QtCore import pyqtSlot, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from EricWidgets.EricPathPicker import EricPathPickerModes

from .Ui_EspFirmwareSelectionDialog import Ui_EspFirmwareSelectionDialog


class EspFirmwareSelectionDialog(QDialog, Ui_EspFirmwareSelectionDialog):
    """
    Class implementing a dialog to select the ESP chip type and the firmware to
    be flashed.
    """
    Chips = (
        ("", ""),
        ("ESP32", "esp32"),
        ("ESP32-C3", "esp32c3"),
        ("ESP32-S2", "esp32s2"),
        ("ESP32-S3", "esp32s3"),
        ("ESP8266", "esp8266"),
    )
    
    FlashModes = (
        ("", ""),
        ("Quad I/O", "qio"),
        ("Quad Output", "qout"),
        ("Dual I/O", "dio"),
        ("Dual Output", "dout"),
    )
    
    FlashAddresses = {
        "esp8266": "0x0000",
        "esp32": "0x1000",
        "esp32c3": "0x0000",
        "esp32s2": "0x1000",
        "esp32s3": "0x0000",
    }
    
    def __init__(self, addon=False, parent=None):
        """
        Constructor
        
        @param addon flag indicating an addon firmware
        @type bool
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.__addon = addon
        
        self.firmwarePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.firmwarePicker.setFilters(
            self.tr("Firmware Files (*.bin);;All Files (*)"))
        
        for text, chip in self.Chips:
            self.espComboBox.addItem(text, chip)
        
        self.baudRateComboBox.addItems([
            "74.880", "115.200", "230.400", "460.800", "921.600", "1.500.000"])
        self.baudRateComboBox.setCurrentIndex(3)
        
        for text, mode in self.FlashModes:
            self.modeComboBox.addItem(text, mode)
        
        if addon:
            self.__validator = QRegularExpressionValidator(
                QRegularExpression(r"[0-9a-fA-F]{0,7}")
            )
            self.addressEdit.setValidator(self.__validator)
        else:
            self.addressLabel.hide()
            self.addressEdit.hide()
        
        msh = self.minimumSizeHint()
        self.resize(max(self.width(), msh.width()), msh.height())
    
    def __updateOkButton(self):
        """
        Private method to update the state of the OK button.
        """
        firmwareFile = self.firmwarePicker.text()
        enable = (bool(self.espComboBox.currentText()) and
                  bool(firmwareFile) and os.path.exists(firmwareFile))
        if self.__addon:
            enable &= bool(self.addressEdit.text())
        self.buttonBox.button(
            QDialogButtonBox.StandardButton.Ok).setEnabled(enable)
    
    @pyqtSlot(str)
    def on_espComboBox_currentTextChanged(self, chip):
        """
        Private slot to handle the selection of a chip type.
        
        @param chip selected chip type
        @type str
        """
        self.__updateOkButton()
    
    @pyqtSlot(str)
    def on_firmwarePicker_textChanged(self, firmware):
        """
        Private slot handling a change of the firmware path.
        
        @param firmware path to the firmware
        @type str
        """
        self.__updateOkButton()
    
    @pyqtSlot(str)
    def on_addressEdit_textChanged(self, address):
        """
        Private slot handling a change of the address.
        
        @param address entered address
        @type str
        """
        self.__updateOkButton()
    
    def getData(self):
        """
        Public method to get the entered data.
        
        @return tuple containing the selected chip type, the path of the
            firmware file, the baud rate, the flash mode and the flash
            address
        @rtype tuple of (str, str, str, str, str)
        """
        chip = self.espComboBox.currentData()
        address = (
            self.addressEdit.text()
            if self.__addon else
            self.FlashAddresses[chip])
        
        return (
            chip,
            self.firmwarePicker.text(),
            self.baudRateComboBox.currentText().replace(".", ""),
            self.modeComboBox.currentData(),
            address,
        )
