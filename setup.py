##############################################################################
#
#  Copyright (C) 2011-2015 Tavendo GmbH
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License, version 3,
#  as published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from __future__ import absolute_import

import sys
from setuptools import setup, find_packages

verstr = "1.0.0"
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
    description='compatibility API between asyncio/Twisted/Trollius',
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
