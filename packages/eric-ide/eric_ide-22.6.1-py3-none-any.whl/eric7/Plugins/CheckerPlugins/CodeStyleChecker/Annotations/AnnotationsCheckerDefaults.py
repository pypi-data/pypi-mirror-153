# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing complex defaults for the annotations checker.
"""

AnnotationsCheckerDefaultArgs = {
    # Annotations
    "SuppressNoneReturning": False,
    "SuppressDummyArgs": False,
    "AllowUntypedDefs": False,
    "AllowUntypedNested": False,
    "MypyInitReturn": False,
    "DispatchDecorators": ["singledispatch", "singledispatchmethod"],
    "OverloadDecorators": ["overload"],
    
    # Annotation Coverage
    "MinimumCoverage": 75,      # % of type annotation coverage
    
    # Annotation Complexity
    "MaximumComplexity": 3,
    "MaximumLength": 7,
}
