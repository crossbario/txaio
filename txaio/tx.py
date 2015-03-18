from twisted.python.failure import Failure
from twisted.internet.defer import maybeDeferred, Deferred, DeferredList
from twisted.internet.defer import succeed, fail

from .interfaces import IFailedPromise

from twisted.internet.defer import inlineCallbacks as future_generator
from twisted.internet.defer import returnValue  # XXX how to do in asyncio?


class FailedPromise(IFailedPromise):
    """
    XXX provide an abstract-base-class for IFailedPromise or similar,
    probably. For consistency between asyncio/twisted.

    ...i.e. to be explicit about what methods and variables may be
    used. Currently:

    .type
    .value
    .traceback

    .printTraceback
    """
    pass

FailedPromise.register(Failure)

# API methods for txaio


def create_future():
    return Deferred()


def create_future_success(result):
    return succeed(result)


def create_future_error(error=None):
    if error is None:
        error = create_failure()
    else:
        assert isinstance(error, Failure)
    return fail(error)


def as_future(fun, *args, **kwargs):
    return maybeDeferred(fun, *args, **kwargs)


def resolve_future(future, result=None):
    future.callback(result)


def reject_future(future, error=None):
    if error is None:
        error = create_failure()
    elif isinstance(error, Exception):
        print("FIXME: passing Exception to reject_future")
        error = Failure(error)
    else:
        assert isinstance(error, IFailedPromise)
    future.errback(error)


def create_failure(exception=None):
    """
    Create a Failure instance.

    if ``exception`` is None (the default), we MUST be inside an
    "except" block. This encapsulates the exception into an object
    that implements IFailedPromise
    """
    if exception:
        return Failure(exception)
    return Failure()


def add_future_callbacks(future, callback, errback):
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


def gather_futures(futures, consume_exceptions=True,
                   first_result=False, first_exception=False):
    def completed(res):
        if first_result:
            return res[0]  # XXX really? what if third one fired first?
        rtn = []
        for (ok, value) in res:
            rtn.append(value)
            if not ok and not consume_exceptions:
                value.raiseException()
        return rtn

    def failed(f):
        # This only gets called if fireOnOneErrback=True *and*
        # consume_exceptions=Ture and in that case, the "failure"
        # always contains a FirstError
        assert not consume_exceptions
        assert first_exception
        return f.value.subFailure

    dl = DeferredList(
        list(futures),
        consumeErrors=consume_exceptions,
        fireOnOneCallback=first_result,
        fireOnOneErrback=first_exception
    )
    add_future_callbacks(dl, completed, failed)
    return dl
