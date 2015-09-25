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
import platform
from setuptools import setup, find_packages

CPY = platform.python_implementation() == 'CPython'
PY3 = sys.version_info >= (3,)
PY33 = (3, 3) <= sys.version_info < (3, 4)

with open('txaio/_version.py') as f:
    exec(f.read())  # defines __version__

with open('README.rst') as f:
    docstr = f.read()

# asyncio dependencies
#
if PY3:
    if PY33:
        # "Tulip"
        extras_require_asyncio = [
            "asyncio>=3.4.3"        # Apache 2.0
        ]
    else:
        # Python 3.4+ has asyncio builtin
        extras_require_asyncio = []
else:
    # backport of asyncio for Python 2
    extras_require_asyncio = [
        "trollius>=2.0",            # Apache 2.0
        "futures>=3.0.3"            # BSD license
    ]

setup(
    name='txaio',
    version=__version__,
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
            'tox>=2.1.1'         # MIT
        ],
        'twisted': [
            'zope.interface>=3.6',  # Zope Public License
            'twisted>=12.1.0',      # MIT
        ],
        'asyncio': extras_require_asyncio
    },
    packages=['txaio'],
    zip_safe=False,
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
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
