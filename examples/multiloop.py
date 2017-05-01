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

from __future__ import print_function

# This example only works with asyncio

import asyncio
import pytest
import txaio
txaio.use_asyncio()


class Thing(object):

    def __init__(self, loop=None):
        self._txa = txaio.with_config(loop=loop)

    def do_thing(self):
        f = self._txa.create_future()

        def done():
            self._txa.resolve(f, "done")
        self._txa.call_later(1, done)
        return f


loop = asyncio.new_event_loop()
thing0 = Thing()
thing1 = Thing(loop=loop)

asyncio.get_event_loop().run_until_complete(thing0.do_thing())
# this will be error, mismatched loops:
#asyncio.get_event_loop().run_until_complete(thing1.do_thing())
loop.run_until_complete(thing1.do_thing())
