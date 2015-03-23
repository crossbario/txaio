txaio: Twisted/asyncio helper
=============================

``txaio`` is a helper library for writing code that runs on both
Twisted and asyncio.

This is like `six`_, but for wrapping over differences between Twisted
and asyncio so one can write code that runs unmodified on both (aka
"source code compatibility").

.. _six: http://pythonhosted.org/six/

    Note that, with this approach, user code runs under the native
    event loop of either Twisted or asyncio. This is different from
    attaching either one's event loop to the other using some event
    loop adapter.

Brief Summary
-------------

Instead of directly importing, instantiating and using ``Deferred``
(for Twisted) or ``Future`` (for asyncio) objects, ``txaio`` provides
helper-functions to do that for you, as well as associated things like
adding callbacks or errbacks.

This obviously changes the style of your code, but then you can choose
at runtime (or import time) which underlying event-loop to use. This
means you can write **one** code-base that can run on Twisted *or*
asyncio (without a Twisted dependency) as you (or your users) see fit.

Code like the following can then run on *either* system:

.. sourcecode:: python

    f0 = txaio.create_future()
    f1 = txaio.as_future(some_func, 1, 2, key='word')
    txaio.add_callbacks(f0, callback, errback)
    txaio.add_callbacks(f1, callback, errback)
    # ...
    txaio.resolve(f0, "value")
    txaio.reject(f1, RuntimeError("it failed"))


See :ref:`restrictions` for limitations.

.. toctree::
   :maxdepth: 3

   overview
   api
