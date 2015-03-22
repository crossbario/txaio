txaio API
=========

The API is identical whether you're using Twisted or asyncio under the
hood. Two ``bool``s are available if you need to know which framework
is in use.


Explicitly Selecting a Framework
--------------------------------

You can simply ``import txaio`` to get an auto-selected framework
(Twisted if available, else asyncio/trollius). If you want to
guarantee one or the other, you can do this:

.. sourcecode:: python

    import txaio               # automatically select framework
    txaio.use_twisted()
    txaio.use_asyncio()

For most cases, a simple ``import txaio`` will be sufficient.


Set an Event Loop / Reactor
---------------------------

You can set ``txaio.config.loop`` to either an EventLoop instance (if
using asyncio) or an explicit reactor (if using Twisted). By defualt,
``reactor`` is imported from ``twisted.internet`` on the first
``call_later`` invocation. For asyncio, ``asyncio.get_event_loop()``
is called at import time.

If you've installed your reactor before ``import txaio`` you shouldn't
need to do anything.

Note that under Twisted, only the ``IReactorTime`` interface is
required.


Test Helpers
------------

There are a few testing utilities available via ``import
txaio.testutils``. For testing delayed calls, you can pass
``twisted.iternet.task.Clock`` as the reactor; see
``test_call_later.py`` for an example.


txaio
-----

.. py:module:: txaio

.. py:data:: using_twisted

    ``True`` only if we're using Twisted as our underlying event framework


.. py:data:: using_asyncio

    ``True`` only if we're using asyncio as our underlying event framework


.. py:function:: use_asyncio()

    Force the use of ``asyncio``.


.. py:function:: use_twisted()

    Force the use of Twisted.


.. py:function:: create_future(value=None, error=None)

    Create and return a new framework-specific future object. On
    asyncio this returns a ``Future``, on Twisted it returns a
    ``Deferred``.

    :param value: if not ``None``, the future is already fulfilled,
        with the given result.

    :param error: if not ``None`` then the future is already failed,
        with the given error.
    :type error: class:`IFailedFuture` or Exception

    :raises ValueError: if both ``value`` and ``error`` are provided.

    :return: under Twisted a :class:`Deferred`, under asyncio a
             :class:`Future`


.. py:function:: as_future(func, *args, **kwargs)

    Call ``func`` with the provided arguments and keyword arguments,
    and always return a Future/Deferred. If ``func`` itself returns a
    future, that is directly returned. If it immediately succeed or
    failed then an already-resolved Future/Deferred is returned instead.

    This allows you to write code that calls functions (e.g. possibly
    provided from user-code) and treat them uniformly. For example:

    .. sourcecode:: python

        p = txaio.as_future(some_function, 1, 2, key='word')
        txaio.add_callbacks(p, do_something, it_failed)

    You therefore don't have to worry if the underlying function was
    itself asynchronous or not -- your code always treats it as async.


.. py:function:: reject(future, error=None)

    Resolve the given future as failed. This will call any errbacks
    registered against this Future/Deferred. On Twisted, the errback
    is called with a bare ``Failure`` instance; on asyncio we provide
    an object that implements ``IFailedFuture`` because there is no
    equivalent in asyncio.

    :param future: an unresolved Deferred/Future as returned by
                    :meth:`create_future`

    :param error: The error to fail the Deferred/Future with. If this
                  is ``None``, ``sys.exc_info()`` is used to create an
                  :class:`txaio.IFailedFuture` (or ``Failure``)
                  wrapping the current exception (so in this case it
                  must be called inside an ``except:`` clause.

    :type error: class:`IFailedFuture` or Exception


.. py:function:: resolve(future, value)

    Resolve the given future with the provided value. This triggers
    any callbacks registered against this Future/Deferred.


.. py:function:: add_callbacks(future, callback, errback):

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


.. py:function:: gather(futures, consume_exceptions=True):

    Returns a new Future that waits for the results from all the
    futures provided.

    The Future/Deferred returned will callback with a list the same
    length as ``futures`` containing either the return value from each
    future, or an IFailedFuture/Failure instance if it failed.

    Note that on Twisted, we use ``DeferredList`` which usually
    returns a list of 2-tuples of (status, value). We do inject a
    callback that unpacks this list to be just the value (or Failure)
    so that your callback can be identical on Twisted and asyncio.
