# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a node visitor for function type annotations.
"""

#
# The visitor and associated classes are adapted from flake8-future-annotations
# v0.0.4
#

import ast


class AnnotationsFutureVisitor(ast.NodeVisitor):
    """
    Class implementing a node visitor to check __future__ imports.
    """
    SimplifyableTypes = (
        "DefaultDict",
        "Deque",
        "Dict",
        "FrozenSet",
        "List",
        "Optional",
        "Set",
        "Tuple",
        "Union",
        "Type",
    )
    
    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        
        self.__typingAliases = []
        self.__importsFutureAnnotations = False
        
        # e.g. from typing import List, typing.List, t.List
        self.__typingImports = []
    
    def visit_Import(self, node):
        """
        Public method to check imports for typing related stuff.
        
        This looks like:
        import typing
        or
        import typing as t
        
        typing or t will be added to the list of typing aliases.
        
        @param node reference to the AST Import node
        @type ast.Import
        """
        for alias in node.names:
            if alias.name == "typing":
                self.__typingAliases.append("typing")
            if alias.asname is not None:
                self.__typingAliases.append(alias.asname)
        
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """
        Public method to detect the 'from __future__ import annotations'
        import if present.

        If 'from typing import ...' is used, add simplifiable names that were
        imported.
        
        @param node reference to the AST ImportFrom node
        @type ast.ImportFrom
        """
        if node.module == "__future__":
            for alias in node.names:
                if alias.name == "annotations":
                    self.__importsFutureAnnotations = True

        if node.module == "typing":
            for alias in node.names:
                if alias.name in AnnotationsFutureVisitor.SimplifyableTypes:
                    self.__typingImports.append(alias.name)

        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """
        Public method to record simplifiable names.
        
        If 'import typing' or 'import typing as t' is used, add simplifiable
        names that were used later on in the code.
        
        @param node reference to the AST Attribute node
        @type ast.Attribute
        """
        if (
            node.attr in AnnotationsFutureVisitor.SimplifyableTypes and
            isinstance(node.value, ast.Name) and
            node.value.id in self.__typingAliases
        ):
            self.__typingImports.append(f"{node.value.id}.{node.attr}")
        
        self.generic_visit(node)
    
    def importsFutureAnnotations(self):
        """
        Public method to check, if the analyzed code uses future annotation.
        
        @return flag indicatung the use of future annotation
        @rtype bool
        """
        return self.__importsFutureAnnotations
    
    def hasTypingImports(self):
        """
        Public method to check, if the analyzed code includes typing imports.
        
        @return flag indicating the use of typing imports
        @rtype bool
        """
        return bool(self.__typingImports)
    
    def getTypingImports(self):
        """
        Public method to get the list of typing imports.
        
        @return list of typing imports
        @rtype list of str
        """
        return self.__typingImports[:]
