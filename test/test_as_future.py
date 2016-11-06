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

from util import run_once


def test_as_future_immediate(framework):
    '''
    Returning an immediate value from as_future
    '''
    errors = []
    results = []
    calls = []

    def method(*args, **kw):
        calls.append((args, kw))
        return 42
    f = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_callbacks(f, cb, errback)

    run_once()

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == 42
    assert calls[0] == ((1, 2, 3), dict(key='word'))


def test_as_future_immediate_none(framework):
    '''
    Returning None immediately from as_future
    '''
    errors = []
    results = []
    calls = []

    def method(*args, **kw):
        calls.append((args, kw))
        return None
    f = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_callbacks(f, cb, errback)

    run_once()

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] is None
    assert calls[0] == ((1, 2, 3), dict(key='word'))


def test_as_future_coroutine(framework):
    '''
    call a coroutine (asyncio)
    '''
    pytest.importorskip('asyncio')
    # can import asyncio on python3.4, but might still be using
    # twisted
    if not txaio.using_asyncio:
        return

    errors = []
    results = []
    calls = []

    from asyncio import coroutine

    @coroutine
    def method(*args, **kw):
        calls.append((args, kw))
        return 42
    f = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_callbacks(f, cb, errback)

    run_once()
    run_once()

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == 42
    assert calls[0] == ((1, 2, 3), dict(key='word'))


def test_as_future_exception(framework):
    '''
    Raises an exception from as_future
    '''
    errors = []
    results = []
    calls = []
    exception = RuntimeError("sadness")

    def method(*args, **kw):
        calls.append((args, kw))
        raise exception
    f = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_callbacks(f, cb, errback)

    run_once()

    assert len(results) == 0
    assert len(errors) == 1
    assert errors[0].value == exception
    assert calls[0] == ((1, 2, 3), dict(key='word'))


def test_as_future_recursive(framework):
    '''
    Returns another Future from as_future
    '''
    errors = []
    results = []
    calls = []
    f1 = txaio.create_future_success(42)

    def method(*args, **kw):
        calls.append((args, kw))
        return f1
    f0 = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_callbacks(f0, cb, errback)

    run_once()

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == 42
    assert calls[0] == ((1, 2, 3), dict(key='word'))
