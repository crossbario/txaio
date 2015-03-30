import txaio
from contextlib import contextmanager


@contextmanager
def replace_loop(new_loop):
    """
    This is a context-manager that sets the txaio event-loop to the
    one supplied temporarily. It's up to you to ensure you pass an
    event_loop or a reactor instance depending upon asyncio/Twisted.

    Use like so:

    .. sourcecode:: python

        from twisted.internet import task
        with replace_loop(task.Clock()) as fake_reactor:
            f = txaio.call_later(5, foo)
            fake_reactor.advance(10)
            # ...etc
    """

    # setup
    orig = txaio.config.loop
    txaio.config.loop = new_loop

    yield new_loop

    # cleanup
    txaio.config.loop = orig
