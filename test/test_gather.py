from six import StringIO
import pytest
import txaio

from util import run_once, await


def test_gather_illegal_args():
    '''
    first_result=True and first_exception=True fails asyncio

    Obviously, if I'm wrong about that lets fix it.
    '''
    if txaio.using_twisted:
        pytest.skip()

    try:
        txaio.gather_futures([], first_result=True, first_exception=True)
        assert False
    except RuntimeError as e:
        assert 'not possible with asyncio' in str(e)


def test_first_result():
    '''
    Stop processing after one result.
    '''

    results = []

    def callback(arg):
        results.append(arg)
        return 9

    f0 = txaio.create_future()
    f1 = txaio.create_future()
    f2 = txaio.create_future_success(42)

    txaio.add_future_callbacks(f0, callback, callback)
    txaio.add_future_callbacks(f1, callback, callback)
    txaio.add_future_callbacks(f2, callback, callback)

    final = txaio.gather_futures([f0, f1, f2], first_result=True)

    def blam(arg):
        results.append(arg)
    txaio.add_future_callbacks(final, blam, None)

    await(final)
    assert len(results) == 2
    assert results[0] == 42
    assert results[1] == 9


def test_first_error():
    '''
    Stop processing after one error.
    '''

    results = []
    exception = RuntimeError("testing")

    def callback(arg):
        results.append(arg)

    try:
        raise exception
    except:
        f0 = txaio.create_future_error()
    f1 = txaio.create_future()
    f2 = txaio.create_future()

    txaio.add_future_callbacks(f0, callback, callback)
    txaio.add_future_callbacks(f1, callback, callback)
    txaio.add_future_callbacks(f1, callback, callback)

    final = txaio.gather_futures([f0, f1, f2], first_exception=True)

    def gather_error(arg):
        results.append(arg)
    txaio.add_future_callbacks(final, None, gather_error)

    await(final)
    assert len(results) == 1
    assert results[0].value == exception


def test_propagate_errors_first():
    '''
    consume_exceptions=False, first_exception=True
    '''

    results = []
    exception = RuntimeError("testing")

    def callback(arg):
        results.append(arg)
        return arg

    try:
        raise exception
    except:
        f0 = txaio.create_future_error()
#    f1 = txaio.create_future_success("quux")
#    f2 = txaio.create_future_success("foo")
    f1 = txaio.create_future()
    f2 = txaio.create_future()

    txaio.add_future_callbacks(f0, callback, callback)
    txaio.add_future_callbacks(f1, callback, callback)
    txaio.add_future_callbacks(f2, callback, callback)

    final = txaio.gather_futures(
        [f0, f1, f2],
        consume_exceptions=False,
        first_exception=True,
    )

    def gather_error(arg):
        results.append(arg)
        return None
    txaio.add_future_callbacks(final, gather_error, gather_error)

    # arrange to cancel/ignore all errors in the futures
    for f in [f0, f1, f2]:
        txaio.add_future_callbacks(f, None, lambda _: None)

    # can't call await(final) because that causes the exception to be
    # raised from await() -- that needs re-design I guess.
    for x in range(20):
        run_once()

    assert len(results) == 2
    assert results[0].value == exception
    assert results[1].value == exception


def test_propagate_errors_all():
    '''
    consume_exceptions=False, first_exception=False
    '''

    results = []
    exception = RuntimeError("testing")

    def callback(arg):
        results.append(arg)
        return arg

    try:
        raise exception
    except:
        f0 = txaio.create_future_error()
        f1 = txaio.create_future_error()
    f2 = txaio.create_future_success("foo")

    txaio.add_future_callbacks(f0, callback, callback)
    txaio.add_future_callbacks(f1, callback, callback)
    txaio.add_future_callbacks(f2, callback, callback)

    final = txaio.gather_futures(
        [f0, f1, f2],
        consume_exceptions=False,
        first_exception=False,
    )

    def gather_error(arg):
        results.append(arg)
        return None
    txaio.add_future_callbacks(final, gather_error, gather_error)

    # arrange to cancel/ignore all errors in the futures
    for f in [f0, f1, f2]:
        txaio.add_future_callbacks(f, None, lambda _: None)

    # can't call await(final) because that causes the exception to be
    # raised from await() -- that needs re-design I guess.
    for x in range(20):
        run_once()

    assert len(results) == 4
    assert results[0].value == exception
    assert results[1].value == exception
    assert results[2] == "foo"
    # we asked for "don't consume errors", so we should get the first
    # one propogated out to the gather-future as a failure.
    assert results[3].value == exception


def test_gather_two():
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

    f2 = txaio.gather_futures([f0, f1])

    def done(arg):
        results.append(arg)

    def error(fail):
        errors.append(fail)
        # fail.printTraceback()
    txaio.add_future_callbacks(f2, done, error)

    await(f0)
    await(f1)
    await(f2)

    assert len(results) == 1
    assert len(errors) == 0
    assert results[0] == ['OHAI', 42] or results[0] == [42, 'OHAI']
    assert len(calls) == 2
    assert calls[0] == ((1, 2, 3), dict(key='word'))
    assert calls[1] == (tuple(), dict())


def test_gather_first_result():
    '''
    Wait for two Futures.
    '''

    errors = []
    results = []

    f0 = txaio.create_future()
    f1 = txaio.create_future()
    txaio.resolve_future(f0, "foo")

    f2 = txaio.gather_futures([f0, f1], first_result=True)

    def done(arg):
        results.append(arg)

    def error(fail):
        errors.append(fail)
        # fail.printTraceback()
    txaio.add_future_callbacks(f2, done, error)

    await(f2)

    assert len(results) == 1
    assert results[0] == "foo"  # gather_futures should return the first result
    assert len(errors) == 0
