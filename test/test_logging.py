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

from io import BytesIO, StringIO

import six
import pytest
import txaio


# XXX just use StringIO?
class TestHandler(object):
    encoding = 'utf8'

    def __init__(self, *args, **kwargs):
        self.messages = []
        self._data = b''

    def write(self, data):
        for line in data.split(b'\n'):
            line = line.strip()
            if line:
                self.messages.append(line)

    def flush(self):
        pass


@pytest.fixture(scope='session')
def log_started():
    """
    Sets up the logging, which we can only do once per run.
    """
    early_log = txaio.make_logger()
    early_log.info("early log")

    handler = TestHandler()
    txaio.start_logging(out=handler, level='debug')
    return handler


@pytest.fixture(scope='function')
def handler(log_started):
    """
    Resets the global TestHandler instance for each test.
    """
    log_started.messages = []
    return log_started


def test_critical(handler):
    logger = txaio.make_logger()

    # do something a little fancy, with attribute access etc.
    logger.critical(
        "{adjective} {nouns[2]}",
        adjective='hilarious',
        nouns=['skunk', 'elephant', 'wombat'],
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"hilarious wombat")


def test_info(handler):
    logger = txaio.make_logger()

    # do something a little fancy, with attribute access etc.
    logger.info(
        "{adjective} {nouns[1]}",
        adjective='hilarious',
        nouns=['skunk', 'elephant', 'wombat'],
    )

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"hilarious elephant")


def test_bad_failures(handler):
    # just ensuring this doesn't explode
    txaio.failure_format_traceback("not a failure")
    txaio.failure_message("not a failure")


def test_debug_with_object(handler):
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


def test_log_noop_trace(handler):
    # trace should be a no-op, because we set the level to 'debug' in
    # the fixture
    logger = txaio.make_logger()

    logger.trace("a trace message")

    assert len(handler.messages) == 0


def test_double_start(handler):
    try:
        txaio.start_logging()
    except RuntimeError:
        assert False, "shouldn't get exception"


def test_invalid_level():
    try:
        txaio.start_logging(level='foo')
        assert False, "should get exception"
    except RuntimeError as e:
        assert 'Invalid log level' in str(e)


def test_class_descriptor(handler):
    class Something(object):
        log = txaio.make_logger()

        def do_a_thing(self):
            self.log.info("doing a thing")

    s = Something()
    s.do_a_thing()

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"doing a thing")


def test_class_attribute(handler):
    class Something(object):
        def __init__(self):
            self.log = txaio.make_logger()

        def do_a_thing(self):
            self.log.info("doing a thing")

    s = Something()
    s.do_a_thing()

    assert len(handler.messages) == 1
    assert handler.messages[0].endswith(b"doing a thing")


def test_log_converter(handler):
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


def test_log_write_binary(handler):
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


def test_log_write_text(handler):
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
