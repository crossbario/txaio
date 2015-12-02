###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from mock import patch

import pytest
import txaio
from txaio.testutil import replace_loop


def test_default_reactor(framework_tx):
    """
    run the code that defaults txaio.config.loop
    """
    pytest.importorskip('twisted')

    assert txaio.config.loop is None
    try:
        txaio.call_later(1, lambda: None)

        from twisted.internet import reactor
        assert txaio.config.loop is reactor
    finally:
        txaio.config.loop = None


def test_explicit_reactor_future(framework):
    """
    If we set an event-loop, Futures + Tasks should use it.
    """
    pytest.importorskip('asyncio')
    if txaio.using_twisted:
        pytest.skip()

    with patch.object(txaio.config, 'loop') as fake_loop:
        f = txaio.create_future('result')
        f.add_done_callback(lambda _: None)

        assert len(fake_loop.method_calls) == 2
        c = fake_loop.method_calls[1]
        assert c[0] == 'call_soon'


def test_explicit_reactor_coroutine(framework):
    """
    If we set an event-loop, Futures + Tasks should use it.
    """
    pytest.importorskip('asyncio')
    if txaio.using_twisted:
        pytest.skip()

    from asyncio import coroutine

    @coroutine
    def some_coroutine():
        yield 'nothing'

    with patch.object(txaio.config, 'loop') as fake_loop:
        txaio.as_future(some_coroutine)

        assert len(fake_loop.method_calls) == 2
        c = fake_loop.method_calls[1]
        assert c[0] == 'call_soon'


def test_call_later_tx(framework_tx):
    '''
    Wait for two Futures.
    '''

    from twisted.internet.task import Clock
    new_loop = Clock()
    calls = []
    with replace_loop(new_loop) as fake_loop:
        def foo(*args, **kw):
            calls.append((args, kw))

        delay = txaio.call_later(1, foo, 5, 6, 7, foo="bar")
        assert len(calls) == 0
        assert hasattr(delay, 'cancel')
        fake_loop.advance(2)

        assert len(calls) == 1
        assert calls[0][0] == (5, 6, 7)
        assert calls[0][1] == dict(foo="bar")


def test_call_later_aio(framework_aio):
    '''
    Wait for two Futures.
    '''

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
        fake_loop.advance_time(2)
        fake_loop._run_once()

        assert len(calls) == 1
        assert calls[0][0] == (5, 6, 7)
        assert calls[0][1] == dict(foo="bar")
