import txaio
from contextlib import contextmanager


@contextmanager
def replace_reactor(reactor):
    """
    This is a context-manager that sets the txaio reactor to the one
    supplied temporarily. This also ensures you're running with
    Twisted; the asyncio equivalent is "with_event_loop".
    """
    assert txaio.using_twisted

    # setup
    orig = txaio.config.loop
    txaio.config.loop = reactor

    yield reactor

    # cleanup
    txaio.config.loop = orig
