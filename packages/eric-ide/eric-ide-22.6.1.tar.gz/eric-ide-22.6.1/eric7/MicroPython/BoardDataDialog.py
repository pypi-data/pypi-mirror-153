# -*- coding: utf-8 -*-

# Copyright (c) 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show information about a connected board.
"""

import contextlib

from PyQt6.QtCore import QLocale
from PyQt6.QtWidgets import QDialog, QTreeWidgetItem

from .Ui_BoardDataDialog import Ui_BoardDataDialog


class BoardDataDialog(QDialog, Ui_BoardDataDialog):
    """
    Class implementing a dialog to show information about a connected board.
    """
    def __init__(self, data, parent=None):
        """
        Constructor
        
        @param data dictionary containing the data to be shown
        @type dict
        @param parent reference to the parent widget (defaults to None)
        @type QWidget (optional)
        """
        super().__init__(parent)
        self.setupUi(self)
        
        loc = QLocale()
        
        self.dataTree.setColumnCount(2)
        
        header = self.__createHeader(self.tr("General"))
        QTreeWidgetItem(header, [
            self.tr("Board ID"),
            data["mc_id"]
        ])
        QTreeWidgetItem(header, [
            self.tr("Board Frequency"),
            self.tr("{0} MHz").format(
                loc.toString(data["mc_frequency_mhz"], "f", 0))
        ])
        with contextlib.suppress(KeyError):
            QTreeWidgetItem(header, [
                self.tr("Board Temperature"),
                self.tr("{0} °C").format(
                    loc.toString(data["mc_temp_c"], "f", 1))
            ])
        
        header = self.__createHeader(self.tr("Python"))
        QTreeWidgetItem(header, [
            self.tr("Python Version"),
            data["py_version"]
        ])
        QTreeWidgetItem(header, [
            self.tr("Platform"),
            data["py_platform"]
        ])
        if data["mpy_name"] == "micropython":
            mpyName = "MicroPython"
        elif data["mpy_name"] == "circuitpython":
            mpyName = "CircuitPython"
        elif data["mpy_name"] == "unknown":
            mpyName = self.tr("unknown")
        else:
            mpyName = data["name"]
        QTreeWidgetItem(header, [
            self.tr("Implementation"),
            self.tr("{0} V. {1}").format(
                mpyName,
                self.tr("unknown")
                if data["mpy_version"] == "unknown" else
                data["mpy_version"]
            )
        ])
        
        header = self.__createHeader(self.tr("System"))
        QTreeWidgetItem(header, [
            self.tr("System Name"),
            data["sysname"]
        ])
        QTreeWidgetItem(header, [
            self.tr("Node Name"),
            data["nodename"]
        ])
        QTreeWidgetItem(header, [
            self.tr("Release"),
            data["release"]
        ])
        QTreeWidgetItem(header, [
            self.tr("Version"),
            data["version"]
        ])
        QTreeWidgetItem(header, [
            self.tr("Machine"),
            data["machine"]
        ])
        
        header = self.__createHeader(self.tr("Memory"))
        QTreeWidgetItem(header, [
            self.tr("total"),
            self.tr("{0} KBytes").format(
                loc.toString(data["mem_total_kb"], "f", 2))
        ])
        QTreeWidgetItem(header, [
            self.tr("used"),
            self.tr("{0} KBytes ({1}%)").format(
                loc.toString(data["mem_used_kb"], "f", 2),
                loc.toString(data["mem_used_pc"], "f", 2))
        ])
        QTreeWidgetItem(header, [
            self.tr("free"),
            self.tr("{0} KBytes ({1}%)").format(
                loc.toString(data["mem_free_kb"], "f", 2),
                loc.toString(data["mem_free_pc"], "f", 2))
        ])
        
        header = self.__createHeader(self.tr("Flash Memory"))
        QTreeWidgetItem(header, [
            self.tr("total"),
            self.tr("{0} KBytes").format(
                loc.toString(data["flash_total_kb"], "f", 0))
        ])
        QTreeWidgetItem(header, [
            self.tr("used"),
            self.tr("{0} KBytes ({1}%)").format(
                loc.toString(data["flash_used_kb"], "f", 0),
                loc.toString(data["flash_used_pc"], "f", 2))
        ])
        QTreeWidgetItem(header, [
            self.tr("free"),
            self.tr("{0} KBytes ({1}%)").format(
                loc.toString(data["flash_free_kb"], "f", 0),
                loc.toString(data["flash_free_pc"], "f", 2))
        ])
        
        header = self.__createHeader(self.tr("µLab"))
        if data["ulab"] is not None:
            QTreeWidgetItem(header, [
                self.tr("Version"),
                data["ulab"]
            ])
        else:
            itm = QTreeWidgetItem(header, [
                self.tr("µLab is not available")
            ])
            itm.setFirstColumnSpanned(True)
        
        for col in range(self.dataTree.columnCount()):
            self.dataTree.resizeColumnToContents(col)
    
    def __createHeader(self, headerText):
        """
        Private method to create a header item.
        
        @param headerText text for the header item
        @type str
        @return reference to the created header item
        @rtype QTreeWidgetItem
        """
        headerItem = QTreeWidgetItem(self.dataTree, [headerText])
        headerItem.setExpanded(True)
        headerItem.setFirstColumnSpanned(True)
        
        font = headerItem.font(0)
        font.setBold(True)
        
        headerItem.setFont(0, font)
        
        return headerItem
