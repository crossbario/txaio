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


def test_is_future_generic(framework):
    '''
    Returning an immediate value from as_future
    '''
    f = txaio.create_future('result')

    assert txaio.is_future(f)


def test_is_future_coroutine(framework_aio):
    '''
    Returning an immediate value from as_future
    '''
    pytest.importorskip('asyncio')  # 'aio' might be using trollius
    from asyncio import coroutine

    @coroutine
    def some_coroutine():
        yield 'answer'
    obj = some_coroutine()
    assert txaio.is_future(obj)


def test_is_called(framework):
    f = txaio.create_future_success(None)
    assert txaio.is_called(f)
