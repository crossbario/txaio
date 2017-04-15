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

import txaio
from txaio.testutil import replace_loop


# XXX it would be nice to unify the _tx versus _aio versions of all
# these tests ...
def test_batched_successful_call(framework_tx):
    '''
    '''
    from twisted.internet.task import Clock
    new_loop = Clock()
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
        new_loop.advance(4.9)
        assert len(calls) == 0

        # tick over past first bucket; first two calls should happen
        # (the "5s -> 10s" bucket)
        new_loop.advance(0.2)
        assert len(calls) == 2
        assert calls[0] == (("first call", ), dict())
        assert calls[1] == (("second call", ), dict())

        # tick into next bucket
        new_loop.advance(5)
        assert len(calls) == 3
        assert calls[2] == (("third call", ), dict())


def test_batched_cancel(framework_tx):
    '''
    '''

    from twisted.internet.task import Clock
    new_loop = Clock()
    calls = []

    def foo(*args, **kw):
        calls.append((args, kw))

    with replace_loop(new_loop):
        batched = txaio.make_batched_timer(1)
        call = batched.call_later(2, foo, "a call")

        # advance clock a bit; shouldn't have fired anything yet
        new_loop.advance(1.2)

        call.cancel()

        # advancing clock past where we "should" get the call, if it
        # were still active.
        new_loop.advance(4.0)
        assert len(calls) == 0


def test_batched_cancel_too_late(framework_tx):
    '''
    nothing bad happens if we cancel() after the callbacks
    '''

    from twisted.internet.task import Clock
    new_loop = Clock()
    calls = []

    def foo(*args, **kw):
        calls.append((args, kw))

    with replace_loop(new_loop):
        batched = txaio.make_batched_timer(1)
        call = batched.call_later(2, foo, "a call")

        new_loop.advance(2.1)
        assert len(calls) == 1
        call.cancel()
        assert len(calls) == 1
        new_loop.advance(1)
        assert len(calls) == 1


def test_batched_chunks(framework_tx):
    '''
    should yield to reactor every chunk
    '''

    from twisted.internet.task import Clock
    laters = []

    class FakeClock(Clock):
        def callLater(self, *args, **kw):  # noqa
            laters.append((args, kw))
            Clock.callLater(self, *args, **kw)
    new_loop = FakeClock()
    calls = []

    def foo(*args, **kw):
        calls.append((args, kw))

    with replace_loop(new_loop):
        batched = txaio.make_batched_timer(1, chunk_size=2)
        batched.call_later(2, foo, "call0")
        batched.call_later(2, foo, "call1")
        batched.call_later(2, foo, "call2")

        # we have 3 calls in one bucket, so there should be just a
        # single "real" delayed call outstanding
        assert len(laters) == 1
        # ...and this call-later should be 2 seconds from now
        assert laters[0][0][0] == 2

        # the chunk-size is 2, so after advancing to 2 seconds from
        # now, we should have notified 2 of the callers and added
        # another call-later. We're spreading these out over the
        # bucket-size, so it should be at 0.5 seconds from now.
        new_loop.advance(2)
        new_loop.advance(1)
        assert len(calls) == 3
        assert len(laters) == 2
        # second call-later half the interval in the future (i.e. 0.5s)
        assert laters[1][0][0] == 0.5


def test_batched_chunks_with_errors(framework_tx):
    '''
    errors from batched calls are reported
    '''

    from twisted.internet.task import Clock
    laters = []

    class FakeClock(Clock):
        def callLater(self, *args, **kw):  # noqa
            laters.append((args, kw))
            Clock.callLater(self, *args, **kw)
    new_loop = FakeClock()
    calls = []

    def foo(*args, **kw):
        calls.append((args, kw))

    def error(*args, **kw):
        raise RuntimeError("sadness")

    with replace_loop(new_loop):
        batched = txaio.make_batched_timer(1, chunk_size=2)
        batched.call_later(2, foo, "call0")
        batched.call_later(2, foo, "call1")
        batched.call_later(2, foo, "call2")
        batched.call_later(2, error)

        # notify everything, causing an error from the second batch
        try:
            new_loop.advance(2)
            new_loop.advance(1)
            assert False, "Should get exception"
        except RuntimeError as e:
            assert "processing call_later" in str(e)


def test_batched_close_to_now(framework_tx):
    '''
    if our current time is fractional, and we make a call_later with a
    tiny delay that's still within the same second, we'll produce a
    negative call_later when adding a bucket; see issue #81
    '''
    from twisted.internet.task import Clock

    class FakeClock(Clock):
        def callLater(self, delay, *args, **kw):  # noqa
            # 'real' reactors do this, but Clock doesn't assert on
            # this.
            assert delay >= 0
            return Clock.callLater(self, delay, *args, **kw)

    with replace_loop(FakeClock()) as clock:
        clock.advance(0.5)
        batched = txaio.make_batched_timer(1, chunk_size=2)
        batched.call_later(0.1, lambda: None)
