###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import absolute_import

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class IFailedFuture(object):
    """
    This defines the interface for a common object encapsulating a
    failure from either an asyncio task/coroutine or a Twisted
    Deferred.

    An instance implementing this interface is given to any
    ``errback`` callables you provde via :meth:`txaio.add_callbacks`

    It is a subset of Twisted's Failure interface, because on Twisted
    backends it actually *is* a Failure.
    """

    @abc.abstractproperty
    def type(self):
        """
        The type of the exception. Same as the first item returned from
        ``sys.exc_info()``
        """

    @abc.abstractproperty
    def value(self):
        """
        An actual Exception instance. Same as the second item returned from
        ``sys.exc_info()``
        """

    @abc.abstractproperty
    def tb(self):
        """
        A traceback object from the exception. Same as the third item
        returned from ``sys.exc_info()``
        """

    @abc.abstractmethod
    def printTraceback(self, file=None):
        """
        Prints the exception and its traceback to the given ``file``. If
        that is ``None`` (the default) then it is printed to
        ``sys.stderr``.

        XXX this is camelCase because Twisted is; can we change somehow?
        """

    @abc.abstractmethod
    def getErrorMessage(self):
        """
        Return a string describing the error.

        XXX this is camelCase because Twisted is; can we change somehow?
        """

    # XXX anything else make sense? Do we ape the *entire* Failure API?
