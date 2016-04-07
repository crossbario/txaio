###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
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

from __future__ import print_function

from collections import namedtuple
from io import BytesIO, StringIO

import os
import six
import pytest
import txaio

Log = namedtuple('Log', ['args'])


class TestHandler(BytesIO):

    @property
    def messages(self):
        # Because we print the \n after, there will always be an empty
        # 'message', so just don't include it.
        return self.getvalue().split(os.linesep.encode('ascii'))[:-1]


_handler = TestHandler()


@pytest.fixture
def log_started(framework):
    """
    Sets up the logging, which we can only do once per run.
    """
    early_log = txaio.make_logger()
    early_log.info("early log")

    txaio.start_logging(out=_handler, level='debug')


@pytest.fixture(scope='function')
def handler(log_started):
    """
    Resets the global TestHandler instance for each test.
    """
    _handler.truncate(0)
    _handler.seek(0)
    return _handler


def test_categories(handler, framework):
    """
    Calling ``txaio.add_log_categories`` with a dict mapping category keys to
    category log formats will allow log messages which have the
    ``log_category`` key take the associated format.
    """
    logger = txaio.make_logger()

    txaio.add_log_categories({"TX100": u"{adjective} {nouns[2]}"})

    # do something a little fancy, with attribute access etc.
    logger.critical(
        "you won't see me",
        log_category="TX100",
        adjective='hilarious',
        nouns=['skunk', 'elephant', 'wombat'],
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"hilarious wombat")


def test_categories_subsequent(handler, framework):
    """
    Later calls to add_log_categories update the list of log categories and
    take precedence.
    """
    logger = txaio.make_logger()

    txaio.add_log_categories({"TX100": u"{adjective} {nouns[2]}"})
    txaio.add_log_categories({"TX100": u"{adjective} {nouns[1]}"})

    # do something a little fancy, with attribute access etc.
    logger.critical(
        log_category="TX100",
        adjective='hilarious',
        nouns=['skunk', 'elephant', 'wombat'],
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"hilarious elephant")


def test_critical(handler, framework):
    logger = txaio.make_logger()

    # do something a little fancy, with attribute access etc.
    logger.critical(
        "{adjective} {nouns[2]}",
        adjective='hilarious',
        nouns=['skunk', 'elephant', 'wombat'],
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"hilarious wombat")


def test_info(handler, framework):
    logger = txaio.make_logger()

    # do something a little fancy, with attribute access etc.
    logger.info(
        "{adjective} {nouns[1]}",
        adjective='hilarious',
        nouns=['skunk', 'elephant', 'wombat'],
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"hilarious elephant")


def test_trace(handler, framework):
    logger = txaio.make_logger()
    old_log = txaio.get_global_log_level()
    txaio.set_global_log_level("trace")

    # the txaio_trace variable should be in it
    logger.trace(
        "trace {txaio_trace}",
    )

    txaio.set_global_log_level(old_log)

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"trace True")


def test_emit_noop(handler, framework):
    """
    emit() with a too-low level is an no-op.
    """
    logger = txaio.make_logger()

    old_log = txaio.get_global_log_level()
    txaio.set_global_log_level("info")

    logger.emit("debug", "foobar")

    txaio.set_global_log_level(old_log)

    assert len(handler.messages) == 0


def test_emit_ok(handler, framework):
    """
    emit() with an OK level emits the message.
    """
    logger = txaio.make_logger()

    old_log = txaio.get_global_log_level()
    txaio.set_global_log_level("trace")

    logger.emit("trace", "foobar")
    logger.emit("info", "barbaz")

    txaio.set_global_log_level(old_log)

    assert len(handler.messages) == 2
    assert handler.messages[0].endswith(b"foobar")
    assert handler.messages[1].endswith(b"barbaz")


def test_bad_failures(handler, framework):
    # just ensuring this doesn't explode
    txaio.failure_format_traceback("not a failure")
    txaio.failure_message("not a failure")


def test_debug_with_object(handler, framework):
    logger = txaio.make_logger()

    class Shape(object):
        sides = 4
        name = "bamboozle"
        config = dict(foo='bar')

    logger.info(
        "{what.config[foo]} {what.sides} {what.name}",
        what=Shape(),
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"bar 4 bamboozle")


def test_log_noop_trace(handler, framework):
    # trace should be a no-op, because we set the level to 'debug' in
    # the fixture
    logger = txaio.make_logger()

    logger.trace("a trace message")

    assert len(handler.messages) == 0


def test_double_start(handler, framework):
    try:
        txaio.start_logging()
    except RuntimeError:
        assert False, "shouldn't get exception"


def test_invalid_level(framework):
    try:
        txaio.start_logging(level='foo')
        assert False, "should get exception"
    except RuntimeError as e:
        assert 'Invalid log level' in str(e)


def test_class_descriptor(handler, framework):
    class Something(object):
        log = txaio.make_logger()

        def do_a_thing(self):
            self.log.info("doing a thing")

    s = Something()
    s.do_a_thing()

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"doing a thing")


def test_class_attribute(handler, framework):
    class Something(object):
        def __init__(self):
            self.log = txaio.make_logger()

        def do_a_thing(self):
            self.log.info("doing a thing")

    s = Something()
    s.do_a_thing()

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"doing a thing")


def test_log_converter(handler, framework):
    pytest.importorskip("twisted.logger")
    # this checks that we can convert a plain Twisted Logger calling
    # failure() into a traceback on our observers.
    from twisted.logger import Logger
    from txaio.tx import _LogObserver

    out = six.StringIO()
    observer = _LogObserver(out)
    logger = Logger(observer=observer)

    try:
        raise RuntimeError("failed on purpose")
    except:
        logger.failure(None)

    output = out.getvalue()
    assert "failed on purpose" in output
    assert "Traceback" in output


def test_txlog_write_binary(handler, framework):
    """
    Writing to a binary stream is supported.
    """
    pytest.importorskip("twisted.logger")
    from txaio.tx import _LogObserver

    out_file = BytesIO()
    observer = _LogObserver(out_file)

    observer({
        "log_format": "hi: {testentry}",
        "testentry": "hello",
        "log_level": observer.to_tx["info"],
        "log_time": 1442890018.002233
    })

    output = out_file.getvalue()
    assert b"hi: hello" in output


def test_txlog_write_text(handler, framework_tx):
    """
    Writing to a text stream is supported.
    """
    pytest.importorskip("twisted.logger")
    from txaio.tx import _LogObserver

    out_file = StringIO()
    observer = _LogObserver(out_file)

    observer({
        "log_format": "hi: {testentry}",
        "testentry": "hello",
        "log_level": observer.to_tx["info"],
        "log_time": 1442890018.002233
    })

    output = out_file.getvalue()
    assert u"hi: hello" in output


def test_aiolog_write_binary(handler, framework_aio):
    """
    Writing to a binary stream is supported.
    """
    pytest.importorskip("txaio.aio")
    from txaio.aio import _TxaioFileHandler

    out_file = BytesIO()
    observer = _TxaioFileHandler(out_file)

    observer.emit(Log(args={
        "log_message": "hi: {testentry}",
        "testentry": "hello",
        "log_time": 1442890018.002233
    }))

    output = out_file.getvalue()
    assert b"hi: hello" in output


def test_aiolog_write_text(handler, framework_aio):
    """
    Writing to a text stream is supported.
    """
    pytest.importorskip("txaio.aio")
    from txaio.aio import _TxaioFileHandler

    out_file = StringIO()
    observer = _TxaioFileHandler(out_file)

    observer.emit(Log(args={
        "log_message": "hi: {testentry}",
        "testentry": "hello",
        "log_time": 1442890018.002233
    }))

    output = out_file.getvalue()
    assert u"hi: hello" in output
