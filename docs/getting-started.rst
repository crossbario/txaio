Getting Started
===============

This guide will help you get started with **txaio** quickly.

Quick Example
-------------

txaio allows you to write code that works on both Twisted and asyncio.
Here's a simple example:

.. code-block:: python

    import txaio

    # Select your framework (do this once at startup)
    txaio.use_twisted()  # or txaio.use_asyncio()

    # Create a future
    f = txaio.create_future()

    # Add callbacks
    def on_success(result):
        print(f"Success: {result}")
        return result

    def on_error(error):
        print(f"Error: {error}")
        return error

    txaio.add_callbacks(f, on_success, on_error)

    # Resolve the future
    txaio.resolve(f, "Hello, txaio!")

Using with Twisted
------------------

.. code-block:: python

    import txaio
    txaio.use_twisted()

    from twisted.internet import reactor

    def main():
        f = txaio.create_future()
        txaio.add_callbacks(f, lambda x: print(f"Got: {x}"), None)
        txaio.resolve(f, "Hello from Twisted!")
        reactor.callLater(1, reactor.stop)

    reactor.callWhenRunning(main)
    reactor.run()

Using with asyncio
------------------

.. code-block:: python

    import asyncio
    import txaio
    txaio.use_asyncio()

    async def main():
        f = txaio.create_future()
        txaio.add_callbacks(f, lambda x: print(f"Got: {x}"), None)
        txaio.resolve(f, "Hello from asyncio!")
        await asyncio.sleep(0.1)

    asyncio.run(main())

Next Steps
----------

* Read the :doc:`programming-guide` for detailed usage
* Check the :doc:`overview` for architectural details
* See the API Reference for complete documentation
