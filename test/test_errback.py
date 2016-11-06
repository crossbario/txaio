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


def test_errback(framework):
    f = txaio.create_future()
    exception = RuntimeError("it failed")
    errors = []

    def err(f):
        errors.append(f)
    txaio.add_callbacks(f, None, err)
    try:
        raise exception
    except:
        fail = txaio.create_failure()
    txaio.reject(f, fail)

    run_once()

    assert len(errors) == 1
    assert isinstance(errors[0], txaio.IFailedFuture)
    assert exception == errors[0].value
    assert txaio.failure_traceback(errors[0]) is not None

    tb = txaio.failure_format_traceback(errors[0])

    assert 'RuntimeError' in tb
    assert 'it failed' in tb
    assert txaio.failure_message(errors[0]) == 'RuntimeError: it failed'
    assert 'it failed' in str(errors[0])


def test_errback_without_except(framework):
    '''
    Create a failure without an except block
    '''
    f = txaio.create_future()
    exception = RuntimeError("it failed")
    errors = []

    def err(f):
        errors.append(f)
    txaio.add_callbacks(f, None, err)
    fail = txaio.create_failure(exception)
    txaio.reject(f, fail)

    run_once()

    assert len(errors) == 1
    assert isinstance(errors[0], txaio.IFailedFuture)
    tb = txaio.failure_format_traceback(errors[0])

    assert 'RuntimeError' in tb
    assert 'it failed' in tb
    assert txaio.failure_message(errors[0]) == 'RuntimeError: it failed'
    assert 'it failed' in str(errors[0])


def test_errback_plain_exception(framework):
    '''
    reject a future with just an Exception
    '''
    f = txaio.create_future()
    exception = RuntimeError("it failed")
    errors = []

    def err(f):
        errors.append(f)
    txaio.add_callbacks(f, None, err)
    txaio.reject(f, exception)

    run_once()

    assert len(errors) == 1
    assert isinstance(errors[0], txaio.IFailedFuture)
    tb = txaio.failure_format_traceback(errors[0])

    assert 'RuntimeError' in tb
    assert 'it failed' in tb
    assert txaio.failure_message(errors[0]) == 'RuntimeError: it failed'
    assert 'it failed' in str(errors[0])


def test_errback_illegal_args(framework):
    '''
    non-Exception/Failures should be rejected
    '''
    f = txaio.create_future()
    try:
        txaio.reject(f, object())
        assert "should have raised exception."
    except RuntimeError:
        pass


def test_errback_reject_no_args(framework):
    """
    txaio.reject() with no args
    """

    f = txaio.create_future()
    exception = RuntimeError("it failed")
    errors = []

    def err(f):
        errors.append(f)
    txaio.add_callbacks(f, None, err)
    try:
        raise exception
    except:
        txaio.reject(f)

    run_once()

    assert len(errors) == 1
    assert isinstance(errors[0], txaio.IFailedFuture)
    assert exception == errors[0].value
    tb = txaio.failure_format_traceback(errors[0])

    assert 'RuntimeError' in tb
    assert 'it failed' in tb
    assert txaio.failure_message(errors[0]) == 'RuntimeError: it failed'
    assert 'it failed' in str(errors[0])


def test_immediate_failure(framework):
    exception = RuntimeError("it failed")
    try:
        raise exception
    except:
        f0 = txaio.create_future_error()
        fail = txaio.create_failure()

    errors = []
    results = []
    f1 = txaio.create_future_error(fail)

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_callbacks(f0, cb, errback)
    txaio.add_callbacks(f1, cb, errback)

    run_once()
    run_once()
    run_once()

    assert len(results) == 0
    assert len(errors) == 2
    assert isinstance(errors[0], txaio.IFailedFuture)
    assert isinstance(errors[1], txaio.IFailedFuture)
    assert errors[0].value == exception
    assert errors[1].value == exception
    # should be distinct FailedPromise instances
    assert id(errors[0]) != id(errors[1])
