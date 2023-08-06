# -*- coding: utf-8 -*-

# Copyright (c) 2014 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing mimetype dependent functions.
"""

import mimetypes

import Preferences


def isTextFile(filename):
    """
    Function to test, if the given file is a text (i.e. editable) file.
    
    @param filename name of the file to be checked
    @type str
    @return flag indicating an editable file
    @rtype bool
    """
    type_ = mimetypes.guess_type(filename)[0]
    return (
        type_ is None or
        type_.split("/")[0] == "text" or
        type_ in Preferences.getUI("TextMimeTypes")
    )


def mimeType(filename):
    """
    Function to get the mime type of a file.
    
    @param filename name of the file to be checked
    @type str
    @return mime type of the file
    @rtype str
    """
    return mimetypes.guess_type(filename)[0]
