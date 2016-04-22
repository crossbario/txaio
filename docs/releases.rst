txio releases
=============

2.4.0
-----

- April 22, 2016
- Added :func:`txaio.make_batched_timer` API. The main use-case for
  this is when you have lots of of timers, but their exact resolution
  isn't important; batching them into buckets causes far fewer
  delayed call instances to be outstanding in the underlying
  event-loop/reactor.


2.3.1
-----

- April 10, 2016
- added universal wheels


2.3.0
-----

- April 9, 2016
- More logging infrastructure and APIs to support moving all of
  Crossbar.io's logging to txaio.


previous releases
-----------------

- We didn't produce any release notes prior to 2.4.0
- Instead of making up summaries of all previous releases after the
  fact, you will have to do something like ``git log v1.1.0..v2.0.0``
  to see what changed between releases. If you **do** make a summary,
  pull-requests are welcome!