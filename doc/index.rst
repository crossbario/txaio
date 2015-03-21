txaio: Twisted/asyncio helper
=============================

``txaio`` is a helper library for writing code that runs on both
Twisted and asyncio.

Instead of directly importing, instantiating and using ``Deferred``
(for Twisted) or ``Future`` (for asyncio) objects, ``txaio`` provides
helper-functions to do that for you, as well as associated things like
adding callbacks or errbacks.

This obviously changes the style of your code, but then you can choose
at runtime (or import time) which underlying event-loop to use. This
means you can write **one** code-base that can run on Twisted *or*
asyncio as you (or your users) see fit.

There are restrictions; see below.


Brief History
-------------

This library has been factored out of the Autobahn|Python WAMP client
library. The ``ApplicationSession`` object from that project therefore
serves as a good example of how to use this library in a complex
use-case. See https://github.com/tavendo/AutobahnPython/blob/master/autobahn/wamp/protocol.py#L410

We are releasing it in the hopes these utilities are useful on their
own to other projects using event-based Python.


Overview by Example
-------------------

The simplest way to use ``txaio`` is to simply ``import txaio`` and
use the helper functions directly. Using the library in this manner will
automatically select the event-loop to use: Twisted if it's available,
then asyncio and finally Trollius if those fail.

If you wish to be explicit about the event-loop you want, you can
import a specific implementation like: ``import txaio.tx as txaio``
for Twisted or ``import txaio.aio as txaio`` for asyncio (the latter
will automatically select Trollius if asyncio isn't available).

Note that to use this library successfully you **must not** call
methods on Promises -- use *only* ``txaio`` methods to operate on
them.

.. sourcecode:: python

    import txaio

    def cb(value):
        print("Callback:", value)

    def eb(fail):
        # fail will implement txaio.IFailedPromise
        print("Errback:", fail)
        fail.printTraceback()

    f = txaio.create_future()
    txaio.add_future_callbacks(f, cb, eb)

    # ...other things happen...

    try:
        answer = do_something()
        fail = None
    except Exception:
        fail = txaio.create_failure()

    if fail:
        txaio.reject_future(f, fail)
    else:
        txaio.resolve_future(f, answer)


Restrictions and Caveats
------------------------

``txaio`` is not a new event-based programming solution. It is not a
complete box-set of async tools.

It is **one piece** that *can* help you to write cross-event-loop
asynchronous code. For example, you'll note that there's no way to run
"the event loop" -- that's up to you.

In most cases asyncio is trying to be "as thin as possible" wrapper
around the different APIs. So, there's nothing wrapping Future or
Deferred -- you get the bare objects. So
py:meth:`txaio.create_future`` returns you the native object, which
you then pass to ``txaio.add_callbacks``.

Similarly, py:meth:`txaio.call_later` returns the underlying object
(IDelayedCall in Twisted or a Handle in asyncio). These both have a
``cancel()`` method.

Twisted and asyncio have made different design-decisions for some
cases. One that stands out is callbacks, and callback chaining. In
Twisted, the return value from an earlier callback is what gets passed
to the next callback. Similarly, errbacks in Twisted can cancel the
error. There are not equivalent facilities in asyncio: if you add
multiple callbacks, they all get the same value (or exception).

So: **don't depend on chaining**. This means that your ``callback``
and ``errback`` methods must **always return their input argument** so
that Twisted works if you add multiple callbacks or errbacks (and
doesn't unexpectedly cancel errors).

We do add the concept of an ``errback`` for handling errors (which
asyncio does not have) and therefore have one helper to encapsulate
exceptions (similar to Twisted's ``Failure`` object) which only exists
in the asyncio implementation.


Real Examples
-------------

You are encouraged to look at Autobahn|Python for an example of a
system that can run on both Twisted and asyncio. In particular, look
at the difference between ``autobahn/twisted/websocket.py`` and
``autobahn/asyncio/websocket.py`` and the compatibility super-class in
``autobahn/wamp/protocol.py`` which is the piece that uses ``txaio``
to provide an event-loop agnostic implementation that both the Twisted
and asyncio concrete ``ApplicationSession`` objects inherit from.

``autobahn.wamp.protocol.ApplicationSession`` is glued to a particular
event-loop via ``autobahn.twisted.wamp.ApplicationSession`` which
takes advantage of ``txaio.tx.LoopMixin`` to provde the
helpers-methods attached to ``self``.

In this manner, code in the generic implementation simply always calls
``txaio`` methods via ``self.create_future()`` or similar and users of
Autobahn|Python can choose between asyncio and Twisted as they prefer
by either ``from autobahn.twisted.wamp import ApplicationSession`` or
``from autobahn.asyncio.wamp import ApplicationSession``



Contents:

.. toctree::
   :maxdepth: 2

   bare_helpers
   mixin_classes
   api


.. comment:
    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

