# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing utility functions for the code style checker dialogs.
"""

import UI.PixmapCache


def setItemIcon(itm, column, msgCode, severity=None):
    """
    Function to set the icon of the passed message item.
    
    @param itm reference to the message item
    @type QTreeWidgetItem
    @param column column for the icon
    @type int
    @param msgCode message code
    @type str
    @param severity severity for message code 'S' (defaults to None)
    @type str (optional)
    """
    if msgCode.startswith(("W", "-", "C", "M")):
        itm.setIcon(column, UI.PixmapCache.getIcon("warning"))
    elif msgCode.startswith("E"):
        itm.setIcon(column, UI.PixmapCache.getIcon("syntaxError"))
    elif msgCode.startswith(("A", "N")):
        itm.setIcon(column, UI.PixmapCache.getIcon("namingError"))
    elif msgCode.startswith("D"):
        itm.setIcon(column, UI.PixmapCache.getIcon("docstringError"))
    elif msgCode.startswith("I"):
        itm.setIcon(column, UI.PixmapCache.getIcon("imports"))
    elif msgCode.startswith("P"):
        itm.setIcon(column, UI.PixmapCache.getIcon("dirClosed"))
    elif msgCode.startswith("Y"):
        itm.setIcon(column, UI.PixmapCache.getIcon("filePython"))
    elif msgCode.startswith("S"):
        if severity is None:
            itm.setIcon(column, UI.PixmapCache.getIcon("securityLow"))
        else:
            if severity == "H":
                itm.setIcon(column, UI.PixmapCache.getIcon("securityLow"))
            elif severity == "M":
                itm.setIcon(column, UI.PixmapCache.getIcon("securityMedium"))
            elif severity == "L":
                itm.setIcon(column, UI.PixmapCache.getIcon("securityHigh"))
            else:
                itm.setIcon(column, UI.PixmapCache.getIcon("securityLow"))
    else:
        # unknown category prefix => warning
        itm.setIcon(column, UI.PixmapCache.getIcon("warning"))
