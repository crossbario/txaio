from six import StringIO
import pytest
import txaio

from util import run_once, await


def test_errback():
    f = txaio.create_future()
    exception = RuntimeError("it failed")
    errors = []

    def err(f):
        print("ERR", f)
        errors.append(f)
    txaio.add_future_callbacks(f, None, err)
    try:
        raise exception
    except:
        fail = txaio.create_failure()
    txaio.reject_future(f, fail)

    print("XXX", run_once, run_once.__doc__)
    run_once()

    assert len(errors) == 1
    assert isinstance(errors[0], txaio.IFailedPromise)
    assert exception == errors[0].value
    assert type(exception) == errors[0].type
    assert errors[0].tb is not None
    tb = StringIO()
    errors[0].printTraceback(file=tb)
    assert 'RuntimeError' in tb.getvalue()
    assert 'it failed' in tb.getvalue()
    assert errors[0].getErrorMessage() == 'it failed'
    assert 'it failed' in str(errors[0])

def test_errback_reject_no_args():
    """
    txaio.reject_future() with no args
    """

    f = txaio.create_future()
    exception = RuntimeError("it failed")
    errors = []

    def err(f):
        errors.append(f)
    txaio.add_future_callbacks(f, None, err)
    try:
        raise exception
    except:
        txaio.reject_future(f)

    run_once()

    assert len(errors) == 1
    assert isinstance(errors[0], txaio.IFailedPromise)
    assert exception == errors[0].value
    assert type(exception) == errors[0].type
    assert errors[0].tb is not None
    tb = StringIO()
    errors[0].printTraceback(file=tb)
    assert 'RuntimeError' in tb.getvalue()
    assert 'it failed' in tb.getvalue()
    assert errors[0].getErrorMessage() == 'it failed'
    assert 'it failed' in str(errors[0])


def test_immediate_failure():
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

    txaio.add_future_callbacks(f0, cb, errback)
    txaio.add_future_callbacks(f1, cb, errback)

    run_once()
    run_once()
    run_once()

    assert len(results) == 0
    assert len(errors) == 2
    assert isinstance(errors[0], txaio.IFailedPromise)
    assert isinstance(errors[1], txaio.IFailedPromise)
    assert errors[0].value == exception
    assert errors[1].value == exception
    # should be distinct FailedPromise instances
    assert id(errors[0]) != id(errors[1])
