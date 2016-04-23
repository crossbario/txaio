API
===

The API is identical whether you're using Twisted or asyncio under the
hood. Two ``bool`` variables are available if you need to know which
framework is in use, and two helpers to enforce one or the other framework.


Explicitly Selecting a Framework
--------------------------------

Until you explicitly select a framework, all txaio API methods just
throw a usage error. So, you must call ``.use_twisted()`` or
``.use_asyncio()`` as appropriate. These will fail with
``ImportError`` if you don't have the correct dependencies.

.. sourcecode:: python

    import txaio
    txaio.use_twisted()
    txaio.use_asyncio()


Set an Event Loop / Reactor
---------------------------

You can set ``txaio.config.loop`` to either an EventLoop instance (if
using asyncio) or an explicit reactor (if using Twisted). By default,
``reactor`` is imported from ``twisted.internet`` on the first
``call_later`` invocation. For asyncio, ``asyncio.get_event_loop()``
is called at import time.

If you've installed your reactor before ``import txaio`` you shouldn't
need to do anything.

Note that under Twisted, only the `IReactorTime`_ interface is
required.


Test Helpers
------------

Test utilities are in ``txaio.testutil``. There is a context-manager
for testing delayed calls; see ``test_call_later.py`` for an example.

.. automodule:: txaio.testutil


txaio module
------------

.. py:module:: txaio

.. py:data:: using_twisted

    ``True`` only if we're using Twisted as our underlying event framework


.. py:data:: using_asyncio

    ``True`` only if we're using asyncio as our underlying event framework


.. py:function:: use_asyncio()

    Select ``asyncio`` framework (uses trollius/tulip on Pythons that lack asyncio).


.. py:function:: use_twisted()

    Select the Twisted framework (will fail if Twisted is not installed).


.. py:function:: create_future(value=None, error=None)

    Create and return a new framework-specific future object. On
    asyncio this returns a `Future`_, on Twisted it returns a
    `Deferred`_.

    :param value: if not ``None``, the future is already fulfilled,
        with the given result.

    :param error: if not ``None`` then the future is already failed,
        with the given error.
    :type error: class:`IFailedFuture` or Exception

    :raises ValueError: if both ``value`` and ``error`` are provided.

    :return: under Twisted a `Deferred`_, under asyncio a `Future`_


.. py:function:: as_future(func, *args, **kwargs)

    Call ``func`` with the provided arguments and keyword arguments,
    and always return a `Future`_/`Deferred`_. If ``func`` itself
    returns a future, that is directly returned. If it immediately
    succeed or failed then an already-resolved `Future`_/`Deferred`_
    is returned instead.

    This allows you to write code that calls functions (e.g. possibly
    provided from user-code) and treat them uniformly. For example:

    .. sourcecode:: python

        p = txaio.as_future(some_function, 1, 2, key='word')
        txaio.add_callbacks(p, do_something, it_failed)

    You therefore don't have to worry if the underlying function was
    itself asynchronous or not -- your code always treats it as asynchronous.


.. py:function:: reject(future, error=None)

    Resolve the given future as failed. This will call any errbacks
    registered against this Future/`Deferred`_. On Twisted, the errback
    is called with a bare `Failure`_ instance; on asyncio we provide
    an object that implements ``IFailedFuture`` because there is no
    equivalent in asyncio (this mimics part of the Failure API).

    :param future: an unresolved `Deferred`_/`Future`_ as returned by
                    :meth:`create_future`

    :param error: The error to fail the `Deferred`_/`Future`_ with. If this
                  is ``None``, ``sys.exc_info()`` is used to create an
                  :class:`txaio.IFailedFuture` (or `Failure`_)
                  wrapping the current exception (so in this case it
                  must be called inside an ``except:`` clause).

    :type error: :class:`IFailedFuture` or :class:`Exception`


.. py:function:: resolve(future, value)

    Resolve the given future with the provided value. This triggers
    any callbacks registered against this `Future`_/`Deferred`_.


.. py:function:: add_callbacks(future, callback, errback)

    Adds the provided callback and/or errback to the given future. To
    add multiple callbacks, call this method multiple times. For
    example, to add just an errback, call ``add_callbacks(p, None,
    my_errback)``

    Note that ``txaio`` doesn't do anything special with regards to
    callback or errback chaining -- it is highly recommended that you
    always return the incoming argument unmodified in your
    callback/errback so that Twisted and asyncio behave the same. For
    example:

    .. sourcecode:: python

        def callback_or_errback(value):
            # other code
            return value

    :raises ValueError: if both callback and errback are None

.. py:function:: failure_message(fail)

    Takes an :class:`txaio.IFailedFuture` instance and returns a
    formatted message suitable to show to a user. This will be a
    ``str`` with no newlines for the form: ``{exception_name}:
    {error_message}`` where ``error_message`` is the result of running
    ``str()`` on the exception instance (under asyncio) or the result
    of ``.getErrorMessage()`` on the Failure under Twisted.


.. py:function:: failure_traceback(fail)

    Take an :class:`txaio.IFailedFuture` instance and returns the
    Python ``traceback`` instance associated with the failure.


.. py:function:: failure_format_traceback(fail):

    Take an :class:`txaio.IFailedFuture` instance and returns a
    formatted string showing the traceback. Typically, this will have
    many newlines in it and look like a "normal" Python traceback.


.. py:function:: call_later(delay, func, *args, **kwargs)

    This calls the function ``func`` with the given parameters at the
    specified time in the future. Although asyncio doesn't directly
    support kwargs with ``loop.call_later`` we wrap it in a
    ``functools.partial``, as asyncio documentation suggests.

    Note: see :func:`txaio.make_batched_timer` if you may have a lot
    of timers, and their absolute accuracy isn't very important.

    :param delay: how many seconds in the future to make the call

    :returns: The underlying library object, which will at least have
              a ``.cancel()`` method on it. It's really
              `IDelayedCall`_ in Twisted and a `Handle`_ in asyncio.


.. py:function:: make_batched_timer(seconds_per_bucket, chunk_size)

    This returns an object implementing :class:`txaio.IBatchedTimer`
    such that any ``.call_later`` calls done through it (instead of
    via :meth:`txaio.call_later`) will be "quantized" into buckets and
    processed in ``chunk_size`` batches "near" the time they are
    supposed to fire. ``seconds_per_bucket`` is only accurate to
    "milliseconds".

    When there are "tens of thousands" of outstanding timers, CPU
    usage can become a problem -- if the accuracy of the timers isn't
    very important, using "batched" timers can greatly reduce the
    number of "real" delayed calls in the event loop.

    For example, Autobahn uses this feature for auto-ping timeouts,
    where the exact time of the event isn't extremely important -- but
    there are 2 outstanding calls per connection.


.. py:function:: gather(futures, consume_exceptions=True)

    Returns a new `Future`_ that waits for the results from all the
    futures provided.

    The `Future`_/`Deferred`_ returned will callback with a list the
    same length as ``futures`` containing either the return value from
    each future, or an :class:`IFailedFuture`/`Failure`_ instance if
    it failed.

    Note that on Twisted, we use `DeferredList`_ which usually
    returns a list of 2-tuples of ``(status, value)``. We do inject a
    callback that unpacks this list to be just the value (or
    `Failure`_) so that your callback can be identical on Twisted and
    asyncio.


.. py:function:: make_logger()

    Creates and returns an instance of :class:`ILogger`. This can pick
    up context from where it's instantiated (e.g. the containing class
    or module) so the best way to use this is to create a logger for
    each class that produces logs; see the example in
    :class:`ILogger` 's documentation


.. autoclass:: txaio.interfaces.ILogger
.. autoclass:: txaio.interfaces.IFailedFuture


.. _Autobahn|Python: http://autobahn.ws/python/
.. _Deferred: https://twistedmatrix.com/documents/current/api/twisted.internet.defer.Deferred.html
.. _DeferredList: https://twistedmatrix.com/documents/current/api/twisted.internet.defer.DeferredList.html
.. _Failure: https://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
.. _IDelayedCall: https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IDelayedCall.html
.. _IReactorTime: https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IReactorTime.html

.. _Handle: https://docs.python.org/3.4/library/asyncio-eventloop.html#asyncio.Handle
.. _Future: https://docs.python.org/3.4/library/asyncio-task.html#asyncio.Future
