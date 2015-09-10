###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH
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

from __future__ import absolute_import

import sys
from setuptools import setup, find_packages

verstr = "2.0.0"
docstr = """
``txaio`` is a helper library for writing code that runs unmodified on
both Twisted and asyncio.

This is like `six <http://pythonhosted.org/six/>`_, but for wrapping
over differences between Twisted and asyncio so one can write code
that runs unmodified on both (*aka* "source code compatibility"). In
other words: your users can choose if they want asyncio **or** Twisted
as a dependency.

    Note that, with this approach, user code runs under the native
    event loop of either Twisted or asyncio. This is different from
    attaching either one's event loop to the other using some event
    loop adapter.
"""

setup (
    name='txaio',
    version=verstr,
    description='Compatibility API between asyncio/Twisted/Trollius',
    long_description=docstr,
    author='Tavendo GmbH',
    author_email='autobahnws@googlegroups.com',
    url='https://github.com/tavendo/txaio',
    platforms=('Any'),
    install_requires=[
        'six'
    ],
    extras_require={
        'dev': [
            'pytest>=2.6.4',     # MIT
            'pytest-cov>=1.8.1', # MIT
            'pep8>=1.6.2',       # MIT

            'Sphinx>=1.2.3',     # BSD
            'alabaster>=0.6.3',  # BSD
        ],
        'twisted': [
            'twisted',          # MIT
        ]
    },
    packages=['txaio'],
    zip_safe=False,
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    #
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords='asyncio twisted coroutine',
)
