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


def test_immediate_result(framework):
    f = txaio.create_future_success("it worked")
    results = []

    def cb(f):
        results.append(f)
    txaio.add_callbacks(f, cb, None)

    run_once()

    assert len(results) == 1
    assert results[0] == "it worked"
