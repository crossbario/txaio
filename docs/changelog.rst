Changelog
=========

This document contains a reverse-chronological list of changes to txaio.

.. note::

    For detailed release information including wheels and artifacts,
    see :doc:`releases`.

25.12.1
-------

**New**

* Phase 1.3: CI/CD Modernization - align workflows with wamp-cicd patterns (#205)
* Phase 1.2: Build Tooling Modernization - migrate to src layout, Furo/MyST/AutoAPI docs (#203)
* Phase 1.1: Update infrastructure submodules to latest Phase 0 versions (#201)
* Migrate from mypy to ty (Astral type checker) for faster type checking
* Enable tests and coverage in GitHub Actions
* Add coverage report artifact upload
* Modernize docs/conf.py with Furo theme, MyST Markdown, sphinx-autoapi

**Fix**

* ci: fix publish-github-releases to skip on PRs
* ci: align release.yml with autobahn-python model to prevent accidental releases

25.9.2
------

**Fix**

* fix: minimum Python version specification in pyproject.toml (#198)

25.9.1
------

**New**

* Migrate from legacy setup.py/setup.cfg/requirements.txt to modern pyproject.toml
* Upgrade GitHub workflows to use just+uv toolchain
* Add modern pyproject.toml configuration with all tool configs
* Add centralized AI support files git submodule (.ai)
* Add support for Python 3.14 (#196)

**Fix**

* polish AI policy and docs
* relax mypy configuration; disable coverage + typing jobs in CI (temporary)

**Other**

* Minimum Python version bumped to 3.11, support 3.11-3.14 on CPython/PyPy
* Copyrights maintained by typedef int GmbH (Germany)

25.6.1
------

**New**

* announcement of upcoming (but not yet effective) new AI policy clarifying matter with respect to AI assisted contributions (see #1663 in AutobahnPython)

**Fix**

* update license file to include contributors (#188)
* remove obsolete dependency on six (#186)
* update pypy version in CI workflow (#187)
* setupcfg.py:508: SetuptoolsDeprecationWarning: The license_file parameter is deprecated, use license_files instead.

**Other**

* Copyrights transferred from Crossbar.io Technologies GmbH (Germany) to typedef int GmbH (Germany)

23.1.1
------

**Fix**

* support for Python up to v3.11
* update GitHub CI
* copyright transferred to typedef int GmbH - no license change!

22.2.1
------

**Fix**

* cancel handling in python 3.8/3.9 (#175)
* gracefully fail if coroutine called with wrong args (#176)
* eliminate redundant dependency on mock (#170)
* doc note that twisted supports native coroutines (#172)

21.2.1
------

**Fix**

* update minimum dependencies (here, and in other crossbar packages) in an attempt to tame the new pip dep resolver madness

20.12.1
-------

**New**

* CI/CD migrated to GitHub Actions
* support Python 3.9 (CI / testing added)
* minimum Python version is now 3.6

20.4.1
------

**New**

* upload wheel to S3 (bucket "crossbarbuilder") in CI deploy stage

**Fix**

* fix event loop threading issue (PR #163)

20.3.1
------

**New**

* support import-time framework selection

**Fix**

* remove python2 support (finally)

20.1.1
------

**New**

* moved ``time_ns`` and ``perf_counter_ns`` helper functions here

**Other**

* IMPORTANT: beginning release v20.1.1, we only support Python 3.5 or later

18.8.1
------

**New**

* add API to support cancellation; this means passing a 1-argument callable to ``create_future`` and ``txaio.cancel`` to actually cancel a future
* support Python 3.7 (CI / testing added)

**Other**

* IMPORTANT: release v18.8.1 is the last release supporting Python 2. We will support Python 3.5 and later beginning with release v20.1.1.

18.7.1
------

**New**

* move to calver

**Other**

* deprecate Python 3.3 support and CI testing

2.10.0
------

**Fix**

* the asyncio version of ``make_logger`` now deduces a proper namespace instead of using the root (thanks `spr0cketeer <https://github.com/spr0cketeer>`_)

2.9.0
-----

*March 2, 2018*

(No detailed changelog available)

2.8.2
-----

*September 4, 2017*

**Fix**

* no longer install LICENSE file into installation directory (conflicts!)

2.8.1
-----

*July 21, 2017*

**Fix**

* the asyncio version of sleep() correctly returns a Future instance

2.8.0
-----

*June 8, 2017*

**New**

* run CI on Python 3.5 and 3.6

**Fix**

* asyncio - remove the hacks for "simulating" chained futures (no longer works - cpy36 has native code for future)

2.7.1
-----

*May 1, 2017*

**New**

* asyncio: example and docs for running multiple loops
* asyncio: log exception tracebacks when they're available for error-message

2.7.0
-----

*April 15, 2017*

**New**

* allow alternate asyncio loops
* new future creation API for alternate loops

2.6.1
-----

*February 9, 2017*

**New**

* added inline sleep helper (Twisted only for now)

2.6.0
-----

*December 29, 2016*

**Fix**

* avoid giving negative times to `callLater` with batched timers (issue #81)

2.5.2
-----

*November 6, 2016*

**Fix**

* fix pytest3/2
* fix Sphinx 1.4+ doc building

**Other**

* Copyrights transferred from Tavendo to Crossbar.io Technologies

2.5.1
-----

*April 28, 2016*

**Fix**

* Bug with ``make_batched_timer`` remembering (via a closure) the reactor/event-loop too persistantly

2.5.0
-----

*April 28, 2016*

**New**

* Objects returned from the :func:`txaio.make_batched_timer` API now have millisecond resolution and spread out their notifications over the entire range of the bucket

**Other**

* Document that ``@coroutine`` and ``@inlineCallbacks`` are not supported

2.4.0
-----

*April 22, 2016*

**New**

* Added :func:`txaio.make_batched_timer` API. The main use-case for this is when you have lots of of timers, but their exact resolution isn't important; batching them into buckets causes far fewer delayed call instances to be outstanding in the underlying event-loop/reactor.

2.3.1
-----

*April 10, 2016*

**New**

* added universal wheels

2.3.0
-----

*April 9, 2016*

**New**

* More logging infrastructure and APIs to support moving all of Crossbar.io's logging to txaio
.. _changelog-previous:

Previous Releases
-----------------

We didn't produce any release notes prior to 2.4.0. Instead of making up summaries
of all previous releases after the fact, you will have to do something like
``git log v1.1.0..v2.0.0`` to see what changed between releases. If you **do** make
a summary, pull-requests are welcome!
