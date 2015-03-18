from __future__ import absolute_import

from .interfaces import IFailedPromise

using_twisted = False
using_asyncio = False

try:
    from .aio_twisted import *
    using_twisted = True
except ImportError:
    try:
        from .aio_asyncio import *
        using_asyncio = True
    except ImportError:
        raise ImportError("Neither asyncio nor Twisted found.")

# XXX perhaps put an __all__ here to be explicit?
