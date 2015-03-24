from txaio.interfaces import IFailedFuture

# This is the API
# see tx.py for Twisted implementation
# see aio.py for asyncio/trollius implementation


class _Config:
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
    reactor instance (by default we "from twisted.internet import
    reactor" on the first call to call_later)
    """
    #: the event-loop object to use
    loop = None


__all__ = (
    'using_twisted',            # True if we're using Twisted
    'using_asyncio',            # True if we're using asyncio
    'use_twisted',              # sets the library to use Twisted, or exception
    'use_asyncio',              # sets the library to use asyncio, or exception

    'config',                   # the config instance, access via attributes

    'create_future',   # create a Future (can be already resolved/errored)
    'as_future',       # call a method, and always return a Future
    'reject',          # errback a Future
    'resolve',         # callback a Future
    'add_callbacks',   # add callback and/or errback
    'gather',          # return a Future waiting for several other Futures

    'IFailedFuture',            # describes API for arg to errback()s
)


def use_twisted():
    from txaio import tx
    import txaio
    txaio.using_twisted = True
    txaio.using_asyncio = False
    for method_name in __all__:
        if method_name in ['use_twisted', 'use_asyncio']:
            continue
        twisted_method = getattr(tx, method_name)
        setattr(txaio, method_name, twisted_method)


def use_asyncio():
    from txaio import aio
    import txaio
    txaio.using_twisted = False
    txaio.using_asyncio = True
    for method_name in __all__:
        if method_name in ['use_twisted', 'use_asyncio']:
            continue
        twisted_method = getattr(aio, method_name)
        setattr(txaio, method_name, twisted_method)


try:
    from txaio.tx import *  # noqa
    using_twisted = True
except ImportError:
    try:
        from txaio.aio import *  # noqa
        using_asyncio = True
    except ImportError:  # pragma: no cover
        # pragma: no cover
        raise ImportError("Neither asyncio nor Twisted found.")
