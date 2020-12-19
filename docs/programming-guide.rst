Programming Guide
=================

This section is a work in progress and suggestions are welcome.


Explict Event Loops
-------------------

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
