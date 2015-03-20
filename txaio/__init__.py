from __future__ import absolute_import

from .interfaces import IFailedFuture

# This is the API
# see tx.py for Twisted implementation
# see aio.py for asyncio/trollius implementation

class config:
    """
    This holds all valid configuration options, accessed as
    class-level variables. For example, if you were using asyncio:

    .. sourcecode:: python

        txaio.config.loop = asyncio.get_event_loop()

    ``loop`` is populated automatically (while importing one of the
    framework-specific libraries) but can be changed before any call
    into this library. Currently, it's only used by :meth:`call_later`
    If using asyncio, you must set this to an event-loop (by default,
    we use asyncio.get_event_loop). If using Twisted, set this to a
    reactor instance (by default we import twisted.internet.reactor)

    ``chain_futures`` if True we behave like Twisted (where a
    callback's return value is passed on to the next) and if False
    like asyncio (where each callback receives the same value). The
    "opposite" framework requires that we insert our own wrapper
    callback. FIXME XXX just for illustration, we don't do this.
    """
    #: the event-loop object to use
    loop = None

    #: if True, return-value of callback used for the next one
    chain_futures = False


__all__ = (
    'using_twisted',            # True if we're using Twisted
    'using_asyncio',            # True if we're using asyncio

    'config',                   # the config class, access via class-level vars

    'create_future',           # create a Future (can be already resolved/errored)
    'as_future',               # call a method, and always return a Future
    'reject',                  # errback a Future
    'resolve',                 # callback a Future
    'add_callbacks',           # add callback and/or errback
    'gather',      # return a Future waiting for several other Futures

    'IFailedFuture',            # describes API for arg to errback()s
)

try:
    from .tx import *
    using_twisted = True
except ImportError:
    try:
        from .aio import *
        using_asyncio = True
    except ImportError:
        raise ImportError("Neither asyncio nor Twisted found.")
