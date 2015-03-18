from six import StringIO
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

    txaio.add_future_callbacks(f, cb, errback)

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

    txaio.add_future_callbacks(f, cb, errback)

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
    exception = RuntimeError("sadness")
    f1 = txaio.create_future_success(42)

    def method(*args, **kw):
        calls.append((args, kw))
        return f1
    f0 = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_future_callbacks(f0, cb, errback)

    run_once()

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == 42
    assert calls[0] == ((1, 2, 3), dict(key='word'))


def test_as_future_generator():
    '''
    Return a coroutine to as_future
    '''
    errors = []
    results = []
    calls = []

    @txaio.future_generator
    def codependant(*args, **kw):
        calls.append((args, kw))
        yield txaio.create_future_success(42)
        txaio.returnValue(42)

    def method(*args, **kw):
        calls.append((args, kw))
        return codependant(*args, **kw)
    f = txaio.as_future(method, 1, 2, 3, key='word')

    def cb(x):
        results.append(x)

    def errback(f):
        errors.append(f)

    txaio.add_future_callbacks(f, cb, errback)

    # XXX really need to figure out something better here :(
    run_once()
    run_once()
    run_once()
    run_once()

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == 42
    assert len(calls) == 2
    assert calls[0] == ((1, 2, 3), dict(key='word'))
    assert calls[1] == ((1, 2, 3), dict(key='word'))
