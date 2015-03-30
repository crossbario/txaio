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

# XXX FIXME
verstr = '0.0.0'
docstr = 'FIXME'

setup (
    name='taxio',
    version=verstr,
    description='compatibility API between asyncio/Twisted/Trollius',
    long_description=docstr,
    author='Tavendo GmbH',
    author_email='FIXME',
    url='FIXME',
    platforms=('Any'),
    install_requires=[
        'six'
    ],
    extras_require={
        'dev': [
            'pytest>=2.6.4',     # FIXME
            'pytest-cov>=1.8.1', # FIXME
            'pep8>=1.6.2',       # MIT

            'Sphinx>=1.2.3',     # BSD
            'alabaster>=0.6.3',  # BSD
        ],
        'twisted': [
            'twisted',
        ]
    },
    packages=['txaio'],
#    include_package_data=True,
#    data_files=[('.', ['LICENSE'])],
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
