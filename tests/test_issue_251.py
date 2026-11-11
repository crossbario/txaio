###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) typedef int GmbH
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


# The sites ty 0.0.100's missing-union-attribute found (#251).

import inspect

import pytest

import txaio
from txaio._common import _BatchedTimer, _caller_namespace


class _FakeDelayedCall:
    def __init__(self):
        self.cancelled = 0

    def cancel(self):
        self.cancelled += 1


def test_batched_call_cancel_twice():
    """
    A second cancel() of a batched call is a no-op; it raised AttributeError.
    """
    delayed = []

    def create_delayed_call(delay, func, *args):
        delayed.append(_FakeDelayedCall())
        return delayed[-1]

    timer = _BatchedTimer(1000, 10, lambda: 0, create_delayed_call)
    call = timer.call_later(2, lambda: None)
    call.cancel()
    call.cancel()
    # the bucket's one underlying delayed call was cancelled once, by the first cancel()
    assert [d.cancelled for d in delayed] == [1]


def _make_logger():
    # stands in for make_logger(): _caller_namespace() looks two frames up
    return _caller_namespace()


def test_caller_namespace_function():
    assert _make_logger() == __name__ + ".test_caller_namespace_function"


def test_caller_namespace_method():
    class Something:
        def __init__(self):
            self.namespace = _make_logger()

    assert Something().namespace == __name__ + ".Something"


def test_caller_namespace_without_frames(monkeypatch):
    """
    Without stack frames (inspect.currentframe() is None), a clear error, not an
    AttributeError on None.
    """
    monkeypatch.setattr(inspect, "currentframe", lambda: None)
    with pytest.raises(RuntimeError, match="needs Python stack frames"):
        _make_logger()


def test_make_logger_namespace(framework):
    """
    make_logger() still names its logger after the caller, on both frameworks.
    """

    class Something:
        def __init__(self):
            self.log = txaio.make_logger()

    log = Something().log
    if txaio.using_twisted:
        namespace = log._logger.namespace
    else:
        namespace = log._logger.name
    assert namespace == __name__ + ".Something"
