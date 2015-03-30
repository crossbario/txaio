from __future__ import absolute_import, print_function

import sys
import traceback
import functools

from txaio.interfaces import IFailedFuture
from txaio import _Config

try:
    import asyncio
    from asyncio import iscoroutine
    from asyncio import Future

except ImportError:
    # Trollius >= 0.3 was renamed
    # noinspection PyUnresolvedReferences
    import trollius as asyncio
    from trollius import iscoroutine
    from trollius import Future


config = _Config()
config.loop = asyncio.get_event_loop()

using_twisted = False
using_asyncio = True


class FailedFuture(IFailedFuture):
    """
    This provides an object with any features from Twisted's Failure
    that we might need in Autobahn classes that use FutureMixin.

    We need to encapsulate information from exceptions so that
    errbacks still have access to the traceback (in case they want to
    print it out) outside of "except" blocks.
    """

    def __init__(self, type_, value, traceback):
        """
        These are the same parameters as returned from ``sys.exc_info()``

        :param type_: exception type
        :param value: the Exception instance
        :param traceback: a traceback object
        """
        self._type = type_
        self._value = value
        self._traceback = traceback

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @property
    def tb(self):
        return self._traceback

    def printTraceback(self, file=None):
        """
        Prints the complete traceback to stderr, or to the provided file
        """
        # print_exception handles None for file
        traceback.print_exception(self.type, self.value, self._traceback,
                                  file=file)

    def getErrorMessage(self):
        """
        Returns the str() of the underlying exception.
        """
        return str(self.value)

    def __str__(self):
        return self.getErrorMessage()


# API methods for txaio, exported via the top-level __init__.py


def create_future():
    return Future()


def create_future_success(result):
    f = Future()
    f.set_result(result)
    return f


def create_future_error(error=None):
    if error is None:
        error = create_failure()
    elif isinstance(error, Exception):
        error = FailedFuture(type(error), error, None)
    else:
        assert isinstance(error, IFailedFuture)
    f = Future()
    f.set_exception(error.value)
    return f


# XXX maybe rename to call()?
def as_future(fun, *args, **kwargs):
    try:
        res = fun(*args, **kwargs)
    except Exception:
        return create_future_error(create_failure())
    else:
        if isinstance(res, Future):
            return res
        elif iscoroutine(res):
            return asyncio.Task(res)
        else:
            return create_future_success(res)


def call_later(delay, fun, *args, **kwargs):
    # loop.call_later doesns't support kwargs
    real_call = functools.partial(fun, *args, **kwargs)
    return config.loop.call_later(delay, real_call)


def resolve(future, result):
    future.set_result(result)


def reject(future, error=None):
    if error is None:
        error = create_failure()  # will be error if we're not in an "except"
    elif isinstance(error, Exception):
        error = FailedFuture(type(error), error, None)
    else:
        assert isinstance(error, IFailedFuture)
    future.set_exception(error.value)


def create_failure(exception=None):
    """
    This returns an object implementing IFailedFuture.

    If exception is None (the default) we MUST be called within an
    "except" block (such that sys.exc_info() returns useful
    information).
    """
    if exception:
        return FailedFuture(type(exception), exception, None)
    return FailedFuture(*sys.exc_info())


def add_callbacks(future, callback, errback):
    """
    callback or errback may be None, but at least one must be
    non-None.

    XXX beware the "f._result" hack to get "chainable-callback" type
    behavior.
    """
    def done(f):
        try:
            res = f.result()
            if callback:
                x = callback(res)
                if x is not None:
                    f._result = x
        except Exception:
            if errback:
                errback(create_failure())
    return future.add_done_callback(done)


def gather(futures, consume_exceptions=True):
    """
    This returns a Future that waits for all the Futures in the list
    ``futures``

    :param futures: a list of Futures (or coroutines?)

    :param consume_exceptions: if True, any errors are eaten and
    returned in the result list.
    """

    # from the asyncio docs: "If return_exceptions is True, exceptions
    # in the tasks are treated the same as successful results, and
    # gathered in the result list; otherwise, the first raised
    # exception will be immediately propagated to the returned
    # future."
    return asyncio.gather(*futures, return_exceptions=consume_exceptions)
