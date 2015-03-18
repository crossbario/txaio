from asyncio import coroutine, async
from functools import wraps
from types import GeneratorType


class Return(Exception):
    def __init__(self, v):
        self.value = v

def returnValue(x):
    # inject the return value into the function-just-called
    raise Return(x)

@coroutine
def unwind_generator(gen):
    future = gen.send(None)
    try:
        while future:
            res = yield from async(future)
            future = gen.send(res)
    except Return as e:
        # print("Return via exception! joys!", e)
        res = e.value
    return res

def future_generator(f):
    @wraps(f)
    @coroutine
    def unwrap_return(*args, **kw):
        r = f(*args, **kw)
        if type(r) is not GeneratorType:
            raise RuntimeError("{0} must return a generator object".format(f))
        real = yield from unwind_generator(r)
        return real
    return unwrap_return
