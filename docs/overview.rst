Overview
========

Brief History
-------------

This library has been factored out of the `Autobahn|Python`_ WAMP client
library. The ``ApplicationSession`` object from that project therefore
serves as a good example of how to use this library in a complex
use-case.

We are releasing it in the hopes these utilities are useful on their
own to other projects using event-based Python. Only authors of
"library style" code are likely to be interested in this -- new
application code should use your favourite Python asynchronous I/O
platform.


Overview by Example
-------------------

The simplest way to use **txaio** is to ``import txaio`` and use the
helper functions directly. You must select the framework you wish to
use by calling ``txaio.use_twisted()`` or ``txaio.use_asyncio()``
(which means asyncio, or trollius/tuplip if asyncio import fails).

Note that to use this library successfully you *shouldn't* call
methods on futures -- use *only* **txaio** methods to operate on them.

.. sourcecode:: python

    import txaio
    txaio.use_twisted()  # or .use_asyncio()

    def cb(value):
        print("Callback:", value)

    def eb(fail):
        # fail will implement txaio.IFailedFuture
        print("Errback:", txaio.failure_message(fail))
        print(txaio.failure_formatted_traceback(fail))

    f = txaio.create_future()
    txaio.add_callbacks(f, cb, eb)

    # ...other things happen...

    try:
        answer = do_something()
        fail = None
    except Exception:
        fail = txaio.create_failure()

    # the point here is that you "somehow" arrange to call either
    # reject() or resolve() on every future you've created.

    if fail:
        txaio.reject(f, fail)
    else:
        txaio.resolve(f, answer)


.. _restrictions:

Restrictions and Caveats
------------------------

**txaio** is not a new event-based programming solution. It is not a
complete box-set of asynchronous programming tools.

It is **one piece** that *can* help **library authors** to write
cross-event-loop asynchronous code. For example, you'll note that
there's no way to run "the event loop" -- that's up to you.

There is **no support for @coroutine or @inlineCallbacks**
decorators. This is not possible, as asyncio under Python3 introduced
a new syntax (``yield from``) to call into other co-routines. So, you
are stuck with "callback style" code for your cross-platform
library. (Note that *users* of your library can of course use new
Python3 features like ``yield from``, ``async`` and ``await`` in their
own code -- but they do so by explicitly choosing "Python3 and
asyncio" as their platform).

``txaio`` is basically a "lowest common denominator" tool. There is a
minimum of wrapping, etcetera but the library author doesn't get to
use fancy features (e.g. ``@inlineCallbacks``, mutation of returns,
``@coroutine``) of the underlying async platforms.


Futures and Deferreds
---------------------

In most cases asyncio is trying to be "as thin as possible" wrapper
around the different APIs. So, there's nothing wrapping Future or
Deferred -- you get the bare objects. This means that
:func:`txaio.create_future` returns you the native object, which
you then pass to :func:`txaio.add_callbacks`

Similarly, :func:`txaio.call_later` returns the underlying object
(``IDelayedCall`` in Twisted or a ``Handle`` in asyncio). These both
have a ``cancel()`` method, but little else in common.


Callbacks and Errbacks
----------------------

Twisted and asyncio have made different design-decisions. One that
stands out is callbacks, and callback chaining. In Twisted, the return
value from an earlier callback is what gets passed to the next
callback. Similarly, errbacks in Twisted can cancel the error. There
are not equivalent facilities in ``asyncio``: if you add multiple
callbacks, they all get the same value (or exception).

When using **txaio**, **don't depend on chaining**. This means that
your ``callback`` and ``errback`` methods must **always return their
input argument** so that Twisted works if you add multiple callbacks
or errbacks (and doesn't unexpectedly cancel errors).

**txaio** does add the concept of an ``errback`` for handling errors
(a concept asyncio does not have) and therefore adds one helper to
encapsulate exceptions (similar to Twisted's `Failure`_ object) which
only exists in the asyncio implementation.

There is no ``inlineCallbacks`` or ``coroutine`` decorator
support. Don't use these.


Error Handling
--------------

In your ``errback``, you will receive a single arg which is an
instance conforming to ``IFailedFuture``. This interface has only a
single attribute: ``.value``, which is the Exception instance which
caused the error. You can also use ``txaio.failure_*`` methods to
operate on an ``IFailedFuture``:

 - txaio.failure_message: returns a unicode error-message
 - txaio.failure_traceback: returns a ``traceback`` object
 - txaio.failure_formatted_traceback: returns a unicode formatted stack-trace

You should **not** depend on *any* other attributes or methods of the
instance you're given.


Real Examples
-------------

You are encouraged to look at `Autobahn|Python`_ for an example of a
system that can run on both Twisted and asyncio. In particular, look
at the difference between ``autobahn/twisted/websocket.py`` and
``autobahn/asyncio/websocket.py`` and the compatibility super-class in
``autobahn/wamp/protocol.py`` which is the piece that uses **txaio**
to provide an event-loop agnostic implementation that both the Twisted
and asyncio concrete ``ApplicationSession`` objects inherit from.

``autobahn.wamp.protocol.ApplicationSession`` is glued to a particular
event-loop via ``autobahn.twisted.wamp.ApplicationSession`` which
takes advantage of ``txaio.tx.LoopMixin`` to provide the
helpers-methods attached to ``self``.

In this manner, code in the generic implementation simply always calls
**txaio** methods via ``self.create_future()`` or similar and users of
`Autobahn|Python`_ can choose between asyncio and Twisted as they prefer
by either ``from autobahn.twisted.wamp import ApplicationSession`` or
``from autobahn.asyncio.wamp import ApplicationSession``


Cross-API Magic
---------------

If you wish to write Twisted-like code that uses ``asyncio`` as its
event-loop, you should look at `txtulip
<https://github.com/itamarst/txtulip>`_. I do not know of a project
that lets you write asyncio-like code that runs on Twisted's
event-loop.


.. _Autobahn|Python: http://autobahn.ws/python/
.. _Failure: https://twistedmatrix.com/documents/current/api/twisted.python.failure.Failure.html
