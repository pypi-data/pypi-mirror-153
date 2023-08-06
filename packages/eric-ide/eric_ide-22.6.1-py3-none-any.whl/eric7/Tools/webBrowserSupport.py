#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2018 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Script to determine the supported web browser variant.

It looks for QtWebEngine. It reports the variant found or the string 'None' if
it is absent.
"""

import sys
import contextlib

variant = "None"

with contextlib.suppress(ImportError):
    from PyQt6 import QtWebEngineWidgets    # __IGNORE_WARNING__
    variant = "QtWebEngine"

print(variant)      # __IGNORE_WARNING_M801__

sys.exit(0)
