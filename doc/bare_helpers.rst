Bare Helper Functions
=====================

The easiest way to use ``txaio`` is via the "bare" helper functions
available via the top-level import or a specific event-loop
implementation. This looks like so:

.. sourcecode:: python

   import txaio               # simple; auto-selects eventloop
   import txaio.tx as txaio   # forces Twisted -- ImportError if not installed
   import txaio.aio as txaio  # forces asyncio (or Trollius on older python)


This then gives you access to the complete ``txaio`` API:

.. sourcecode:: python

    import txaio

    f0 = txaio.create_future()
    f1 = txaio.create_future_success("the answer")
    try:
        raise NameError('foo')
    except:
        # these two APIs can only be called in an "except"
        f2 = txaio.create_future_error()
        # or:
        error = txaio.create_failure()
        f3 = txaio.create_future_error(error)

    f5 = txaio.gather_futures([f0, f1, f2])

    def done(answer):
        assert answer == "the answer"

    def problem(fail):
        fail.printTraceback()  # stderr by default

    txaio.add_future_callbacks(f5, done, problem)
