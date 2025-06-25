txaio
=====

| |Version| |Build| |Deploy| |Coverage| |Docs|

--------------

**txaio** is a helper library for writing code that runs unmodified on
both `Twisted <https://twistedmatrix.com/>`_ and `asyncio <https://docs.python.org/3/library/asyncio.html>`_ / `Trollius <http://trollius.readthedocs.org/en/latest/index.html>`_.

This is like `six <http://pythonhosted.org/six/>`_, but for wrapping
over differences between Twisted and asyncio so one can write code
that runs unmodified on both (aka *source code compatibility*). In
other words: your *users* can choose if they want asyncio **or** Twisted
as a dependency.

Note that, with this approach, user code **runs under the native event
loop of either Twisted or asyncio**. This is different from attaching
either one's event loop to the other using some event loop adapter.


Platform support
----------------

**txaio** runs on CPython 3.6+ and PyPy 3, on top of *Twisted* or *asyncio*. Specifically, **txaio** is tested on the following platforms:

* CPython 3.6 and 3.9 on Twisted 18.7, 19.10, trunk and on asyncio (stdlib)
* PyPy 3.6 an 3.7 on Twisted 18.7, 19.10, trunk and on asyncio (stdlib)

> Note: txaio up to version 18.8.1 also supported Python 2.7 and Python 3.4. Beginning with release v20.1.1, txaio only supports Python 3.5+. Beginning with release v20.12.1, txaio only supports Python 3.6+.


How it works
------------

Instead of directly importing, instantiating and using ``Deferred``
(for Twisted) or ``Future`` (for asyncio) objects, **txaio** provides
helper-functions to do that for you, as well as associated things like
adding callbacks or errbacks.

This obviously changes the style of your code, but then you can choose
at runtime (or import time) which underlying event-loop to use. This
means you can write **one** code-base that can run on Twisted *or*
asyncio (without a Twisted dependency) as you or your users see fit.

Code like the following can then run on *either* system:

.. sourcecode:: python

    import txaio
    txaio.use_twisted()  # or .use_asyncio()

    f0 = txaio.create_future()
    f1 = txaio.as_future(some_func, 1, 2, key='word')
    txaio.add_callbacks(f0, callback, errback)
    txaio.add_callbacks(f1, callback, errback)
    # ...
    txaio.resolve(f0, "value")
    txaio.reject(f1, RuntimeError("it failed"))

Please refer to the `documentation <https://txaio.readthedocs.io/en/latest/>`_ for description and usage of the library features.


AI Policy
---------

.. important::

   **A Note on Upcoming Policy Changes Regarding AI-Assisted Content**

   Up to and including version **v25.6.1**, this project contains no code or documentation
   generated with the assistance of AI tools. This version represents the final release under
   our historical contribution policy.

   Starting with future versions (after v25.6.1), our contribution policy will change.
   Subsequent releases **MAY** contain code or documentation created with AI assistance.

   We urge all users and contributors to review our :ref:`ai_policy`. This document details:

   - The rules and warranties required for all future contributions.
   - The potential intellectual property implications for the project and its users.

   This policy was established following an open community discussion, which you can review
   on `GitHub issue #1663 <https://github.com/crossbario/autobahn-python/issues/1663>`_.

   We are providing this transparent notice to enable you to make an informed decision.
   If our new AI policy is incompatible with your own (or your organization's) development
   practices or risk tolerance, please take this into consideration when deciding whether
   to upgrade beyond version v25.6.1.


.. |Version| image:: https://img.shields.io/pypi/v/txaio.svg
   :target: https://pypi.python.org/pypi/txaio
   :alt: Version

.. |Build| image:: https://github.com/crossbario/txaio/workflows/main/badge.svg
   :target: https://github.com/crossbario/txaio/actions?query=workflow%3Amain
   :alt: Build Workflow

.. |Deploy| image:: https://github.com/crossbario/txaio/workflows/deploy/badge.svg
   :target: https://github.com/crossbario/txaio/actions?query=workflow%3Adeploy
   :alt: Deploy Workflow

.. |Coverage| image:: https://codecov.io/github/crossbario/txaio/coverage.svg?branch=master
   :target: https://codecov.io/github/crossbario/txaio
   :alt: Coverage

.. |Docs| image:: https://readthedocs.org/projects/txaio/badge/?version=latest
   :target: https://txaio.readthedocs.io/en/latest/
   :alt: Docs
