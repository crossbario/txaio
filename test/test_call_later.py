import pytest
import txaio
from txaio.testutil import replace_loop


def test_call_later():
    '''
    Wait for two Futures.
    '''

    # set up a test reactor or event-loop depending on asyncio or
    # Twisted
    twisted = False
    try:
        from twisted.internet.task import Clock
        new_loop = Clock()
        twisted = True
    except ImportError:
        # Trollius doesn't come with this, so won't work on py2
        pytest.importorskip('asyncio.test_utils')

        def time_gen():
            when = yield
            assert when == 1
            # even though we only do one call, I guess TestLoop needs
            # a "trailing" yield? "or something"
            when = yield 0
            print("Hmmm", when)
        from asyncio.test_utils import TestLoop
        new_loop = TestLoop(time_gen)

    calls = []
    with replace_loop(new_loop) as fake_loop:
        def foo(*args, **kw):
            calls.append((args, kw))

        delay = txaio.call_later(1, foo, 5, 6, 7, foo="bar")
        assert len(calls) == 0
        assert hasattr(delay, 'cancel')
        if twisted:
            fake_loop.advance(2)
        else:
            # XXX maybe we monkey-patch a ".advance()" onto asyncio
            # loops that does both of these?
            fake_loop.advance_time(2)
            fake_loop._run_once()

        assert len(calls) == 1
        assert calls[0][0] == (5, 6, 7)
        assert calls[0][1] == dict(foo="bar")
