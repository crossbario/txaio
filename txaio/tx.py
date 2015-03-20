from twisted.python.failure import Failure
from twisted.internet.defer import maybeDeferred, Deferred, DeferredList
from twisted.internet.defer import succeed, fail

from .interfaces import IFailedFuture

from twisted.internet.defer import inlineCallbacks as future_generator
from twisted.internet.defer import returnValue  # XXX how to do in asyncio?


using_twisted = True
using_asyncio = False


class FailedFuture(IFailedFuture):
    """
    XXX provide an abstract-base-class for IFailedFuture or similar,
    probably. For consistency between asyncio/twisted.

    ...i.e. to be explicit about what methods and variables may be
    used. Currently:

    .type
    .value
    .traceback

    .printTraceback
    """
    pass


FailedFuture.register(Failure)


def create_future(result=None, error=None):
    if result == None and error == None:
        return Deferred()
    elif result != None:
        return create_future_success(result)
    elif error != None:
        return create_future_error(error)
    else:
        raise ValueError("Cannot have both result and error.")

# maybe delete, just use create_future()
def create_future_success(result):
    return succeed(result)


# maybe delete, just use create_future()
def create_future_error(error=None):
    if error is None:
        error = create_failure()
    else:
        assert isinstance(error, Failure)
    return fail(error)


# maybe rename to call()?
def as_future(fun, *args, **kwargs):
    return maybeDeferred(fun, *args, **kwargs)


def resolve(future, result=None):
    future.callback(result)


def reject(future, error=None):
    if error is None:
        error = create_failure()
    elif isinstance(error, Exception):
        print("FIXME: passing Exception to reject_future")
        error = Failure(error)
    else:
        assert isinstance(error, IFailedFuture)
    future.errback(error)


def create_failure(exception=None):
    """
    Create a Failure instance.

    if ``exception`` is None (the default), we MUST be inside an
    "except" block. This encapsulates the exception into an object
    that implements IFailedFuture
    """
    if exception:
        return Failure(exception)
    return Failure()


def add_callbacks(future, callback, errback):
    """
    callback or errback may be None, but at least one must be
    non-None.
    """
    assert future is not None
    if callback is None:
        assert errback is not None
        future.addErrback(errback)
    else:
        # Twisted allows errback to be None here
        future.addCallbacks(callback, errback)
    return future


def gather(futures, consume_exceptions=True):
    def completed(res):
        rtn = []
        for (ok, value) in res:
            rtn.append(value)
            if not ok and not consume_exceptions:
                value.raiseException()
        return rtn

    dl = DeferredList(list(futures), consumeErrors=consume_exceptions)
    # we unpack the (ok, value) tuples into just a list of values
    add_callback(dl, completed)
    return dl
