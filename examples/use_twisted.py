import txaio.tx as txaio

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

# note that in this simple example (because Twisted will resolve
# callbacks immediately when results are already available) we don't
# actually need to enter the event-loop. In a "real" program you'd
# have to arrange to call ``reactor.run()`` or ``react()`` at some
# point.
