# Copyright (c) 2015 Twisted Matrix Laboratories, released under the MIT license
# https://github.com/twisted/twisted/blob/log-booyah-6750-6/twisted/python/compat.py#L279

from __future__ import absolute_import, division

import sys

from io import TextIOBase, IOBase

if sys.version_info < (3, 0):
    _PY3 = False
else:
    _PY3 = True

if _PY3:
    unicode = str
else:
    unicode = unicode


def ioType(fileIshObject, default=unicode):
    """
    Determine the type which will be returned from the given file object's
    read() and accepted by its write() method as an argument.

    In other words, determine whethr the given file is 'opened in text mode'.

    @param fileIshObject: Any object, but ideally one which resembles a file.
    @type fileIshObject: L{object}

    @param default: A default value to return when the type of C{fileIshObject}
        cannot be determined.
    @type default: L{type}

    @return: There are 3 possible return values:

            1. L{unicode}, if the file is unambiguously opened in text mode.

            2. L{bytes}, if the file is unambiguously opened in binary mode.

            3. L{basestring}, if we are on python 2 (the L{basestring} type
               does not exist on python 3) and the file is opened in binary
               mode, but has an encoding and can therefore accept both bytes
               and text reliably for writing, but will return L{bytes} from
               read methods.

            4. The C{default} parameter, if the given type is not understood.

    @rtype: L{type}
    """
    if isinstance(fileIshObject, TextIOBase):
        # If it's for text I/O, then it's for text I/O.
        return unicode
    if isinstance(fileIshObject, IOBase):
        # If it's for I/O but it's _not_ for text I/O, it's for bytes I/O.
        return bytes
    encoding = getattr(fileIshObject, 'encoding', None)
    import codecs
    if isinstance(fileIshObject, (codecs.StreamReader, codecs.StreamWriter)):
        # On StreamReaderWriter, the 'encoding' attribute has special meaning;
        # it is unambiguously unicode.
        if encoding:
            return unicode
        else:
            return bytes
    if not _PY3:
        # Special case: if we have an encoding file, we can *give* it unicode,
        # but we can't expect to *get* unicode.
        if isinstance(fileIshObject, file):
            if encoding is not None:
                return basestring
            else:
                return bytes
        from cStringIO import InputType, OutputType
        from StringIO import StringIO
        if isinstance(fileIshObject, (StringIO, InputType, OutputType)):
            return bytes
    return default
