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


import sys
import platform
from setuptools import setup

CPY = platform.python_implementation() == 'CPython'

with open('txaio/_version.py') as f:
    exec(f.read())  # defines __version__

with open('README.rst') as f:
    docstr = f.read()


# Twisted dependencies
#
extras_require_twisted = [
    'zope.interface>=5.2.0',            # Zope Public License
    'twisted>=20.3.0',                  # MIT
]

# asyncio dependencies: Python 3.5+ has asyncio builtin
#
extras_require_asyncio = []

# development dependencies
#
extras_require_dev = [
    'wheel',                            # MIT
    'pytest>=2.6.4',                    # MIT
    'pytest-cov>=1.8.1',                # MIT
    'pep8>=1.6.2',                      # MIT
    'sphinx>=1.2.3',                    # BSD
    'pyenchant>=1.6.6',                 # LGPL
    'sphinxcontrib-spelling>=2.1.2',    # BSD
    'sphinx_rtd_theme>=0.1.9',          # BSD
    'tox>=2.1.1',                       # MIT
    'twine>=1.6.5',                     # Apache 2.0
    'tox-gh-actions>=2.2.0 ',           # MIT
]

# everything
#
extras_require_all = extras_require_twisted + extras_require_asyncio


setup(
    name='txaio',
    version=__version__,
    description='Compatibility API between asyncio/Twisted/Trollius',
    long_description=docstr,
    license='MIT License',
    author='Crossbar.io Technologies GmbH',
    author_email='autobahnws@googlegroups.com',
    url='https://github.com/crossbario/txaio',
    platforms=('Any'),
    python_requires='>=3.6',
    extras_require={
        'twisted': extras_require_twisted,
        'asyncio': extras_require_asyncio,
        'dev': extras_require_dev,
        'all': extras_require_all
    },
    packages=['txaio'],

    # this flag will make files from MANIFEST.in go into _source_ distributions only
    include_package_data=True,

    # in addition, the following will make the specified files go into
    # source _and_ bdist distributions! For the LICENSE file
    # specifically, see setup.cfg
    # data_files=[('.', ['list', 'of', 'files'])],

    # this package does not access its own source code or data files
    # as normal operating system files
    zip_safe=True,

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Twisted",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords='asyncio twisted trollius coroutine',
)
