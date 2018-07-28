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

from util import _await


def test_gather_two(framework):
    '''
    Wait for two Futures.
    '''

    errors = []
    results = []
    calls = []

    def foo():
        def codependant(*args, **kw):
            calls.append((args, kw))
            return 42
        return txaio.as_future(codependant)

    def method(*args, **kw):
        calls.append((args, kw))
        return "OHAI"
    f0 = txaio.as_future(method, 1, 2, 3, key='word')
    f1 = txaio.as_future(foo)

    f2 = txaio.gather([f0, f1])

    def done(arg):
        results.append(arg)

    def error(fail):
        errors.append(fail)
        # fail.printTraceback()
    txaio.add_callbacks(f2, done, error)

    for f in [f0, f1, f2]:
        _await(f)

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == ['OHAI', 42] or results[0] == [42, 'OHAI']
    assert len(calls) == 2
    assert calls[0] == ((1, 2, 3), dict(key='word'))
    assert calls[1] == (tuple(), dict())


def test_gather_no_consume(framework):
    '''
    consume_exceptions=False
    '''

    errors = []
    results = []
    calls = []

    f0 = txaio.create_future_error(error=RuntimeError("f0 failed"))
    f1 = txaio.create_future_error(error=RuntimeError("f1 failed"))

    f2 = txaio.gather([f0, f1], consume_exceptions=False)

    def done(arg):
        results.append(arg)

    def error(fail):
        errors.append(fail)
        # fail.printTraceback()
    txaio.add_callbacks(f0, done, error)
    txaio.add_callbacks(f1, done, error)
    txaio.add_callbacks(f2, done, error)

    # FIXME more testing annoyance; the propogated errors are raised
    # out of "run_until_complete()" as well; fix util.py?
    for f in [f0, f1, f2]:
        try:
            _await(f)
        except Exception:
            pass

    assert len(results) == 0
    assert len(errors) == 3
    assert len(calls) == 0
