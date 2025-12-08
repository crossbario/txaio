Installation
============

This guide covers how to install **txaio**.

Requirements
------------

txaio supports:

* Python 3.9+
* CPython and PyPy

Installing from PyPI
--------------------

The recommended way to install txaio is from PyPI using pip:

.. code-block:: bash

    pip install txaio

Installing with Twisted Support
-------------------------------

To use txaio with Twisted:

.. code-block:: bash

    pip install txaio[twisted]

Installing with asyncio Support
-------------------------------

asyncio is included in Python's standard library, so no additional
dependencies are needed:

.. code-block:: bash

    pip install txaio

Installing from Source
----------------------

To install from source:

.. code-block:: bash

    git clone https://github.com/crossbario/txaio.git
    cd txaio
    pip install -e .

Verifying Installation
----------------------

To verify txaio is installed correctly:

.. code-block:: python

    import txaio
    print(txaio.__version__)
