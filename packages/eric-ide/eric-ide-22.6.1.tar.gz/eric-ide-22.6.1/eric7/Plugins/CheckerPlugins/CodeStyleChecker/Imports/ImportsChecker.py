# -*- coding: utf-8 -*-

# Copyright (c) 2021 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a checker for import statements.
"""

import ast
import copy
import sys


class ImportsChecker:
    """
    Class implementing a checker for import statements.
    """
    Codes = [
        ## Local imports
        "I101", "I102", "I103",
        
        ## Imports order
        "I201", "I202", "I203", "I204",
        
        ## Various other import related
        "I901", "I902", "I903", "I904",
    ]

    def __init__(self, source, filename, tree, select, ignore, expected,
                 repeat, args):
        """
        Constructor
        
        @param source source code to be checked
        @type list of str
        @param filename name of the source file
        @type str
        @param tree AST tree of the source code
        @type ast.Module
        @param select list of selected codes
        @type list of str
        @param ignore list of codes to be ignored
        @type list of str
        @param expected list of expected codes
        @type list of str
        @param repeat flag indicating to report each occurrence of a code
        @type bool
        @param args dictionary of arguments for the various checks
        @type dict
        """
        self.__select = tuple(select)
        self.__ignore = ("",) if select else tuple(ignore)
        self.__expected = expected[:]
        self.__repeat = repeat
        self.__filename = filename
        self.__source = source[:]
        self.__tree = copy.deepcopy(tree)
        self.__args = args
        
        # statistics counters
        self.counters = {}
        
        # collection of detected errors
        self.errors = []
        
        checkersWithCodes = [
            (self.__checkLocalImports, ("I101", "I102", "I103")),
            (self.__checkImportOrder, ("I201", "I202", "I203", "I204")),
            (self.__tidyImports, ("I901", "I902", "I903", "I904")),
        ]
        
        self.__checkers = []
        for checker, codes in checkersWithCodes:
            if any(not (code and self.__ignoreCode(code))
                    for code in codes):
                self.__checkers.append(checker)
    
    def __ignoreCode(self, code):
        """
        Private method to check if the message code should be ignored.

        @param code message code to check for
        @type str
        @return flag indicating to ignore the given code
        @rtype bool
        """
        return (code.startswith(self.__ignore) and
                not code.startswith(self.__select))
    
    def __error(self, lineNumber, offset, code, *args):
        """
        Private method to record an issue.
        
        @param lineNumber line number of the issue
        @type int
        @param offset position within line of the issue
        @type int
        @param code message code
        @type str
        @param args arguments for the message
        @type list
        """
        if self.__ignoreCode(code):
            return
        
        if code in self.counters:
            self.counters[code] += 1
        else:
            self.counters[code] = 1
        
        # Don't care about expected codes
        if code in self.__expected:
            return
        
        if code and (self.counters[code] == 1 or self.__repeat):
            # record the issue with one based line number
            self.errors.append(
                {
                    "file": self.__filename,
                    "line": lineNumber + 1,
                    "offset": offset,
                    "code": code,
                    "args": args,
                }
            )
    
    def run(self):
        """
        Public method to check the given source against miscellaneous
        conditions.
        """
        if not self.__filename:
            # don't do anything, if essential data is missing
            return
        
        if not self.__checkers:
            # don't do anything, if no codes were selected
            return
        
        for check in self.__checkers:
            check()
    
    def getStandardModules(self):
        """
        Public method to get a list of modules of the standard library.
        
        @return set of builtin modules
        @rtype set of str
        """
        try:
            return sys.stdlib_module_names
        except AttributeError:
            return {
                "__future__", "__main__", "_dummy_thread", "_thread", "abc",
                "aifc", "argparse", "array", "ast", "asynchat", "asyncio",
                "asyncore", "atexit", "audioop", "base64", "bdb", "binascii",
                "binhex", "bisect", "builtins", "bz2", "calendar", "cgi",
                "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop",
                "collections", "colorsys", "compileall", "concurrent",
                "configparser", "contextlib", "contextvars", "copy", "copyreg",
                "cProfile", "crypt", "csv", "ctypes", "curses", "dataclasses",
                "datetime", "dbm", "decimal", "difflib", "dis", "distutils",
                "doctest", "dummy_threading", "email", "encodings",
                "ensurepip", "enum", "errno", "faulthandler", "fcntl",
                "filecmp", "fileinput", "fnmatch", "formatter", "fractions",
                "ftplib", "functools", "gc", "getopt", "getpass", "gettext",
                "glob", "grp", "gzip", "hashlib", "heapq", "hmac", "html",
                "http", "imaplib", "imghdr", "imp", "importlib", "inspect",
                "io", "ipaddress", "itertools", "json", "keyword", "lib2to3",
                "linecache", "locale", "logging", "lzma", "mailbox", "mailcap",
                "marshal", "math", "mimetypes", "mmap", "modulefinder",
                "msilib", "msvcrt", "multiprocessing", "netrc", "nis",
                "nntplib", "numbers", "operator", "optparse", "os",
                "ossaudiodev", "parser", "pathlib", "pdb", "pickle",
                "pickletools", "pipes", "pkgutil", "platform", "plistlib",
                "poplib", "posix", "pprint", "profile", "pstats", "pty", "pwd",
                "py_compile", "pyclbr", "pydoc", "queue", "quopri", "random",
                "re", "readline", "reprlib", "resource", "rlcompleter",
                "runpy", "sched", "secrets", "select", "selectors", "shelve",
                "shlex", "shutil", "signal", "site", "smtpd", "smtplib",
                "sndhdr", "socket", "socketserver", "spwd", "sqlite3", "ssl",
                "stat", "statistics", "string", "stringprep", "struct",
                "subprocess", "sunau", "symbol", "symtable", "sys",
                "sysconfig", "syslog", "tabnanny", "tarfile", "telnetlib",
                "tempfile", "termios", "test", "textwrap", "threading", "time",
                "timeit", "tkinter", "token", "tokenize", "trace", "traceback",
                "tracemalloc", "tty", "turtle", "turtledemo", "types",
                "typing", "unicodedata", "unittest", "urllib", "uu", "uuid",
                "venv", "warnings", "wave", "weakref", "webbrowser", "winreg",
                "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc", "zipapp",
                "zipfile", "zipimport", "zlib", "zoneinfo",
            }
    
    #######################################################################
    ## Local imports
    ##
    ## adapted from: flake8-local-import v1.0.6
    #######################################################################
    
    def __checkLocalImports(self):
        """
        Private method to check local imports.
        """
        from .LocalImportVisitor import LocalImportVisitor
        
        visitor = LocalImportVisitor(self.__args, self)
        visitor.visit(copy.deepcopy(self.__tree))
        for violation in visitor.violations:
            if not self.__ignoreCode(violation[1]):
                node = violation[0]
                reason = violation[1]
                self.__error(node.lineno - 1, node.col_offset, reason)
    
    #######################################################################
    ## Import order
    ##
    ## adapted from: flake8-alphabetize v0.0.17
    #######################################################################
    
    def __checkImportOrder(self):
        """
        Private method to check the order of import statements.
        """
        from .ImportNode import ImportNode
        
        errors = []
        imports = []
        importNodes, listNode = self.__findNodes(self.__tree)
        
        # check for an error in '__all__'
        allError = self.__findErrorInAll(listNode)
        if allError is not None:
            errors.append(allError)
        
        for importNode in importNodes:
            if (
                isinstance(importNode, ast.Import) and
                len(importNode.names) > 1
            ):
                # skip suck imports because its already handled by pycodestyle
                continue
            
            imports.append(ImportNode(
                self.__args.get("ApplicationPackageNames", []),
                importNode, self))
        
        lenImports = len(imports)
        if lenImports > 0:
            p = imports[0]
            if p.error is not None:
                errors.append(p.error)
            
            if lenImports > 1:
                for n in imports[1:]:
                    if n.error is not None:
                        errors.append(n.error)
                    
                    if n == p:
                        errors.append((n.node, "I203", str(p), str(n)))
                    elif n < p:
                        errors.append((n.node, "I201", str(n), str(p)))
                    
                    p = n
        
        for error in errors:
            if not self.__ignoreCode(error[1]):
                node = error[0]
                reason = error[1]
                args = error[2:]
                self.__error(node.lineno - 1, node.col_offset, reason, *args)
    
    def __findNodes(self, tree):
        """
        Private method to find all import and import from nodes of the given
        tree.
        
        @param tree reference to the ast node tree to be parsed
        @type ast.AST
        @return tuple containing a list of import nodes and the '__all__' node
        @rtype tuple of (ast.Import | ast.ImportFrom, ast.List | ast.Tuple)
        """
        importNodes = []
        listNode = None
        
        if isinstance(tree, ast.Module):
            body = tree.body
            
            for n in body:
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    importNodes.append(n)
                
                elif isinstance(n, ast.Assign):
                    for t in n.targets:
                        if isinstance(t, ast.Name) and t.id == "__all__":
                            value = n.value

                            if isinstance(value, (ast.List, ast.Tuple)):
                                listNode = value
        
        return importNodes, listNode
    
    def __findErrorInAll(self, node):
        """
        Private method to check the '__all__' node for errors.
        
        @param node reference to the '__all__' node
        @type ast.List or ast.Tuple
        @return tuple containing a reference to the node and an error code
        @rtype rtype tuple of (ast.List | ast.Tuple, str)
        """
        if node is not None:
            actualList = []
            for el in node.elts:
                if isinstance(el, ast.Constant):
                    actualList.append(el.value)
                elif isinstance(el, ast.Str):
                    actualList.append(el.s)
                else:
                    # Can't handle anything that isn't a string literal
                    return None

            expectedList = sorted(actualList)
            if expectedList != actualList:
                return (node, "I204", ", ".join(expectedList))
        
        return None
    
    #######################################################################
    ## Tidy imports
    ##
    ## adapted from: flake8-tidy-imports v4.5.0
    #######################################################################
    
    def __tidyImports(self):
        """
        Private method to check various other import related topics.
        """
        self.__bannedModules = self.__args.get("BannedModules", [])
        self.__banRelativeImports = self.__args.get("BanRelativeImports", "")
        
        ruleMethods = []
        if not self.__ignoreCode("I901"):
            ruleMethods.append(self.__checkUnnecessaryAlias)
        if (
            not self.__ignoreCode("I902") and
            bool(self.__bannedModules)
        ):
            ruleMethods.append(self.__checkBannedImport)
        if (
            (not self.__ignoreCode("I903") and
             self.__banRelativeImports == "parents") or
            (not self.__ignoreCode("I904") and
             self.__banRelativeImports == "true")
        ):
            ruleMethods.append(self.__checkBannedRelativeImports)
        
        for node in ast.walk(self.__tree):
            for method in ruleMethods:
                method(node)
    
    def __checkUnnecessaryAlias(self, node):
        """
        Private method to check unnecessary import aliases.
        
        @param node reference to the node to be checked
        @type ast.AST
        """
        if isinstance(node, ast.Import):
            for alias in node.names:
                if "." not in alias.name:
                    fromName = None
                    importedName = alias.name
                else:
                    fromName, importedName = alias.name.rsplit(".", 1)
                
                if importedName == alias.asname:
                    if fromName:
                        rewritten = "from {0} import {1}".format(
                            fromName, importedName)
                    else:
                        rewritten = "import {0}".format(importedName)
                    
                    self.__error(node.lineno - 1, node.col_offset, "I901",
                                 rewritten)
        
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == alias.asname:
                    rewritten = "from {0} import {1}".format(
                        node.module, alias.name)
                    
                    self.__error(node.lineno - 1, node.col_offset, "I901",
                                 rewritten)
    
    def __checkBannedImport(self, node):
        """
        Private method to check import of banned modules.
        
        @param node reference to the node to be checked
        @type ast.AST
        """
        if not bool(self.__bannedModules):
            return
        
        if isinstance(node, ast.Import):
            moduleNames = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            nodeModule = node.module or ""
            moduleNames = [nodeModule]
            for alias in node.names:
                moduleNames.append("{0}.{1}".format(nodeModule, alias.name))
        else:
            return
        
        # Sort from most to least specific paths.
        moduleNames.sort(key=len, reverse=True)
        
        warned = set()
        
        for moduleName in moduleNames:
            if moduleName in self.__bannedModules:
                if any(mod.startswith(moduleName) for mod in warned):
                    # Do not show an error for this line if we already showed
                    # a more specific error.
                    continue
                else:
                    warned.add(moduleName)
                self.__error(node.lineno - 1, node.col_offset, "I902",
                             moduleName)
    
    def __checkBannedRelativeImports(self, node):
        """
        Private method to check if relative imports are banned.
        
        @param node reference to the node to be checked
        @type ast.AST
        """
        if not self.__banRelativeImports:
            return
        
        elif self.__banRelativeImports == "parents":
            minNodeLevel = 1
            msgCode = "I903"
        else:
            minNodeLevel = 0
            msgCode = "I904"
        
        if (
            self.__banRelativeImports and
            isinstance(node, ast.ImportFrom) and
            node.level > minNodeLevel
        ):
            self.__error(node.lineno - 1, node.col_offset, msgCode)
