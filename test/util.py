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


def run_once():
    '''
    A helper that takes one trip through the event-loop to process any
    pending Futures. This is a no-op for Twisted, because you don't
    need to use the event-loop to get callbacks to happen in Twisted.
    '''

    import txaio
    if txaio.using_twisted:
        return

    try:
        import asyncio
        from asyncio.test_utils import run_once as _run_once
        return _run_once(asyncio.get_event_loop())

    except ImportError:
        import trollius as asyncio
        # let any trollius import error out; if we're not using
        # twisted, and have no asyncio *and* no trollius, that's a
        # problem.

        # copied from asyncio.testutils because trollius has no
        # testutils"

        # just like modern asyncio.testutils.run_once does it...
        loop = asyncio.get_event_loop()
        loop.stop()
        loop.run_forever()
        asyncio.gather(*asyncio.Task.all_tasks())


def await(future):
    '''
    Essentially just a way to call "run_until_complete" that becomes a
    no-op if we're using Twisted.
    '''

    import txaio
    if txaio.using_twisted:
        return

    try:
        import asyncio
    except ImportError:
        import trollius as asyncio

    asyncio.get_event_loop().run_until_complete(future)
