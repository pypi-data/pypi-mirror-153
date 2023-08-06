# -*- coding: utf-8 -*-

# Copyright (c) 2002 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a Python lexer with some additional methods.
"""

import re
import contextlib

from PyQt6.Qsci import QsciLexerPython, QsciScintilla

from .SubstyledLexer import SubstyledLexer
import Preferences


class LexerPython(SubstyledLexer, QsciLexerPython):
    """
    Subclass to implement some additional lexer dependant methods.
    """
    def __init__(self, variant="", parent=None):
        """
        Constructor
        
        @param variant name of the language variant (string)
        @param parent parent widget of this lexer
        """
        QsciLexerPython.__init__(self, parent)
        SubstyledLexer.__init__(self)
        
        self.variant = variant
        self.commentString = "#"
        
        self.keywordSetDescriptions = [
            self.tr("Keywords"),
            self.tr("Highlighted identifiers"),
        ]
        
        ##############################################################
        ## default sub-style definitions
        ##############################################################
        
        # list of style numbers, that support sub-styling
        self.baseStyles = [11]
        
        self.defaultSubStyles = {
            11: {
                0: {
                    "Description": self.tr("Standard Library Modules"),
                    "Words": """
 __main__ _dummy_thread _thread abc aifc argparse array ascii ast asynchat
 asyncio asyncore atexit audioop base64 bdb binascii binhex bisect builtins bz2
 calendar cgi cgitb chunk cmath cmd code codecs codeop collections colorsys
 compileall concurrent configparser contextlib contextvars copy copyreg
 cProfile crypt csv ctypes curses dataclasses datetime dbm decimal difflib dis
 distutils doctest email encodings ensurepip enum errno faulthandler fcntl
 filecmp fileinput fnmatch formatter fractions ftplib functools gc getopt
 getpass gettext glob graphlib grp gzip hashlib heapq hmac html http imaplib
 imghdr imp importlib inspect io ipaddress itertools json keyword lib2to3
 linecache locale logging lzma mailbox mailcap marshal math mimetypes mmap
 modulefinder msilib msvcrt multiprocessing netrc nis nntplib numbers opcode
 operator optparse os ossaudiodev parser path pathlib pdb pickle pickletools
 pipes pkgutil platform plistlib poplib posix pprint profile pstats pty pwd
 py_compile pyclbr pydoc queue quopri random re readline reprlib resource
 rlcompleter runpy sched secrets select selectors shelve shlex shutil signal
 site smtpd smtplib sndhdr socket socketserver spwd sqlite3 ssl stat statistics
 string stringprep struct subprocess sunau symbol symtable sys sysconfig syslog
 tabnanny tarfile telnetlib tempfile termios test textwrap threading time
 timeit tkinter token tokenize trace traceback tracemalloc tty turtle
 turtledemo types typing unicodedata unittest urllib uu uuid venv warnings wave
 weakref webbrowser winreg winsound wsgiref xdrlib xml xmlrpc zipapp zipfile
 zipimport zlib zoneinfo""",
                    "Style": {
                        "fore": 0xDD9900,
                        "font_bold": True,
                    }
                },
                1: {
                    "Description": self.tr("__future__ Imports"),
                    "Words": """
 __future__ absolute_import annotations division generators generator_stop
 nested_scopes print_function unicode_literals with_statement""",
                    "Style": {
                        "fore": 0xEE00AA,
                        "font_italic": True,
                    }
                },
                2: {
                    "Description": self.tr("PyQt5/6 Modules"),
                    "Words": """
 PyQt5 PyQt6 Qsci Qt Qt3DAnimation Qt3DCore Qt3DExtras Qt3DInput Qt3DLogic
 Qt3DRender QtBluetooth QtChart QtCharts QtCore QtDataVisualization QtDBus
 QtDesigner QtGui QtHelp QtLocation QtMacExtras QtMultimedia
 QtMultimediaWidgets QtNetwork QtNetworkAuth QtNfc QtOpenGL QtOpenGLWidgets
 QtPositioning QtPrintSupport QtPurchasing QtQml QtQuick QtQuick3D
 QtQuickWidgets QtRemoteObjects QtSensors QtSerialPort QtSql QtSvg QtSvgWidgets
 QtTest QtTextToSpeech QtWebChannel QtWebEngine QtWebEngineCore
 QtWebEngineWidgets QtWebSockets QtWidgets QtWinExtras QtX11Extras QtXml
 QtXmlPatterns sip""",
                    "Style": {
                        "fore": 0x44AADD,
                        "font_bold": True,
                    }
                },
                3: {
                    "Description": self.tr("Cython Specifics"),
                    "Words": "cython pyximport Cython __cinit__ __dealloc__",
                    "Style": {
                        "fore": 0xdd0000,
                        "font_bold": True,
                    }
                },
            },
        }
    
    def language(self):
        """
        Public method to get the lexer language.
        
        @return lexer language (string)
        """
        if not self.variant:
            return QsciLexerPython.language(self)
        else:
            return self.variant
    
    def initProperties(self):
        """
        Public slot to initialize the properties.
        """
        self.setIndentationWarning(
            Preferences.getEditor("PythonBadIndentation"))
        self.setFoldComments(Preferences.getEditor("PythonFoldComment"))
        self.setFoldQuotes(Preferences.getEditor("PythonFoldString"))
        if not Preferences.getEditor("PythonAutoIndent"):
            self.setAutoIndentStyle(QsciScintilla.AiMaintain)
        with contextlib.suppress(AttributeError):
            self.setV2UnicodeAllowed(
                Preferences.getEditor("PythonAllowV2Unicode"))
            self.setV3BinaryOctalAllowed(
                Preferences.getEditor("PythonAllowV3Binary"))
            self.setV3BytesAllowed(Preferences.getEditor("PythonAllowV3Bytes"))
        with contextlib.suppress(AttributeError):
            self.setFoldQuotes(Preferences.getEditor("PythonFoldQuotes"))
            self.setStringsOverNewlineAllowed(
                Preferences.getEditor("PythonStringsOverNewLineAllowed"))
        with contextlib.suppress(AttributeError):
            self.setHighlightSubidentifiers(
                Preferences.getEditor("PythonHighlightSubidentifier"))
    
    def getIndentationDifference(self, line, editor):
        """
        Public method to determine the difference for the new indentation.
        
        @param line line to perform the calculation for (integer)
        @param editor QScintilla editor
        @return amount of difference in indentation (integer)
        """
        indent_width = editor.getEditorConfig('IndentWidth')
        
        lead_spaces = editor.indentation(line)
        
        pline = line - 1
        while pline >= 0 and re.match(r'^\s*(#.*)?$', editor.text(pline)):
            pline -= 1
        
        if pline < 0:
            last = 0
        else:
            previous_lead_spaces = editor.indentation(pline)
            # trailing spaces
            m = re.search(r':\s*(#.*)?$', editor.text(pline))
            last = previous_lead_spaces
            if m:
                last += indent_width
            else:
                # special cases, like pass (unindent) or return (also unindent)
                m = re.search(r'(pass\s*(#.*)?$)|(^[^#]return)',
                              editor.text(pline))
                if m:
                    last -= indent_width
        
        indentDifference = (
            last - lead_spaces
            if (lead_spaces % indent_width != 0 or
                lead_spaces == 0 or
                self.lastIndented != line) else
            -indent_width           # __IGNORE_WARNING_W503__
        )
        
        return indentDifference
    
    def autoCompletionWordSeparators(self):
        """
        Public method to return the list of separators for autocompletion.
        
        @return list of separators (list of strings)
        """
        return ['.']
    
    def isCommentStyle(self, style):
        """
        Public method to check, if a style is a comment style.
        
        @param style style to check (integer)
        @return flag indicating a comment style (boolean)
        """
        return style in [QsciLexerPython.Comment,
                         QsciLexerPython.CommentBlock]
    
    def isStringStyle(self, style):
        """
        Public method to check, if a style is a string style.
        
        @param style style to check (integer)
        @return flag indicating a string style (boolean)
        """
        return style in [QsciLexerPython.DoubleQuotedString,
                         QsciLexerPython.SingleQuotedString,
                         QsciLexerPython.TripleDoubleQuotedString,
                         QsciLexerPython.TripleSingleQuotedString,
                         QsciLexerPython.UnclosedString]
    
    def defaultKeywords(self, kwSet):
        """
        Public method to get the default keywords.
        
        @param kwSet number of the keyword set (integer)
        @return string giving the keywords (string) or None
        """
        if kwSet == 1:
            if self.language() == "Python3":
                import keyword
                keywords = " ".join(keyword.kwlist)
            elif self.language() == "MicroPython":
                keywords = ("False None True and as assert break class "
                            "continue def del elif else except finally for "
                            "from global if import in is lambda nonlocal not "
                            "or pass raise return try while with yield")
            elif self.language() == "Cython":
                keywords = ("False None True and as assert break class "
                            "continue def del elif else except finally for "
                            "from global if import in is lambda nonlocal not "
                            "or pass raise return try while with yield "
                            "cdef cimport cpdef ctypedef")
            else:
                keywords = QsciLexerPython.keywords(self, kwSet)
        else:
            keywords = QsciLexerPython.keywords(self, kwSet)
        
        return keywords
    
    def maximumKeywordSet(self):
        """
        Public method to get the maximum keyword set.
        
        @return maximum keyword set (integer)
        """
        return 2
