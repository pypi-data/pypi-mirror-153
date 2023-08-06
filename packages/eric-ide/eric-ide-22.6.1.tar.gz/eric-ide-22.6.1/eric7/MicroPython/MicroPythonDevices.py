# -*- coding: utf-8 -*-

# Copyright (c) 2019 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some utility functions and the MicroPythonDevice base
class.
"""

import logging
import os

from PyQt6.QtCore import pyqtSlot, QObject, QCoreApplication
from PyQt6.QtWidgets import QInputDialog

from EricWidgets.EricApplication import ericApp

import UI.PixmapCache
import Preferences


SupportedBoards = {
    "esp": {
        "ids": [
            (0x0403, 0x6001),       # M5Stack ESP32 device"),
            (0x0403, 0x6001),       # FT232/FT245 (XinaBox CW01, CW02)
            (0x0403, 0x6010),       # FT2232C/D/L/HL/Q (ESP-WROVER-KIT)
            (0x0403, 0x6011),       # FT4232
            (0x0403, 0x6014),       # FT232H
            (0x0403, 0x6015),       # Sparkfun ESP32
            (0x0403, 0x601C),       # FT4222H
            (0x10C4, 0xEA60),       # CP210x
            (0x1A86, 0x55D4),       # CH343
            (0x1A86, 0x7523),       # HL-340, CH340
        ],
        "description": "ESP32, ESP8266",
        "icon": "esp32Device",
        "port_description": "",
    },
    
    "circuitpython": {
        "ids": [
            (0x04D8, 0xEA2A),       # BHDynamics DynaLoRa_USB
            (0x04D8, 0xEAD1),       # BH Dynamics DynOSSAT-EDU-EPS-v1.0
            (0x04D8, 0xEAD2),       # BH Dynamics DynOSSAT-EDU-OBC-v1.0
            (0x04D8, 0xEC44),       # maholli PyCubed
            (0x04D8, 0xEC63),       # Kevin Neubauer CircuitBrains Basic
            (0x04D8, 0xEC64),       # Kevin Neubauer CircuitBrains Deluxe
            (0x04D8, 0xEC72),       # XinaBox CC03
            (0x04D8, 0xEC75),       # XinaBox CS11
            (0x04D8, 0xED5F),       # Itaca Innovation uChip CircuitPython
            (0x04D8, 0xED94),       # maholli kicksat-sprite
            (0x04D8, 0xEDB3),       # Capable Robot Programmable USB Hub
            (0x04D8, 0xEDBE),       # maholli SAM32
            (0x04D8, 0xEE8C),       # J&J Studios LLC datum-Distance
            (0x04D8, 0xEE8D),       # J&J Studios LLC datum-IMU
            (0x04D8, 0xEE8E),       # J&J Studios LLC datum-Light
            (0x04D8, 0xEE8F),       # J&J Studios LLC datum-Weather
            (0x04D8, 0xEF67),       # senseBox MCU
            (0x054C, 0x0BC2),       # Sony Spresense
            (0x1209, 0x2017),       # Benjamin Shockley Mini SAM M4
            (0x1209, 0x3141),       # CrumpSpace CrumpS2
            (0x1209, 0x3252),       # Targett Module Clip w/Wroom
            (0x1209, 0x3253),       # Targett Module Clip w/Wrover
            (0x1209, 0x4D43),       # Robotics Masters Robo HAT MM1 M4
            (0x1209, 0x4DDD),       # ODT CP Sapling
            (0x1209, 0x4DDE),       # ODT CP Sapling M0 w/ SPI Flash
            (0x1209, 0x4DDF),       # ODT CP Sapling Rev B
            (0x1209, 0x4DF0),       # Oak Dev Tech Pixelwing ESP32S2
            (0x1209, 0x4DF1),       # Oak Dev Tech BREAD2040
            (0x1209, 0x4DF2),       # Oak Dev Tech CAST AWAY RP2040
            (0x1209, 0x5BF0),       # Foosn Fomu
            (0x1209, 0x7150),       # Electronic Cats Hunter Cat NFC
            (0x1209, 0x7382),       # Invector Labs AB iLabs Challenger 840
            (0x1209, 0x805A),       # Electronic Cats BastBLE
            (0x1209, 0xA182),       # Solder Party RP2040 Stamp
            (0x1209, 0xBAB0),       # Electronic Cats Bast WiFi
            (0x1209, 0xBAB1),       # Electronic Cats Meow Meow
            (0x1209, 0xBAB2),       # Electronic Cats CatWAN USBStick
            (0x1209, 0xBAB3),       # Electronic Cats Bast Pro Mini M0
            (0x1209, 0xBAB6),       # Electronic Cats Escornabot Makech
            (0x1209, 0xBAB8),       # Electronic Cats NFC Copy Cat
            (0x1209, 0xC051),       # Betrusted Simmel
            (0x1209, 0xD10D),       # Diodes Delight Piunora
            (0x1209, 0xE3E3),       # StackRduino M0 PRO
            (0x1209, 0xF500),       # Silicognition LLC M4-Shim
            (0x16D0, 0x08C6),       # Pimoroni Keybow 2040
            (0x16D0, 0x08C7),       # Pimoroni Tiny 2040 (8MB)
            (0x16D0, 0x08C8),       # Pimoroni PicoSystem
            (0x1915, 0xB001),       # Makerdiary Pitaya Go
            (0x192F, 0xB1B2),       # WarmBit BluePixel nRF52840
            (0x1B4F, 0x0015),       # SparkFun RedBoard Turbo Board
            (0x1B4F, 0x0016),       # SparkFun SAMD51 Thing+
            (0x1B4F, 0x0017),       # SparkFun LUMIDrive Board
            (0x1B4F, 0x0020),       # SparkFun MicroMod SAMD51 Processor
            (0x1B4F, 0x0021),       # SparkFun MicroMod nRF52840 Processor
            (0x1B4F, 0x0024),       # SparkFun MicroMod RP2040 Processor
            (0x1B4F, 0x0025),       # SparkFun Thing Plus RP2040
            (0x1B4F, 0x0026),       # SparkFun Pro Micro RP2040
            (0x1B4F, 0x0027),       # SparkFun STM32 MicroMod Processor
            (0x1B4F, 0x0028),       # SparkFun Thing Plus - STM32
            (0x1B4F, 0x002E),       # PJRC/Sparkfun Teensy MicroMod
            (0x1B4F, 0x5289),       # SparkFun SFE_nRF52840_Mini
            (0x1B4F, 0x8D22),       # SparkFun SAMD21 Mini Breakout
            (0x1B4F, 0x8D23),       # SparkFun SAMD21 Dev Breakout
            (0x1B4F, 0x8D24),       # SparkFun Qwiic Micro
            (0x1D50, 0x60E8),       # Radomir Dopieralski PewPew M4
            (0x1D50, 0x6152),       # nrf52.jpconstantineau.com BlueMicro833
            (0x1D50, 0x6153),       # JPConstantineau PyKey18
            (0x1D50, 0x6153),       # JPConstantineau PyKey44
            (0x1D50, 0x6153),       # JPConstantineau PyKey60
            (0x1D50, 0x6153),       # JPConstantineau PyKey87
            (0x1D50, 0x6154),       # JPConstantineau EncoderPad RP2040
            (0x1D50, 0x6161),       # nrf52.jpconstantineau.com BlueMicro840
            (0x2341, 0x8053),       # Arduino MKR1300
            (0x2341, 0x8057),       # Arduino Nano 33 IoT
            (0x2341, 0x805A),       # Arduino Arduino_Nano_33_BLE
            (0x2341, 0x824D),       # Arduino Zero
            (0x2786, 0x9207),       # Switch Sc. BLE-SS dev board Multi Sensor
            (0x2786, 0x920D),       # Switch Sc. SSCI ISP1807 Dev Board
            (0x2786, 0x920F),       # Switch Sc. SSCI ISP1807 Micro Board
            (0x2886, 0x002F),       # Seeed Seeeduino XIAO
            (0x2886, 0x0042),       # Seeed Seeeduino XIAO RP2040
            (0x2886, 0x0045),       # Seeed XIAO nRF52840 Sense
            (0x2886, 0x802D),       # Seeed Seeeduino Wio Terminal
            (0x2886, 0x802F),       # Seeed Seeeduino XIAO KB
            (0x2886, 0xF001),       # Makerdiary nRF52840 M.2 Developer Kit
            (0x2886, 0xF002),       # Makerdiary M60 Keyboard
            (0x2B04, 0xC00C),       # Particle Argon
            (0x2B04, 0xC00D),       # Particle Boron
            (0x2B04, 0xC00E),       # Particle Xenon
            (0x2E8A, 0x1000),       # Cytron Maker Pi RP2040
            (0x2E8A, 0x1002),       # Pimoroni Pico LiPo (4MB)
            (0x2E8A, 0x1003),       # Pimoroni Pico LiPo (16MB)
            (0x2E8A, 0x1005),       # Melopero Shake RP2040
            (0x2E8A, 0x1006),       # Invector Labs Challenger RP2040 WiFi
            (0x2E8A, 0x1008),       # Pimoroni PGA2040
            (0x2E8A, 0x1009),       # Pimoroni Interstate 75
            (0x2E8A, 0x100A),       # Pimoroni Plasma 2040
            (0x2E8A, 0x100B),       # Invector Labs Challenger RP2040 LTE
            (0x2E8A, 0x100D),       # Invector Labs Challenger NB RP2040 WiFi
            (0x2E8A, 0x100E),       # Raspberry Pi Zero
            (0x2E8A, 0x100F),       # Cytron Maker Nano RP2040
            (0x2E8A, 0x1012),       # Raspberry Pi Compute Module 4 IO Board
            (0x2E8A, 0x1013),       # Raspberry Pi 4B
            (0x2E8A, 0x1014),       # Raspberry Pi Compute Module 4
            (0x2E8A, 0x1015),       # Raspberry Pi Zero 2W
            (0x2E8A, 0x1016),       # Pimoroni Tiny 2040 (2MB)
            (0x2E8A, 0x1019),       # Pimoroni Motor 2040
            (0x2E8A, 0x101A),       # Pimoroni Servo 2040
            (0x2E8A, 0x101B),       # Pimoroni Badger 2040
            (0x2E8A, 0x101E),       # Raspberry Pi Zero W
            (0x2E8A, 0x101F),       # Waveshare Electronics RP2040-Zero
            (0x2E8A, 0x1026),       # ELECFREAKS Pico:ed
            (0x2E8A, 0x1027),       # WIZnet W5100S-EVB-Pico
            (0x303A, 0x7001),       # Espressif ESP32-S2-HMI-DevKit-1
            (0x303A, 0x7003),       # Espressif ESP32-S3-DevKitC-1
            (0x303A, 0x7003),       # Espressif ESP32-S3-DevKitC-1-N8
            (0x303A, 0x7003),       # Espressif ESP32-S3-DevKitC-1-N8R2
            (0x303A, 0x7003),       # Espressif ESP32-S3-DevKitC-1-N8R8
            (0x303A, 0x7003),       # Espressif ESP32-S3-DevKitC-1-nopsram
            (0x303A, 0x7005),       # Espressif ESP32-S3-Box-2.5
            (0x303A, 0x7007),       # Espressif ESP32-S3-DevKitM-1-N8
            (0x303A, 0x7009),       # Espressif ESP32-S2-DevKitC-1-N4
            (0x303A, 0x7009),       # Espressif ESP32-S2-DevKitC-1-N4R2
            (0x303A, 0x700B),       # Espressif ESP32-S3-USB-OTG-N8
            (0x303A, 0x8002),       # UnexpectedMaker TinyS2
            (0x303A, 0x8007),       # LILYGO TTGO T8 ESP32-S2
            (0x303A, 0x800D),       # Gravitech Cucumber RS
            (0x303A, 0x80A1),       # Gravitech Cucumber R
            (0x303A, 0x80A4),       # Gravitech Cucumber M
            (0x303A, 0x80A7),       # Gravitech Cucumber MS
            (0x303A, 0x80AA),       # Espressif Franzininho WIFI w/Wroom
            (0x303A, 0x80AD),       # Espressif Franzininho WIFI w/Wrover
            (0x303A, 0x80AF),       # Artisense Reference Design RD00
            (0x303A, 0x80B2),       # Muselab nanoESP32-S2  w/Wrover
            (0x303A, 0x80B5),       # UnexpectedMaker FeatherS2 Neo
            (0x303A, 0x80B7),       # MORPHEANS MORPHESP-240
            (0x303A, 0x80C3),       # Lolin S2 Mini
            (0x303A, 0x80C6),       # Lolin S2 Pico
            (0x303A, 0x80D1),       # UnexpectedMaker TinyS3
            (0x303A, 0x80D4),       # UnexpectedMaker ProS3
            (0x303A, 0x80D7),       # UnexpectedMaker FeatherS3
            (0x303A, 0x80D9),       # FutureKeys HexKy_S2
            (0x303A, 0x80E8),       # HiiBot IoTs2
            (0x303A, 0x80EA),       # LILYGO TTGO T8 ESP32-S2-WROOM
            (0x303A, 0x80ED),       # LILYGO TTGO T8 ESP32-S2
            (0x30A4, 0x0002),       # Blues Inc. Swan R5
            (0x3171, 0x0101),       # 8086.net Commander
            (0x31E2, 0x2001),       # BDMICRO LLC VINA-D21
            (0x31E2, 0x2011),       # BDMICRO LLC VINA-D51
            (0x31E2, 0x2021),       # BDMICRO LLC VINA-D51
            (0x32BD, 0x3001),       # Alorium Tech. AloriumTech Evo M51
            (0x4097, 0x0001),       # TG-Boards Datalore IP M4
            (0x612B, 0x80A7),       # Ai-Thinker ESP 12k NodeMCU
            
            (0x239A, None),         # Any Adafruit Boards
        ],
        "description": "CircuitPython",
        "icon": "circuitPythonDevice",
        "port_description": "",
    },
    
    "bbc_microbit": {
        "ids": [
            (0x0D28, 0x0204),       # micro:bit
        ],
        "description": "BBC micro:bit",
        "icon": "microbitDevice",
        "port_description": "BBC micro:bit CMSIS-DAP",
    },
    
    "calliope": {
        "ids": [
            (0x0D28, 0x0204),       # Calliope mini
        ],
        "description": "Calliope mini",
        "icon": "calliope_mini",
        "port_description": "DAPLink CMSIS-DAP",
    },
    
    "pyboard": {
        "ids": [
            (0xF055, 0x9800),       # Pyboard in CDC mode
            (0xF055, 0x9801),       # Pyboard in CDC+HID mode
            (0xF055, 0x9802),       # Pyboard in CDC+MSC mode
        ],
        "description": "PyBoard",
        "icon": "micropython48",
        "port_description": "",
    },
    
    "rp2040": {
        "ids": [
            (0x2E8A, 0x0005),       # Raspberry Pi Pico
        ],
        "description": QCoreApplication.translate(
            "MicroPythonDevice", "RP2040 based"),
        "icon": "rp2040Device",
        "port_description": "",
    },
    
    "generic": {
        # only manually configured devices use this
        "ids": [],
        "description": QCoreApplication.translate(
            "MicroPythonDevice", "Generic Board"),
        "icon": "micropython48",
        "port_description": "",
    },
}

IgnoredBoards = (
    (0x8086, 0x9c3d),
    (0x8086, None),
)


def getSupportedDevices():
    """
    Function to get a list of supported MicroPython devices.
    
    @return set of tuples with the board type and description
    @rtype set of tuples of (str, str)
    """
    boards = []
    for board in SupportedBoards:
        boards.append(
            (board, SupportedBoards[board]["description"]))
    return boards


def getFoundDevices():
    """
    Function to check the serial ports for supported MicroPython devices.
    
    @return tuple containing a list of tuples with the board type, the port
        description, a description, the serial port it is connected at, the
        VID and PID for known device types, a list of tuples with VID, PID
        and description for unknown devices and a list of tuples with VID,
        PID, description and port name for ports with missing VID or PID
    @rtype tuple of (list of tuples of (str, str, str, str, int, int),
        list of tuples of (int, int, str),
        list of tuples of (int, int, str, str)
    """
    from PyQt6.QtSerialPort import QSerialPortInfo
    
    foundDevices = []
    unknownDevices = []
    unknownPorts = []
    
    manualDevices = {}
    for deviceDict in Preferences.getMicroPython("ManualDevices"):
        manualDevices[(deviceDict["vid"], deviceDict["pid"])] = deviceDict
    
    availablePorts = QSerialPortInfo.availablePorts()
    for port in availablePorts:
        if port.hasVendorIdentifier() and port.hasProductIdentifier():
            supported = False
            vid = port.vendorIdentifier()
            pid = port.productIdentifier()
            
            for board in SupportedBoards:
                if (
                    (vid, pid) in SupportedBoards[board]["ids"] or
                    (vid, None) in SupportedBoards[board]["ids"]
                ):
                    if (
                        board in ("bbc_microbit", "calliope") and
                        (port.description().strip() !=
                         SupportedBoards[board]["port_description"])
                    ):
                        # both boards have the same VID and PID
                        # try to differentiate based on port description
                        continue
                    foundDevices.append((
                        board,
                        port.description(),
                        SupportedBoards[board]["description"],
                        port.portName(),
                        vid,
                        pid,
                    ))
                    supported = True
            if not supported and (vid, pid) in manualDevices:
                # check the locally added ones next
                board = manualDevices[(vid, pid)]["type"]
                foundDevices.append((
                    board,
                    port.description(),
                    SupportedBoards[board]["description"],
                    port.portName(),
                    vid,
                    pid,
                ))
                supported = True
            if not supported:
                if vid and pid:
                    if (
                        (vid, pid) not in IgnoredBoards and
                        (vid, None) not in IgnoredBoards
                    ):
                        unknownDevices.append((vid, pid, port.description()))
                        logging.debug("Unknown device: (0x%04x:0x%04x %s)",
                                      vid, pid, port.description())
                else:
                    # either VID or PID or both not detected
                    desc = port.description()
                    if not desc:
                        desc = QCoreApplication.translate("MicroPythonDevice",
                                                          "Unknown Device")
                    unknownPorts.append((vid, pid, desc, port.portName()))
    
    return foundDevices, unknownDevices, unknownPorts


def getDeviceIcon(boardName, iconFormat=True):
    """
    Function to get the icon for the given board.
    
    @param boardName name of the board
    @type str
    @param iconFormat flag indicating to get an icon or a pixmap
    @type bool
    @return icon for the board (iconFormat == True) or
        a pixmap (iconFormat == False)
    @rtype QIcon or QPixmap
    """
    iconName = (
        SupportedBoards[boardName]["icon"]
        if boardName in SupportedBoards else
        # return a generic MicroPython icon
        "micropython48"
    )
    
    if iconFormat:
        return UI.PixmapCache.getIcon(iconName)
    else:
        return UI.PixmapCache.getPixmap(iconName)


def getDevice(deviceType, microPythonWidget, vid, pid):
    """
    Public method to instantiate a specific MicroPython device interface.
    
    @param deviceType type of the device interface
    @type str
    @param microPythonWidget reference to the main MicroPython widget
    @type MicroPythonWidget
    @param vid vendor ID (only used for deviceType 'generic')
    @type int
    @param pid product ID (only used for deviceType 'generic')
    @type int
    @return instantiated device interface
    @rtype MicroPythonDevice
    """
    if deviceType == "esp":
        from .EspDevices import EspDevice
        return EspDevice(microPythonWidget, deviceType)
    elif deviceType == "circuitpython":
        from .CircuitPythonDevices import CircuitPythonDevice
        return CircuitPythonDevice(microPythonWidget, deviceType)
    elif deviceType in ("bbc_microbit", "calliope"):
        from .MicrobitDevices import MicrobitDevice
        return MicrobitDevice(microPythonWidget, deviceType)
    elif deviceType == "pyboard":
        from .PyBoardDevices import PyBoardDevice
        return PyBoardDevice(microPythonWidget, deviceType)
    elif deviceType == "rp2040":
        from .RP2040Devices import RP2040Device
        return RP2040Device(microPythonWidget, deviceType)
    elif deviceType == "generic":
        from .GenericMicroPythonDevices import GenericMicroPythonDevice
        return GenericMicroPythonDevice(microPythonWidget, deviceType,
                                        vid, pid)
    else:
        # nothing specific requested
        return MicroPythonDevice(microPythonWidget, deviceType)


class MicroPythonDevice(QObject):
    """
    Base class for the more specific MicroPython devices.
    """
    def __init__(self, microPythonWidget, deviceType, parent=None):
        """
        Constructor
        
        @param microPythonWidget reference to the main MicroPython widget
        @type MicroPythonWidget
        @param deviceType device type assigned to this device interface
        @type str
        @param parent reference to the parent object
        @type QObject
        """
        super().__init__(parent)
        
        self._deviceType = deviceType
        self.microPython = microPythonWidget
    
    def getDeviceType(self):
        """
        Public method to get the device type.
        
        @return type of the device
        @rtype str
        """
        return self._deviceType
    
    def setButtons(self):
        """
        Public method to enable the supported action buttons.
        """
        self.microPython.setActionButtons(
            open=False, save=False,
            run=False, repl=False, files=False, chart=False)
    
    def forceInterrupt(self):
        """
        Public method to determine the need for an interrupt when opening the
        serial connection.
        
        @return flag indicating an interrupt is needed
        @rtype bool
        """
        return True
    
    def deviceName(self):
        """
        Public method to get the name of the device.
        
        @return name of the device
        @rtype str
        """
        return self.tr("Unsupported Device")
    
    def canStartRepl(self):
        """
        Public method to determine, if a REPL can be started.
        
        @return tuple containing a flag indicating it is safe to start a REPL
            and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("REPL is not supported by this device.")
    
    def setRepl(self, on):
        """
        Public method to set the REPL status and dependent status.
        
        @param on flag indicating the active status
        @type bool
        """
        pass
    
    def canStartPlotter(self):
        """
        Public method to determine, if a Plotter can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("Plotter is not supported by this device.")
    
    def setPlotter(self, on):
        """
        Public method to set the Plotter status and dependent status.
        
        @param on flag indicating the active status
        @type bool
        """
        pass
    
    def canRunScript(self):
        """
        Public method to determine, if a script can be executed.
        
        @return tuple containing a flag indicating it is safe to start a
            Plotter and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("Running scripts is not supported by this"
                              " device.")
    
    def runScript(self, script):
        """
        Public method to run the given Python script.
        
        @param script script to be executed
        @type str
        """
        pass
    
    def canStartFileManager(self):
        """
        Public method to determine, if a File Manager can be started.
        
        @return tuple containing a flag indicating it is safe to start a
            File Manager and a reason why it cannot.
        @rtype tuple of (bool, str)
        """
        return False, self.tr("File Manager is not supported by this device.")
    
    def setFileManager(self, on):
        """
        Public method to set the File Manager status and dependent status.
        
        @param on flag indicating the active status
        @type bool
        """
        pass
    
    def supportsLocalFileAccess(self):
        """
        Public method to indicate file access via a local directory.
        
        @return flag indicating file access via local directory
        @rtype bool
        """
        return False        # default
    
    def getWorkspace(self):
        """
        Public method to get the workspace directory.
        
        @return workspace directory used for saving files
        @rtype str
        """
        return (
            Preferences.getMicroPython("MpyWorkspace") or
            Preferences.getMultiProject("Workspace") or
            os.path.expanduser("~")
        )
    
    def selectDeviceDirectory(self, deviceDirectories):
        """
        Public method to select the device directory from a list of detected
        ones.
        
        @param deviceDirectories list of directories to select from
        @type list of str
        @return selected directory or an empty string
        @rtype str
        """
        deviceDirectory, ok = QInputDialog.getItem(
            None,
            self.tr("Select Device Directory"),
            self.tr("Select the directory for the connected device:"),
            [""] + deviceDirectories,
            0, False)
        if ok:
            return deviceDirectory
        else:
            # user cancelled
            return ""
    
    def sendCommands(self, commandsList):
        """
        Public method to send a list of commands to the device.
        
        @param commandsList list of commands to be sent to the device
        @type list of str
        """
        rawOn = [       # sequence of commands to enter raw mode
            b'\x02',            # Ctrl-B: exit raw repl (just in case)
            b'\r\x03\x03\x03',  # Ctrl-C three times: interrupt any running
                                # program
            b'\r\x01',          # Ctrl-A: enter raw REPL
        ]
        newLine = [b'print("\\n")\r', ]
        commands = [c.encode("utf-8)") + b'\r' for c in commandsList]
        commands.append(b'\r')
        commands.append(b'\x04')
        rawOff = [b'\x02', b'\x02']
        commandSequence = rawOn + newLine + commands + rawOff
        self.microPython.commandsInterface().executeAsync(commandSequence)
    
    @pyqtSlot()
    def handleDataFlood(self):
        """
        Public slot handling a data floof from the device.
        """
        pass
    
    def addDeviceMenuEntries(self, menu):
        """
        Public method to add device specific entries to the given menu.
        
        @param menu reference to the context menu
        @type QMenu
        """
        pass
    
    def hasFlashMenuEntry(self):
        """
        Public method to check, if the device has its own flash menu entry.
        
        @return flag indicating a specific flash menu entry
        @rtype bool
        """
        return False
    
    def hasTimeCommands(self):
        """
        Public method to check, if the device supports time commands.
        
        The default returns True.
        
        @return flag indicating support for time commands
        @rtype bool
        """
        return True
    
    def hasDocumentationUrl(self):
        """
        Public method to check, if the device has a configured documentation
        URL.
        
        @return flag indicating a configured documentation URL
        @rtype bool
        """
        return bool(self.getDocumentationUrl())
    
    def getDocumentationUrl(self):
        """
        Public method to get the device documentation URL.
        
        @return documentation URL of the device
        @rtype str
        """
        return ""
    
    def hasFirmwareUrl(self):
        """
        Public method to check, if the device has a configured firmware
        download URL.
        
        @return flag indicating a configured firmware download URL
        @rtype bool
        """
        return bool(self.getFirmwareUrl())
    
    def getFirmwareUrl(self):
        """
        Public method to get the device firmware download URL.
        
        @return firmware download URL of the device
        @rtype str
        """
        return ""
    
    def downloadFirmware(self):
        """
        Public method to download the device firmware.
        """
        url = self.getFirmwareUrl()
        if url:
            ericApp().getObject("UserInterface").launchHelpViewer(url)
    
    def getDownloadMenuEntries(self):
        """
        Public method to retrieve the entries for the downloads menu.
        
        @return list of tuples with menu text and URL to be opened for each
            entry
        @rtype list of tuple of (str, str)
        """
        return []
