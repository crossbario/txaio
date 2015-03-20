from six import StringIO
import pytest
import txaio
from mock import patch

from util import run_once, await

# we need implementation-specific tests because we have to do
# implementation-specific mocking of the event-loops

def test_call_later_twisted():
    '''
    Wait for two Futures.
    '''

    pytest.importorskip('twisted')

    from twisted.internet.task import Clock

    reactor = Clock()
    calls = []

    orig = txaio.config.loop
    try:
        txaio.config.loop = reactor

        def foo(*args, **kw):
            calls.append((args, kw))

        delay = txaio.call_later(1, foo, 5, 6, 7, foo="bar")
        assert len(calls) == 0
        reactor.advance(2)

        assert len(calls) == 1
        assert calls[0][0] == (5, 6, 7)
        assert calls[0][1] == dict(foo="bar")

    finally:
        txaio.config.loop = orig
