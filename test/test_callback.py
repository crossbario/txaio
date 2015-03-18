from six import StringIO
import pytest
import txaio

from util import run_once


def test_callback():
    f = txaio.create_future()
    results = []

    def cb(f):
        results.append(f)
    txaio.add_future_callbacks(f, cb, None)
    txaio.resolve_future(f, "it worked")

    run_once()

    assert len(results) == 1
    assert results[0] == "it worked"


def test_chained_callback():
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
    txaio.add_future_callbacks(f, callback0, None)
    txaio.add_future_callbacks(f, callback1, None)
    txaio.resolve_future(f, "the deal")

    run_once()

    assert len(calls) == 2
    assert calls[0] == "the deal"
    assert calls[1] == "the deal pray I do not alter it futher"


def test_immediate_result():
    f = txaio.create_future_success("it worked")
    results = []

    def cb(f):
        results.append(f)
    txaio.add_future_callbacks(f, cb, None)

    run_once()

    assert len(results) == 1
    assert results[0] == "it worked"
