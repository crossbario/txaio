from __future__ import print_function
import txaio

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
