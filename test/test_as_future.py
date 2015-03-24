import pytest
import txaio

from util import run_once


def test_as_future_immediate():
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


def test_as_future_coroutine():
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


def test_as_future_exception():
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


def test_as_future_recursive():
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
