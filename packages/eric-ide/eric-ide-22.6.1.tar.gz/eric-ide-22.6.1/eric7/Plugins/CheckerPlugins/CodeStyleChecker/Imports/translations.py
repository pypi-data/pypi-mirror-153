# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing message translations for the code style plugin messages
(import statements part).
"""

from PyQt6.QtCore import QCoreApplication

_importsMessages = {
    "I101": QCoreApplication.translate(
        "ImportsChecker",
        "local import must be at the beginning of the method body"),
    "I102": QCoreApplication.translate(
        "ImportsChecker",
        "packages from external modules should not be imported locally"),
    "I103": QCoreApplication.translate(
        "ImportsChecker",
        "packages from standard modules should not be imported locally"),
    
    "I201": QCoreApplication.translate(
        "ImportsChecker",
        "Import statements are in the wrong order. "
        "'{0}' should be before '{1}'"),
    "I202": QCoreApplication.translate(
        "ImportsChecker",
        "Imported names are in the wrong order. "
        "Should be '{0}'"),
    "I203": QCoreApplication.translate(
        "ImportsChecker",
        "Import statements should be combined. "
        "'{0}' should be combined with '{1}'"),
    "I204": QCoreApplication.translate(
        "ImportsChecker",
        "The names in __all__ are in the wrong order. "
        "The order should be '{0}'"),
    
    "I901": QCoreApplication.translate(
        "ImportsChecker",
        "unnecessary import alias - rewrite as '{0}'"),
    "I902": QCoreApplication.translate(
        "ImportsChecker",
        "banned import '{0}' used"),
    "I903": QCoreApplication.translate(
        "ImportsChecker",
        "relative imports from parent modules are banned"),
    "I904": QCoreApplication.translate(
        "ImportsChecker",
        "relative imports are banned"),
}

_importsMessagesSampleArgs = {
    "I201": ["import bar", "import foo"],
    "I202": ["bar, baz, foo"],
    "I203": ["from foo import bar", "from foo import baz"],
    "I204": ["bar, baz, foo"],
    "I901": ["from foo import bar"],
    "I902": ["foo"],
}
