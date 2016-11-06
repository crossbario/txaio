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
import txaio
txaio.use_twisted()

def cb(value):
    print("Callback:", value)
    return value  # should always return input arg

def eb(fail):
    # fail will implement txaio.IFailedPromise
    print("Errback:", fail)
    # fail.printTraceback()
    return fail  # should always return input arg

f0 = txaio.create_future()
f1 = txaio.create_future()
txaio.add_callbacks(f0, cb, eb)
txaio.add_callbacks(f1, cb, eb)

# ...

txaio.reject(f0, RuntimeError("it failed"))
# or can just "txaio.reject(f0)" if inside an except: block
txaio.resolve(f1, "The answer is: 42")

if txaio.using_asyncio:
    # for twisted, we don't need to enter the event-loop for this
    # simple example (since all results are already available), but
    # you'd simply use reactor.run()/.stop() or task.react() as normal
    import asyncio
    asyncio.get_event_loop().run_until_complete(f1)
