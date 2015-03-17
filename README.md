# txaio
Utilities to support code that runs unmodified on Twisted and asyncio

This is like [six](http://pythonhosted.org/six/), but for wrapping over differences between Twisted and asyncio so one can write code that runs unmodified on both (aka "source code compatibility").

> Note that, with this approach, user code runs under the native event loop of either Twisted or asyncio. This is different from attaching either one's event loop to the other using some event loop adapter.
