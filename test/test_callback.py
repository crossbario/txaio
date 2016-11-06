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

from util import run_once


def test_default_resolve(framework):
    f = txaio.create_future()
    results = []

    def cb(f):
        results.append(f)
    txaio.add_callbacks(f, cb, None)
    txaio.resolve(f)

    run_once()

    assert len(results) == 1
    assert results[0] is None


def test_callback(framework):
    f = txaio.create_future()
    results = []

    def cb(f):
        results.append(f)
    txaio.add_callbacks(f, cb, None)
    txaio.resolve(f, "it worked")

    run_once()

    assert len(results) == 1
    assert results[0] == "it worked"


def test_chained_callback(framework):
    """
    Chain two callbacks where the first one alters the value.
    """
    calls = []

    def callback0(arg):
        calls.append(arg)
        return arg + " pray I do not alter it futher"

    def callback1(arg):
        calls.append(arg)

    f = txaio.create_future()
    txaio.add_callbacks(f, callback0, None)
    txaio.add_callbacks(f, callback1, None)
    txaio.resolve(f, "the deal")

    run_once()

    assert len(calls) == 2
    assert calls[0] == "the deal"
    assert calls[1] == "the deal pray I do not alter it futher"


def test_immediate_result(framework):
    f = txaio.create_future_success("it worked")
    results = []

    def cb(f):
        results.append(f)
    txaio.add_callbacks(f, cb, None)

    run_once()

    assert len(results) == 1
    assert results[0] == "it worked"
