###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from __future__ import print_function
import sys
import logging

import txaio
txaio.use_asyncio()


# some library you use is using txaio logging stuff
class Library(object):
    log = txaio.make_logger()

    def something(self):
        self.log.info("info log from library foo={foo}", foo='bar')
        self.log.debug("debug information")
        self.log.error("An error in the library num={num}", num=42)

lib = Library()
print("logging not started")

# you start you own logging; this is about the simplest way to.
lg = logging.getLogger()
lg.setLevel(logging.DEBUG)
logging.basicConfig()
lg.info('info-level log from my program: %d', 42)
print("logging started; calling library")
lib.something()
print("finished library call")
