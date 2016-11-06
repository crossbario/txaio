###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
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

import pytest
import txaio
from txaio.testutil import replace_loop


# XXX can we unify these tests, tx vs aio?
def test_batched_successful_call(framework_aio):
    '''
    batched calls really happen in batches
    '''
    # Trollius doesn't come with this, so won't work on py2
    pytest.importorskip('asyncio.test_utils')
    from asyncio.test_utils import TestLoop

    # XXX I *really* don't get the point of these generators...
    def time_gen():
        yield
        yield
        yield
    new_loop = TestLoop(time_gen)
    calls = []
    with replace_loop(new_loop):
        def foo(*args, **kw):
            calls.append((args, kw))

        batched = txaio.make_batched_timer(5)

        # add 3 calls: first 2 should be in the same bucket, 3rd in
        # another bucket
        batched.call_later(5.1, foo, "first call")
        batched.call_later(9.9, foo, "second call")
        batched.call_later(10.1, foo, "third call")

        # advancing 4.9 seconds: shouldn't have expired from a bucket
        new_loop.advance_time(4.9)
        new_loop._run_once()
        assert len(calls) == 0

        # tick over past first bucket; first two calls should happen
        # (the "5s -> 10s" bucket)
        new_loop.advance_time(0.2)
        new_loop._run_once()
        assert len(calls) == 2
        assert calls[0] == (("first call", ), dict())
        assert calls[1] == (("second call", ), dict())

        # tick into next bucket
        new_loop.advance_time(5)
        new_loop._run_once()
        assert len(calls) == 3
        assert calls[2] == (("third call", ), dict())


def test_batched_cancel(framework_aio):
    '''
    we can cancel uncalled call_laters
    '''
    # Trollius doesn't come with this, so won't work on py2
    pytest.importorskip('asyncio.test_utils')
    from asyncio.test_utils import TestLoop

    def time_gen():
        yield
        yield
        yield
    new_loop = TestLoop(time_gen)
    calls = []

    def foo(*args, **kw):
        calls.append((args, kw))

    with replace_loop(new_loop):
        batched = txaio.make_batched_timer(1)
        call = batched.call_later(2, foo, "a call")

        # advance clock a bit; shouldn't have fired anything yet
        new_loop.advance_time(1.2)
        new_loop._run_once()

        call.cancel()

        # advancing clock past where we "should" get the call, if it
        # were still active.
        new_loop.advance_time(4.0)
        new_loop._run_once()
        assert len(calls) == 0


def test_batched_cancel_too_late(framework_aio):
    '''
    nothing bad happens if we cancel() after the callbacks
    '''
    # Trollius doesn't come with this, so won't work on py2
    pytest.importorskip('asyncio.test_utils')
    from asyncio.test_utils import TestLoop

    def time_gen():
        yield
        yield
        yield
    new_loop = TestLoop(time_gen)
    calls = []

    def foo(*args, **kw):
        calls.append((args, kw))

    with replace_loop(new_loop):
        batched = txaio.make_batched_timer(1)
        call = batched.call_later(2, foo, "a call")

        new_loop.advance_time(2.1)
        new_loop._run_once()
        assert len(calls) == 1
        call.cancel()
        assert len(calls) == 1
        new_loop.advance_time(1)
        new_loop._run_once()
        assert len(calls) == 1
