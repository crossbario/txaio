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

try:
    import asyncio
    from asyncio.test_utils import run_once as _run_once

    def run_once():
        return _run_once(asyncio.get_event_loop())

except ImportError as e:
    try:
        import trollius as asyncio
    except ImportError:
        asyncio = None

    def run_once():
        '''
        copied from asyncio.testutils because trollius has no
        "testutils"
        '''
        # in Twisted, this method is a no-op
        if asyncio is None:
            return

        # just like modern asyncio.testutils.run_once does it...
        loop = asyncio.get_event_loop()
        loop.stop()
        loop.run_forever()
        asyncio.gather(*asyncio.Task.all_tasks())


try:
    # XXX fixme hack better way to detect twisted
    # (has to work on py3 where asyncio exists always, though)
    import twisted  # noqa

    def await(_):
        return

except ImportError:
    def await(future):
        asyncio.get_event_loop().run_until_complete(future)
