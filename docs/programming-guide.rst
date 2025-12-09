Programming Guide
=================

This guide covers the txaio API and common usage patterns.

--------------

Application Programming Interface
---------------------------------

The API is identical whether you're using Twisted or asyncio under the
hood. Two ``bool`` variables are available if you need to know which
framework is in use, and two helpers to enforce one or the other framework.


Explicitly Selecting a Framework
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Until you explicitly select a framework, all txaio API methods just
throw a usage error. So, you must call ``.use_twisted()`` or
``.use_asyncio()`` as appropriate. These will fail with
``ImportError`` if you don't have the correct dependencies.

.. sourcecode:: python

    import txaio
    txaio.use_twisted()
    txaio.use_asyncio()


Set an Event Loop / Reactor
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^

Test utilities are in ``txaio.testutil``. There is a context-manager
for testing delayed calls; see ``test_call_later.py`` for an example.

.. automodule:: txaio.testutil


txaio module
^^^^^^^^^^^^

.. py:module:: txaio

.. py:data:: using_twisted

    ``True`` only if we're using Twisted as our underlying event framework


.. py:data:: using_asyncio

    ``True`` only if we're using asyncio as our underlying event framework


.. py:function:: use_asyncio()

    Select ``asyncio`` framework (uses trollius/tulip on Pythons that lack asyncio).


.. py:function:: use_twisted()

    Select the Twisted framework (will fail if Twisted is not installed).


.. py:function:: create_future(result=None, error=None, canceller=None)

    Create and return a new framework-specific future object. On
    asyncio this returns a `Future`_, on Twisted it returns a
    `Deferred`_.

    :param result: if not ``None``, the future is already fulfilled,
        with the given result.

    :param error: if not ``None`` then the future is already failed,
        with the given error.
    :type error: IFailedFuture or Exception

    :param canceller: a single-argument callable which is invoked if
        this future is cancelled (the single argument is the future
        object which has been cancelled)

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
                  `IFailedFuture` (or `Failure`_)
                  wrapping the current exception (so in this case it
                  must be called inside an ``except:`` clause).

    :type error: IFailedFuture or :class:`Exception`


.. py:function:: cancel(future)

    Cancel the given future. If a ``canceller`` was registered, it is
    invoked now. It is invalid to ``resolve`` or ``reject`` the future
    after cancelling it.

    :param future: an unresolved `Deferred`_/`Future`_ as returned by
                    :meth:`create_future`


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

    Takes an `IFailedFuture` instance and returns a
    formatted message suitable to show to a user. This will be a
    ``str`` with no newlines for the form: ``{exception_name}:
    {error_message}`` where ``error_message`` is the result of running
    ``str()`` on the exception instance (under asyncio) or the result
    of ``.getErrorMessage()`` on the Failure under Twisted.


.. py:function:: failure_traceback(fail)

    Take an `IFailedFuture` instance and returns the
    Python ``traceback`` instance associated with the failure.


.. py:function:: failure_format_traceback(fail):

    Take an `IFailedFuture` instance and returns a
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

    This returns an object implementing `IBatchedTimer`
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
    each future, or an `IFailedFuture`/`Failure`_ instance if
    it failed.

    Note that on Twisted, we use `DeferredList`_ which usually
    returns a list of 2-tuples of ``(status, value)``. We do inject a
    callback that unpacks this list to be just the value (or
    `Failure`_) so that your callback can be identical on Twisted and
    asyncio.


.. py:function:: make_logger()

    Creates and returns an instance of `ILogger`. This can pick
    up context from where it's instantiated (e.g. the containing class
    or module) so the best way to use this is to create a logger for
    each class that produces logs; see the example in
    `ILogger` 's documentation


.. autoclass:: txaio.interfaces.ILogger
.. autoclass:: txaio.interfaces.IFailedFuture

--------------

Explicit Event Loops
--------------------

Twisted has a single, global reactor (for now). As such, txaio was built with a single, global (but configurable) event-loop. However, asyncio supports multiple event-loops.

After version 2.7.0 it is possible to use txaio with multiple event-loops, and thereby offer asyncio users the chance to pass one. Of course, it's still not possible to use multiple event-loops at once with Twisted.

To start using multiple event-loops with txaio, use `txaio.with_config` to return a new "instance" of the txaio API with the given config (the only thing you can configure currently is the event-loop). On Twisted, it's an error if you try to use a different reactor.

The object returned by `txaio.with_config` is a drop-in replacement for every `txaio.*` call, so you can go from code like this::

    import txaio
    f = txaio.create_future()

...and instead make your code do look like this::

    import asyncio
    import txaio
    txa = txaio.with_config(loop=asyncio.new_event_loop())
    f = txa.create_future()

If you're doing this inside a class, you could use ``self._txa`` or similar instead. This gives you an easy path to opt-in to this multiple event-loop API:

   - replace all ``txaio.*`` calls to use an object, like ``self._txa``.

   - assign this to the txaio module (``self._txa = txaio``) or use
     the new API right away (``self._txa = txaio.with_config()``)

   - add a public API to your library to pass in an event loop

   - when this is used, you set ``self._txa = txaio.with_config(loop=loop)``

See the example in ``examples/multiloop.py``.


Logging
-------

If you are developing a new application, you can take advantage of more structured logging by using txaio's APIs throughout. This API is similar to `Twisted's logging <https://twistedmatrix.com/documents/current/core/howto/logger.html>`_ in many ways, but not identical. If you're integrating txaio into existing code, it should "play nicely" with the ``logging`` module, Twisted's newest logger, and the pre-15.2.0 "legacy" Twisted logger.

To create an object suitable for logging, call :func:`txaio.make_logger`. This will return an instance which has a series of methods indicating the "severity" or "level" of the log -- see :class:`txaio.interfaces.ILogger` for an example and more details.

So, given some code like::

    import txaio
    txaio.use_twisted()

    class Bunny(object):
        log = txaio.make_logger()

        def hop(self, times=1):
            self.log.trace("Bunny.hop(times={times})", times=times)
            self.log.debug("Hopping {times} times.", times=times)
            try:
                1 / 0
            except Exception:
                fail = txaio.create_failure()
                self.log.critical(txaio.failure_format_traceback(fail))

    print("output before start_logging")
    txaio.start_logging(level='debug')
    print("output after start_logging")
    jack = Bunny()
    jack.hop(42)

Then you should see output approximately like this::

    output before start_logging
    2016-01-21T01:02:03-0100 output after start_logging
    2016-01-21T01:02:03-0100 Hopping 42 times.
    2016-01-21T01:02:03-0100 Traceback (most recent call last):
      File "logging-example.py", line 21, in <module>
        jack.hop(42)
    --- <exception caught here> ---
      File "logging-example.py", line 12, in hop
        raise RuntimeError("Fox spotted!")
    exceptions.RuntimeError: Fox spotted!


Note that the ``trace``-level message wasn't logged. If you don't like to see full tracebacks except with debugging, you can use this idiom::

    self.log.critical(txaio.failure_message(fail))
    self.log.debug(txaio.failure_format_traceback(fail))

It's worth noting the code doesn't change at all if you do ``.use_asyncio()`` at the top instead -- of course this is the whole point of ``txaio``!


Logging Interoperability
------------------------

When you're using libraries that are already doing logging, but not using the ``txaio`` APIs, you shouldn't need to do anything. For example::

    import txaio
    txaio.use_twisted()


    def existing_code():
        from twisted.python import log
        log.msg("A legacy Twisted logger message")

    txaio.start_logging(level='debug')
    existing_code()

If you're using ``asyncio`` (or just built-in Python logging), it could look like this::

    import txaio
    txaio.use_asyncio()


    def existing_code():
        import logging
        log = logging.getLogger("roy")
        log.info("Python stdlib message: %s", "txaio was here")

    txaio.start_logging(level='debug')
    existing_code()


Starting Logging Yourself
-------------------------

If you are already starting your favourite logging system yourself (be that Twiste'd logger via ``globalLogBeginner`` or Python stdlib logging), any library using txaio's logging should play nicely with it. **Not** ever calling `txaio.start_logging` has a slight drawback, however: as part of setting up logging, we re-bind all the "unused" logging methods to do-nothing. For example, if the log level is set to ``'info'`` than the ``.debug`` method on all txaio-created logger instances becomes a no-op.

For fully-worked examples of this, look in ``examples/log_interop_stdlib.py`` and ``examples/log_interop_twisted.py``.

--------------

.. _Autobahn|Python: http://autobahn.ws/python/
.. _Deferred: https://twistedmatrix.com/documents/current/api/twisted.internet.defer.Deferred.html
.. _DeferredList: https://twistedmatrix.com/documents/current/api/twisted.internet.defer.DeferredList.html
.. _Failure: https://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
.. _IDelayedCall: https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IDelayedCall.html
.. _IReactorTime: https://twistedmatrix.com/documents/current/api/twisted.internet.interfaces.IReactorTime.html

.. _Handle: https://docs.python.org/3.4/library/asyncio-eventloop.html#asyncio.Handle
.. _Future: https://docs.python.org/3.4/library/asyncio-task.html#asyncio.Future
