from __future__ import print_function
import txaio.aio as txaio

# note: all the code below is *identical* to the use_asyncio.py
# example, except for the import line above and event-loop running

def cb(value):
    print("Callback:", value)

def eb(fail):
    # fail will implement txaio.IFailedPromise
    print("Errback:", fail)
    fail.printTraceback()

f = txaio.create_future()
txaio.add_future_callbacks(f, cb, eb)

# ...other things happen...

def do_something():
    if False:
        return "at least it's something"
    raise RuntimeError("sadness")

try:
    answer = do_something()
    fail = None
except Exception:
    fail = txaio.create_failure()

if fail:
    txaio.reject_future(f, fail)
else:
    txaio.resolve_future(f, answer)

# Arrange for our event-loop to run.
try:
    import asyncio
except ImportError:
    import trollius as asyncio
loop = asyncio.get_event_loop()
loop.stop()
loop.run_forever()
