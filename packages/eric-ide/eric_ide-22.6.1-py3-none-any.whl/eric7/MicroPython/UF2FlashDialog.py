# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to flash any UF2 capable device.
"""

import os
import shutil
import contextlib

from PyQt6.QtCore import pyqtSlot, Qt, QCoreApplication, QThread, QEventLoop
from PyQt6.QtWidgets import QDialog

from EricWidgets.EricPathPicker import EricPathPickerModes
from EricWidgets.EricApplication import ericApp

from .Ui_UF2FlashDialog import Ui_UF2FlashDialog

import UI.PixmapCache
import Utilities

from . import MicroPythonDevices

SupportedUF2Boards = {
    "circuitpython": {
        "volumes": {
            (0x03EB, 0x2402): [
                "SAMD21",         # SAMD21 Board
                "SAME54",         # SAME54 Board
            ],
            (0x04D8, 0xEC44): [
                "PYCUBEDBOOT",    # PyCubedv04
            ],
            (0x04D8, 0xEC63): [
                "BOOT",           # CircuitBrains Basic
            ],
            (0x04D8, 0xEC64): [
                "BOOT",           # CircuitBrains Deluxe
            ],
            (0x04D8, 0xED5F): [
                "UCHIPYBOOT",     # uChip CircuitPython
            ],
            (0x04D8, 0xEDB3): [
                "USBHUBBOOT",     # Programmable USB Hub
            ],
            (0x04D8, 0xEDBE): [
                "SAM32BOOT",      # SAM32
            ],
            (0x04D8, 0xEF66): [
                "SENSEBOX",       # senseBox MCU
            ],
            (0x1209, 0x2017): [
                "MINISAMBOOT",    # Mini SAM M4
            ],
            (0x1209, 0x3252): [
                "MCBS2OMBOOT",    # Module Clip w/Wroom
            ],
            (0x1209, 0x3253): [
                "MCBS2ERBOOT",    # Module Clip w/Wrover
            ],
            (0x1209, 0x4D44): [
                "ROBOM0BOOT",     # Robo HAT MM1
                "ROBOM4BOOT",     # Robo HAT MM1 M4
            ],
            (0x1209, 0x4DDD): [
                "SapBOOT",        # CP Sapling
            ],
            (0x1209, 0x7102): [
                "MINISAMBOOT",    # Mini SAM M0
            ],
            (0x1209, 0x7A01): [
                "MIKOTO-BOOT",    # Mikoto nRF52840
            ],
            (0x1209, 0x805A): [
                "BASTBLE",        # Bast BLE
            ],
            (0x1209, 0xE3E2): [
                "StackRduino",    # StackRduino M0 PRO
            ],
            (0x1209, 0xF501): [
                "M4SHIMBOOT",     # M4-Shim
            ],
            (0x15BA, 0x28DC): [
                "OLMLIPOBOOT",    # ESP32S2 DevKit Lipo
            ],
            (0x16D0, 0x0CDA): [
                "AUTOMAT",        # automat
            ],
            (0x1B4F, 0x0022): [
                "SFMM852BOOT",    # MicroMod nRF52840
            ],
            (0x1B4F, 0x002C): [
                "THNG+32BOOT",    # Thing Plus - STM32
            ],
            (0x1B4F, 0x0D22): [
                "SPARKFUN",       # SAMD21 Mini Breakout
            ],
            (0x1B4F, 0x0D23): [
                "SPARKFUN",       # SAMD21 Dev Breakout
            ],
            (0x1D50, 0x6110): [
                "ROBOTICS",       # Robotics
            ],
            (0x1D50, 0x6112): [
                "RCBOOT",         # Wattuino RC
            ],
            (0x1D50, 0x6157): [
                "BBOARDBOOT",     # nRF52840 BBoard
            ],
            (0x1D50, 0x6160): [
                "BLUEMICRO",      # BlueMicro
            ],
            (0x1D50, 0x616F): [
                "BLUEMICRO",      # BlueMicro
            ],
            (0x1FC9, 0x0094): [
                "DblM33BOOT",     # Double M33
                "LPC5528BOOT",    # LPCXpresso 55s28
                "LPC5569BOOT",    # LPCXpresso 55s69
            ],
            (0x1FC9, 0x0154): [
                "K32L2BOOT",      # FRDM-K32L2B3
                "K32L2BOOT",      # KUIIC
            ],
            (0x230A, 0x00E9): [
                "TAU_BOOT",       # Tau
            ],
            (0x2341, 0x0057): [
                "NANOBOOT",       # NANO 33 IoT
            ],
            (0x2341, 0x8053): [
                "MKR1300",        # MKR1300
            ],
            (0x239A, 0x000F): [
                "ITSYBOOT",       # ItsyBitsy M0 Express
            ],
            (0x239A, 0x0013): [
                "METROBOOT",      # Metro M0
            ],
            (0x239A, 0x0015): [
                "FEATHERBOOT",    # Feather M0
            ],
            (0x239A, 0x0018): [
                "CPLAYBOOT",      # CPlay Express
            ],
            (0x239A, 0x001B): [
                "FEATHERBOOT",    # Feather M0 Express
            ],
            (0x239A, 0x001C): [
                "GEMMABOOT",      # Gemma M0
            ],
            (0x239A, 0x001E): [
                "TRINKETBOOT",    # Trinket M0
            ],
            (0x239A, 0x0021): [
                "METROM4BOOT",    # Metro M4 Express
            ],
            (0x239A, 0x0022): [
                "ARCADE-D5",      # Feather Arcade D51
                "FEATHERBOOT",    # Feather M4 Express
            ],
            (0x239A, 0x0024): [
                "RADIOBOOT",      # Radiofruit M0
            ],
            (0x239A, 0x0027): [
                "PIRKEYBOOT",     # pIRKey M0
            ],
            (0x239A, 0x0029): [
                "ARGONBOOT  ",    # Argon
                "BORONBOOT  ",    # Boron
                "FTHR840BOOT",    # Feather nRF52840 Express
                "MDK840DONGL",    # MDK nRF52840 USB Dongle
                "WS52840EVK",     # Waveshare nRF52840 Eval
                "XENONBOOT  ",    # Xenon
            ],
            (0x239A, 0x002B): [
                "ARCADE-D5",      # Itsy Arcade D51
                "ITSYM4BOOT",     # ItsyBitsy M4 Express
            ],
            (0x239A, 0x002D): [
                "CRICKITBOOT",    # crickit
            ],
            (0x239A, 0x002F): [
                "TRELM4BOOT",     # Trellis M4 Express
            ],
            (0x239A, 0x0031): [
                "GCM4BOOT",       # Grand Central M4 Express
            ],
            (0x239A, 0x0033): [
                "PYBADGEBOOT",    # PyBadge
            ],
            (0x239A, 0x0034): [
                "BADGELCBOOT",    # BadgeLC
                "PEWBOOT",        # PewPew
            ],
            (0x239A, 0x0035): [
                "MKRZEROBOOT",    # MKRZero
                "PORTALBOOT",     # PyPortal M4 Express
            ],
            (0x239A, 0x0037): [
                "METROM4BOOT",    # Metro M4 AirLift
            ],
            (0x239A, 0x003D): [
                "PYGAMERBOOT",    # PyGamer
            ],
            (0x239A, 0x003F): [
                "METR840BOOT",    # Metro nRF52840 Express
            ],
            (0x239A, 0x0045): [
                "CPLAYBTBOOT",    # Circuit Playground nRF52840
            ],
            (0x239A, 0x0047): [
                "MASKM4BOOT",     # Hallowing Mask M4
            ],
            (0x239A, 0x0049): [
                "HALLOM4BOOT",    # HalloWing M4
            ],
            (0x239A, 0x004D): [
                "SNEKBOOT",       # snekboard
            ],
            (0x239A, 0x0051): [
                "ITSY840BOOT",    # ItsyBitsy nRF52840 Express
            ],
            (0x239A, 0x0057): [
                "SERPENTBOOT",    # Serpente
            ],
            (0x239A, 0x0059): [
                "FTHR405BOOT",    # Feather STM32F405 Express
            ],
            (0x239A, 0x005D): [
                "BlackPill",      # STM32F401CxUx
                "STMF411BOOT",    # STM32F411 Discovery
            ],
            (0x239A, 0x0061): [
                "SOLBOOT",        # Sol
            ],
            (0x239A, 0x0063): [
                "NANO33BOOT",     # Nano 33 BLE
            ],
            (0x239A, 0x0065): [
                "ND6BOOT",        # ndBit6
            ],
            (0x239A, 0x0069): [
                "STMF411BOOT",    # STM32F411 BlackPill
            ],
            (0x239A, 0x006B): [
                "shIRtty",        # shIRtty
            ],
            (0x239A, 0x0071): [
                "CLUEBOOT",       # CLUE nRF52840
            ],
            (0x239A, 0x0077): [
                "RT1010BOOT",     # RT1010 EVK
            ],
            (0x239A, 0x0079): [
                "ARAMBOOT",       # ARAMCON Badge 2019
            ],
            (0x239A, 0x007B): [
                "ARAMBOOT",       # ARAMCON2 Badge
            ],
            (0x239A, 0x007D): [
                "BOOKBOOT",       # The Open Book Feather
            ],
            (0x239A, 0x007F): [
                "BADGEBOOT",      # OHS2020 Badge
            ],
            (0x239A, 0x0081): [
                "RT1020BOOT",     # RT1020 EVK
                "RT1024BOOT",     # RT1024 EVK
            ],
            (0x239A, 0x0083): [
                "RT1060BOOT",     # RT1060 EVK
                "RT1064BOOT",     # RT1064 EVK
            ],
            (0x239A, 0x0087): [
                "FTHRSNSBOOT",    # Feather nRF52840 Sense
            ],
            (0x239A, 0x0093): [
                "ISVITABoot",     # IkigaiSense Vita nRF52840
            ],
            (0x239A, 0x0095): [
                "UARTLOGBOOT",    # UARTLogger II
            ],
            (0x239A, 0x009F): [
                "ADM840BOOT",     # AtelierDuMaker NRF52840 Breakout
            ],
            (0x239A, 0x00A5): [
                "S3DKC1BOOT",     # ESP32S3 DevKitC 1
                "S3DKM1BOOT",     # ESP32S3 DevKitM 1
                "SAOLA1RBOOT",    # Saola 1R WROVER
            ],
            (0x239A, 0x00A7): [
                "SAOLA1MBOOT",    # Saola 1M WROOM
            ],
            (0x239A, 0x00AB): [
                "UFTHRS2BOOT",    # FeatherS2
            ],
            (0x239A, 0x00AF): [
                "FLUFFBOOT",      # Fluff M0
            ],
            (0x239A, 0x00B3): [
                "NICENANO",       # nice!nano
            ],
            (0x239A, 0x00B5): [
                "E54XBOOT",       # SAME54 Xplained
            ],
            (0x239A, 0x00B9): [
                "ND7BOOT",        # ndBit7
            ],
            (0x239A, 0x00BB): [
                "MDBT50QBOOT",    # Raytac MDBT50Q Demo Board 40
            ],
            (0x239A, 0x00BF): [
                "BADGEBOOT",      # BLM Badge
            ],
            (0x239A, 0x00C3): [
                "GEMINIBOOT",     # Gemini
            ],
            (0x239A, 0x00C5): [
                "MICROS2BOOT",    # microS2
            ],
            (0x239A, 0x00C7): [
                "KALUGA1BOOT",    # Kaluga 1
            ],
            (0x239A, 0x00C9): [
                "MATRIXBOOT",     # Matrix Portal M4
            ],
            (0x239A, 0x00CB): [
                "QTPY_BOOT",      # QT Py M0
            ],
            (0x239A, 0x00CD): [
                "FTHRCANBOOT",    # Feather M4 CAN Express
            ],
            (0x239A, 0x00DE): [
                "NANOESPBOOT",    # nanoESP32-S2 WROOM
            ],
            (0x239A, 0x00DF): [
                "METROS2BOOT",    # Metro ESP32-S2
            ],
            (0x239A, 0x00E1): [
                "METROM7BOOT",    # Metro M7 iMX RT1011
            ],
            (0x239A, 0x00E5): [
                "MAGTAGBOOT",     # Metro MagTag 2.9 Grayscale
                "MAGTAGBOOT",     # MagTag 2.9 Grayscale
            ],
            (0x239A, 0x00EB): [
                "FTHRS2BOOT",     # Feather ESP32-S2
            ],
            (0x239A, 0x00ED): [
                "FTHRS2BOOT",     # Feather ESP32-S2 Reverse TFT
            ],
            (0x239A, 0x00EF): [
                "TRINKEYBOOT",    # NeoPixel Trinkey M0
            ],
            (0x239A, 0x00F5): [
                "STARBOOT",       # Binary Star
            ],
            (0x239A, 0x00F9): [
                "HOUSEBOOT",      # FunHouse
            ],
            (0x239A, 0x00FB): [
                "TRINKEYBOOT",    # Rotary Trinkey M0
            ],
            (0x239A, 0x00FF): [
                "TRINKEYBOOT",    # NeoKey Trinkey M0
            ],
            (0x239A, 0x0101): [
                "TRINKEYBOOT",    # Slide Trinkey M0
            ],
            (0x239A, 0x0103): [
                "TRINKEYBOOT",    # ProxSense Trinkey M0
            ],
            (0x239A, 0x010B): [
                "MDBT50QBOOT",    # Raytac MDBT50Q-RX
            ],
            (0x239A, 0x010D): [
                "GLASSESBOOT",    # LED Glasses Driver nRF52840
            ],
            (0x239A, 0x010F): [
                "FTHRS2BOOT",     # Feather ESP32-S2 TFT
            ],
            (0x239A, 0x0111): [
                "QTPYS2BOOT",     # QT Py ESP32-S2
            ],
            (0x239A, 0x0113): [
                "FTHRS3BOOT",     # Feather ESP32-S3 No PSRAM
            ],
            (0x239A, 0x0115): [
                "FEATHERBOOT",    # Feather M4 Adalogger
            ],
            (0x239A, 0x0117): [
                "CAMERABOOT",     # Camera
            ],
            (0x239A, 0x0119): [
                "QTPYS3BOOT",     # QT Py ESP32-S3
            ],
            (0x239A, 0x800B): [
                "ATMZBOOT",       # ATMegaZero ESP32-S2
            ],
            (0x239A, 0xB000): [
                "HALLOWBOOT",     # Hallowing M0
            ],
            (0x239A, 0xE005): [
                "HONKBOOT",       # Big Honking Button
            ],
            (0x2886, 0x000D): [
                "Grove Zero",     # Grove Zero
            ],
            (0x2886, 0x002F): [
                "Seeed XIAO",     # Seeeduino XIAO
            ],
            (0x2886, 0xF00E): [
                "PITAYAGO",       # Pitaya Go
            ],
            (0x2886, 0xF00F): [
                "M60KEYBOARD",    # MakerDiary M60 Mechanical Keyboard
                "nRF52840M2",     # MakerDiary nRF52840 M.2 Module
            ],
            (0x303A, 0x7000): [
                "ESPHMI1BOOT",    # HMI 1
            ],
            (0x303A, 0x8005): [
                "TINYS2BOOT",     # TinyS2
            ],
            (0x303A, 0x8008): [
                "TTGOS2BOOT",     # TTGO_T8_S2_Display
            ],
            (0x303A, 0x800E): [
                "CCMBRISBOOT",    # CucumberRIS v1.1
            ],
            (0x303A, 0x80B0): [
                "RD00RBOOT",      # Reference Design RD00
            ],
            (0x303A, 0x80B3): [
                "NANOESPBOOT",    # nanoESP32-S2 WROVER
            ],
            (0x303A, 0x80B5): [
                "FS2NEOBOOT",     # FeatherS2 Neo
            ],
            (0x303A, 0x80B6): [
                "MORPHBOOT",      # MORPHESP-240
            ],
            (0x303A, 0x80C4): [
                "S2MINIBOOT",     # S2 Mini
            ],
            (0x303A, 0x80C7): [
                "S2PICOBOOT",     # S2 Pico
            ],
            (0x303A, 0x80D2): [
                "TINYS3BOOT",     # TinyS3
            ],
            (0x303A, 0x80D5): [
                "PROS3BOOT",      # ProS3
            ],
            (0x303A, 0x80D8): [
                "UFTHRS3BOOT",    # FeatherS3
            ],
            (0x303A, 0x80DA): [
                "HEXKYBOOT",      # HexKy-S2
            ],
            (0x303A, 0x80DE): [
                "LEAFS3BOOT",     # BPI-Leaf-S3
            ],
            (0x303A, 0x80E1): [
                "LEAFS2BOOT",     # BPI-Leaf-S2
            ],
            (0x303A, 0x80E4): [
                "BITS2BOOT",      # BPI-BIT-S2
            ],
            (0x303A, 0x80EB): [
                "TTGOS2BOOT",     # TTGO_T8_S2_WROOM
            ],
            (0x303A, 0x80EE): [
                "TTGOS2BOOT",     # TTGO_T8_S2
            ],
            (0x3171, 0x0100): [
                "CMDBOOT",        # COMMANDER
            ],
            (0x80E7, 0x8111): [
                "IOTS2BOOT",      # HiiBot IoTs2
            ],
            (0xCAFE, 0xFFFF): [
                "F303BOOT",       # STM32F303 Discovery
            ],
        },
        "instructions": QCoreApplication.translate(
            "UF2FlashDialog",
            "<h3>CircuitPython Board</h3>"
            "<p>In order to prepare the board for flashing follow these"
            " steps:</p><ol>"
            "<li>Switch your device to 'bootloader' mode by double-pressing"
            " the reset button.</li>"
            "<li>Wait until the device has entered 'bootloader' mode.</li>"
            "<li>(If this does not happen, then try shorter or longer"
            " pauses between presses.)</li>"
            "<li>Ensure the boot volume is available (this may require"
            " mounting it).</li>"
            "<li>Select the firmware file to be flashed and click the"
            " flash button.</li>"
            "</ol>"
        ),
        "show_all": True,
        "firmware": "CircuitPython",
    },
    
    "circuitpython_rp2040": {
        "volumes": {
            (0x239A, 0x80F4): [
                "RPI-RP2",        # Raspberry Pi Pico loaded with CircuitPython
            ],
        },
        "instructions": QCoreApplication.translate(
            "UF2FlashDialog",
            "<h3>Pi Pico (RP2040) Board</h3>"
            "<p>In order to prepare the board for flashing follow these"
            " steps:</p><ol>"
            "<li>Enter 'bootloader' mode (board <b>without</b> RESET button):"
            "<ul>"
            "<li>Plug in your board while holding the BOOTSEL button.</li>"
            "</ul>"
            "Enter 'bootloader' mode (board <b>with</b> RESET button):"
            "<ul>"
            "<li>hold down RESET</li>"
            "<li>hold down BOOTSEL</li>"
            "<li>release RESET</li>"
            "<li>release BOOTSEL</li>"
            "</ul></li>"
            "<li>Wait until the device has entered 'bootloader' mode.</li>"
            "<li>Ensure the boot volume is available (this may require"
            " mounting it).</li>"
            "<li>Select the firmware file to be flashed and click the"
            " flash button.</li>"
            "</ol>"
        ),
        "show_all": False,
        "firmware": "CircuitPython",
    },
    
    "rp2040": {
        "volumes": {
            (0x0000, 0x0000): [
                "RPI-RP2",        # Raspberry Pi Pico does not present a TTY
            ],
        },
        "instructions": QCoreApplication.translate(
            "UF2FlashDialog",
            "<h3>Pi Pico (RP2040) Board</h3>"
            "<p>In order to prepare the board for flashing follow these"
            " steps:</p><ol>"
            "<li>Enter 'bootloader' mode (board <b>without</b> RESET button):"
            "<ul>"
            "<li>Plug in your board while holding the BOOTSEL button.</li>"
            "</ul>"
            "Enter 'bootloader' mode (board <b>with</b> RESET button):"
            "<ul>"
            "<li>hold down RESET</li>"
            "<li>hold down BOOTSEL</li>"
            "<li>release RESET</li>"
            "<li>release BOOTSEL</li>"
            "</ul></li>"
            "<li>Wait until the device has entered 'bootloader' mode.</li>"
            "<li>Ensure the boot volume is available (this may require"
            " mounting it).</li>"
            "<li>Select the firmware file to be flashed and click the"
            " flash button.</li>"
            "</ol>"
        ),
        "show_all": True,
        "firmware": "MicroPython / CircuitPython",
    },
}


def getFoundDevices(boardType=""):
    """
    Function to get the list of known serial devices supporting UF2.
    
    @param boardType specific board type to search for
    @type str
    @return list of tuples with the board type, the port description, the
        VID and PID
    @rtype list of tuple of (str, str, int, int)
    """
    from PyQt6.QtSerialPort import QSerialPortInfo
    
    foundDevices = []
    
    availablePorts = QSerialPortInfo.availablePorts()
    for port in availablePorts:
        vid = port.vendorIdentifier()
        pid = port.productIdentifier()
        
        if vid == 0 and pid == 0:
            # no device detected at port
            continue
        
        for board in SupportedUF2Boards:
            if (
                (not boardType or (board.startswith(boardType))) and
                (vid, pid) in SupportedUF2Boards[board]["volumes"]
            ):
                foundDevices.append((
                    board,
                    port.description(),
                    (vid, pid),
                ))
    
    # second run for boards needing special treatment (e.g. RP2040)
    for board in SupportedUF2Boards:
        if not boardType or (board == boardType):
            with contextlib.suppress(KeyError):
                # find mounted volume
                volumes = SupportedUF2Boards[board]["volumes"][(0, 0)]
                foundVolumes = []
                for volume in volumes:
                    foundVolumes += Utilities.findVolume(volume, findAll=True)
                if foundVolumes:
                    foundDevices.append((
                        board,
                        QCoreApplication.translate(
                            "UF2FlashDialog", "'{0}' Board").format(board),
                        (0, 0),             # VID/PID of (0, 0) is special
                    ))
    
    return foundDevices


class UF2FlashDialog(QDialog, Ui_UF2FlashDialog):
    """
    Class implementing a dialog to flash any UF2 capable device.
    """
    DeviceTypeRole = Qt.ItemDataRole.UserRole
    DeviceVidPidRole = Qt.ItemDataRole.UserRole + 1
    
    def __init__(self, boardType="", parent=None):
        """
        Constructor
        
        @param boardType specific board type to show the dialog for
        @type str
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.refreshButton.setIcon(UI.PixmapCache.getIcon("rescan"))
        
        self.firmwarePicker.setMode(EricPathPickerModes.OPEN_FILE_MODE)
        self.firmwarePicker.setFilters(
            self.tr("MicroPython/CircuitPython Files (*.uf2);;"
                    "All Files (*)"))
        
        self.bootPicker.setMode(EricPathPickerModes.DIRECTORY_SHOW_FILES_MODE)
        self.bootPicker.setEnabled(False)
        
        self.__mandatoryStyleSheet = (
            "QLineEdit {border: 2px solid; border-color: #dd8888}"
            if ericApp().usesDarkPalette() else
            "QLineEdit {border: 2px solid; border-color: #800000}"
        )
        self.__manualType = "<manual>"
        
        self.__boardType = boardType
        
        self.__populate()
        
        self.__updateFlashButton()
    
    def __populate(self):
        """
        Private method to (re-)populate the dialog.
        """
        # save the currently selected device
        currentDevice = self.devicesComboBox.currentText()
        firmwareFile = self.firmwarePicker.text()
        
        # clear the entries first
        self.devicesComboBox.clear()
        self.firmwarePicker.clear()
        self.bootPicker.clear()
        self.infoLabel.clear()
        self.infoEdit.clear()
        
        # now populate the entries with data
        devices = getFoundDevices(boardType=self.__boardType)
        if len(devices) == 0:
            # no device detected
            devices = list(filter(
                lambda x: x[0] in SupportedUF2Boards,
                MicroPythonDevices.getFoundDevices()[0]
            ))
            if devices:
                self.__showSpecificInstructions(list(devices))
            else:
                self.__showAllInstructions()
            self.devicesComboBox.addItem("")
            self.devicesComboBox.addItem(self.tr("Manual Select"))
            self.devicesComboBox.setItemData(1, self.__manualType,
                                             self.DeviceTypeRole)
        elif len(devices) == 1:
            # set the board type to the found one
            self.__boardType = devices[0][0]
            
            self.devicesComboBox.addItem(devices[0][1])
            self.devicesComboBox.setItemData(
                0, devices[0][0], self.DeviceTypeRole)
            self.devicesComboBox.setItemData(
                0, devices[0][2], self.DeviceVidPidRole)
            self.devicesComboBox.addItem(self.tr("Manual Select"))
            self.devicesComboBox.setItemData(1, self.__manualType,
                                             self.DeviceTypeRole)
            self.on_devicesComboBox_currentIndexChanged(0)
        else:
            self.devicesComboBox.addItem("")
            for index, (boardType, description,
                        vidpid) in enumerate(sorted(devices), 1):
                self.devicesComboBox.addItem(description)
                self.devicesComboBox.setItemData(
                    index, boardType, self.DeviceTypeRole)
                self.devicesComboBox.setItemData(
                    index, vidpid, self.DeviceVidPidRole)
            self.devicesComboBox.addItem(self.tr("Manual Select"))
            self.devicesComboBox.setItemData(index + 1, self.__manualType,
                                             self.DeviceTypeRole)
        
        # reselect the remembered device, if it is still there
        if currentDevice:
            self.devicesComboBox.setCurrentText(currentDevice)
            self.firmwarePicker.setText(firmwareFile)
        else:
            self.devicesComboBox.setCurrentIndex(0)
    
    def __updateFlashButton(self):
        """
        Private method to update the state of the Flash button and the retest
        button.
        """
        firmwareFile = self.firmwarePicker.text()
        if self.devicesComboBox.currentData(self.DeviceTypeRole) is not None:
            if bool(firmwareFile) and os.path.exists(firmwareFile):
                self.firmwarePicker.setStyleSheet("")
            else:
                self.firmwarePicker.setStyleSheet(self.__mandatoryStyleSheet)
            
            if bool(self.bootPicker.text()):
                self.bootPicker.setStyleSheet("")
            else:
                self.bootPicker.setStyleSheet(self.__mandatoryStyleSheet)
        else:
            self.firmwarePicker.setStyleSheet("")
            self.bootPicker.setStyleSheet("")
        
        enable = (
            bool(self.bootPicker.text()) and
            bool(firmwareFile) and
            os.path.exists(firmwareFile)
        )
        self.flashButton.setEnabled(enable)
    
    def __showAllInstructions(self):
        """
        Private method to show instructions for resetting devices to bootloader
        mode.
        """
        self.infoLabel.setText(self.tr("Reset Instructions:"))
        
        htmlText = self.tr(
            "<h4>No known devices detected.</h4>"
            "<p>Follow the appropriate instructions below to set <b>one</b>"
            " board into 'bootloader' mode. Press <b>Refresh</b> when ready."
            "</p>"
        )
        for boardType in SupportedUF2Boards:
            if SupportedUF2Boards[boardType]["show_all"]:
                htmlText += (
                    "<hr/>" +
                    SupportedUF2Boards[boardType]["instructions"]
                )
        self.infoEdit.setHtml(htmlText)
    
    def __showSpecificInstructions(self, devices):
        """
        Private method to show instructions for resetting devices to bootloader
        mode for a list of detected devices.
        
        @param devices list of detected devices
        @type list of str
        """
        boardTypes = {x[0] for x in devices}
        
        self.infoLabel.setText(self.tr("Reset Instructions:"))
        
        if self.__boardType:
            htmlText = self.tr(
                "<h4>Flash {0} Firmware</h4>"
                "<p>Follow the instructions below to set <b>one</b> board into"
                " 'bootloader' mode. Press <b>Refresh</b> when ready.</p>"
                "<hr/>{1}"
            ).format(
                SupportedUF2Boards[self.__boardType]["firmware"],
                SupportedUF2Boards[self.__boardType]["instructions"],
            )
        else:
            htmlText = self.tr(
                "<h4>Potentially UF2 capable devices found</h4>"
                "<p>Found these potentially UF2 capable devices:</p>"
                "<ul><li>{0}</li></ul>"
                "<p>Follow the instructions below to set <b>one</b> board into"
                " 'bootloader' mode. Press <b>Refresh</b> when ready.</p>"
            ).format(
                "</li><li>".join(sorted(x[1] for x in devices))
            )
            for boardType in sorted(boardTypes):
                htmlText += (
                    "<hr/>" + SupportedUF2Boards[boardType]["instructions"]
                )
        self.infoEdit.setHtml(htmlText)
    
    def __showTypedInstructions(self, boardType):
        """
        Private method to show instructions for resetting devices to bootloader
        mode for a specific board type.
        
        @param boardType type of the board to show instructions for
        @type str
        """
        self.infoLabel.setText(self.tr("Reset Instructions:"))
        
        htmlText = self.tr(
            "<h4>No known devices detected.</h4>"
            "<p>Follow the instructions below to set <b>one</b> board into"
            " 'bootloader' mode. Press <b>Refresh</b> when ready.</p>"
        )
        htmlText += "<hr/>" + SupportedUF2Boards[boardType]["instructions"]
        self.infoEdit.setHtml(htmlText)
    
    def __showManualInstructions(self):
        """
        Private method to show instructions for flashing devices manually.
        """
        self.infoLabel.setText(self.tr("Flash Instructions:"))
        
        htmlText = self.tr(
            "<h4>Flash method 'manual' selected.</h4>"
            "<p>Follow the instructions below to flash a device by entering"
            " the data manually.</p><ol>"
            "<li>Change the device to 'bootloader' mode.</li>"
            "<li>Wait until the device has entered 'bootloader' mode.</li>"
            "<li>Ensure the boot volume is available (this may require"
            " mounting it) and select its path.</li>"
            "<li>Select the firmware file to be flashed and click the"
            " flash button.</li>"
            "</ol>"
        )
        for boardType in SupportedUF2Boards:
            htmlText += "<hr/>" + SupportedUF2Boards[boardType]["instructions"]
        self.infoEdit.setHtml(htmlText)
    
    def __showNoVolumeInformation(self, volumes, boardType):
        """
        Private method to show information about the expected boot volume(s).
        
        @param volumes list of expected volume names
        @type list of str
        @param boardType type of the board to show instructions for
        @type str
        """
        self.infoLabel.setText(self.tr("Boot Volume not found:"))
        
        htmlText = self.tr(
            "<h4>No Boot Volume detected.</h4>"
            "<p>Please ensure that the boot volume of the device to be flashed"
            " is available. "
        )
        if len(volumes) == 1:
            htmlText += self.tr(
                "This volume should be named <b>{0}</b>."
                " Press <b>Refresh</b> when ready.</p>"
            ).format(volumes[0])
        else:
            htmlText += self.tr(
                "This volume should have one of these names.</p>"
                "<ul><li>{0}</li></ul>"
                "<p>Press <b>Refresh</b> when ready.</p>"
            ).format("</li><li>".join(sorted(volumes)))
        
        if boardType:
            htmlText += self.tr(
                "<h4>Reset Instructions</h4>"
                "<p>Follow the instructions below to set the board into"
                " 'bootloader' mode. Press <b>Refresh</b> when ready.</p>"
            )
            htmlText += "<hr/>" + SupportedUF2Boards[boardType]["instructions"]
        
        self.infoEdit.setHtml(htmlText)
    
    def __showMultipleVolumesInformation(self, volumePaths):
        """
        Private method to show information because multiple devices of the
        same type are ready for flashing.
        
        Note: This is a dangerous situation!
        
        @param volumePaths list of volume paths
        @type list of str
        """
        self.infoLabel.setText(self.tr("Multiple Boot Volumes found:"))
        
        htmlText = self.tr(
            "<h4>Multiple Boot Volumes were found</h4>"
            "<p>These volume paths were found.</p><ul><li>{0}</li></ul>"
            "<p>Please ensure that only one device of a type is ready for"
            " flashing. Press <b>Refresh</b> when ready.</p>"
        ).format("</li><li>".join(sorted(volumePaths)))
        self.infoEdit.setHtml(htmlText)
    
    @pyqtSlot()
    def on_flashButton_clicked(self):
        """
        Private slot to flash the selected MicroPython or CircuitPython
        firmware onto the device.
        """
        boardType = self.devicesComboBox.currentData(self.DeviceTypeRole)
        firmwarePath = self.firmwarePicker.text()
        volumePath = self.bootPicker.text()
        if os.path.exists(firmwarePath) and os.path.exists(volumePath):
            if boardType == self.__manualType:
                self.infoLabel.setText(self.tr("Flashing Firmware"))
                self.infoEdit.setHtml(self.tr(
                    "<p>Flashing the selected firmware to the device. Please"
                    " wait until the device resets automatically.</p>")
                )
            else:
                firmwareType = SupportedUF2Boards[boardType]["firmware"]
                self.infoLabel.setText(
                    self.tr("Flashing {0}").format(firmwareType))
                self.infoEdit.setHtml(self.tr(
                    "<p>Flashing the {0} firmware to the device. Please wait"
                    " until the device resets automatically.</p>"
                ).format(firmwareType))
            QCoreApplication.processEvents(
                QEventLoop.ProcessEventsFlag.ExcludeUserInputEvents)
            shutil.copy2(firmwarePath, volumePath)
            QThread.sleep(1)
            self.on_refreshButton_clicked()
    
    @pyqtSlot()
    def on_refreshButton_clicked(self):
        """
        Private slot to refresh the dialog.
        """
        # special treatment for RPi Pico
        if self.__boardType == "circuitpython_rp2040":
            self.__boardType = "rp2040"
        
        self.__populate()
    
    @pyqtSlot(int)
    def on_devicesComboBox_currentIndexChanged(self, index):
        """
        Private slot to handle the selection of a board.
        
        @param index selected index
        @type int
        """
        vidpid = self.devicesComboBox.itemData(index, self.DeviceVidPidRole)
        boardType = self.devicesComboBox.itemData(index, self.DeviceTypeRole)
        
        self.bootPicker.setEnabled(boardType == self.__manualType)
        if boardType == self.__manualType:
            self.__showManualInstructions()
        
        if vidpid is None:
            if boardType is None:
                self.bootPicker.clear()
        else:
            volumes = SupportedUF2Boards[boardType]["volumes"][vidpid]
            foundVolumes = []
            for volume in volumes:
                foundVolumes += Utilities.findVolume(volume, findAll=True)
            
            if len(foundVolumes) == 0:
                self.__showNoVolumeInformation(volumes, boardType)
                self.bootPicker.clear()
            elif len(foundVolumes) == 1:
                self.bootPicker.setText(foundVolumes[0])
            else:
                self.__showMultipleVolumesInformation()
                self.bootPicker.clear()
        
        self.__updateFlashButton()
    
    @pyqtSlot(str)
    def on_firmwarePicker_textChanged(self, text):
        """
        Private slot handling a change of the firmware file.
        
        @param text current text of the firmware edit
        @type str
        """
        self.__updateFlashButton()
    
    @pyqtSlot(str)
    def on_bootPicker_textChanged(self, text):
        """
        Private slot handling a change of the boot volume.
        
        @param text current text of the boot volume edit
        @type str
        """
        self.__updateFlashButton()
