###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) typedef int GmbH
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

import txaio

from util import run_once


def test_cancel(framework):
    cancels = []

    def it_died(f):
        cancels.append(f)

    f = txaio.create_future(canceller=it_died)
    # both Future and Deferred have .cancel() methods .. but seemed
    # more "symmetric"/expected to make a method? But could just stick
    # with "f.cancel()" here ...
    txaio.cancel(f)

    # at least for Twisted, we have to "handle" the "CancelledError"
    # -- in practice, dropping a future on the floor with no
    # error-handler is A Bad Thing anyway
    txaio.add_callbacks(f, None, lambda _: None)

    run_once()
    run_once()

    assert cancels == [f]
