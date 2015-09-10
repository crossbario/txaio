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

    In your errback you can extract information from an IFailedFuture
    with :meth:`txaio.failure_message` and
    :meth:`txaio.failure_traceback` or use ``.value`` to get the
    Exception instance.

    Depending on other details or methods will probably cause
    incompatibilities between asyncio and Twisted.
    """

    @abc.abstractproperty
    def value(self):
        """
        An actual Exception instance. Same as the second item returned from
        ``sys.exc_info()``
        """
