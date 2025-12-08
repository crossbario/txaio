Release Notes
=============

This page provides links to release artifacts for each version of txaio.

For detailed changelog entries, see :doc:`changelog`.


25.12.1
-------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v25.12.1>`__
* `PyPI Package <https://pypi.org/project/txaio/25.12.1/>`__
* `Documentation <https://txaio.readthedocs.io/en/v25.12.1/>`__


25.9.2
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v25.9.2>`__
* `PyPI Package <https://pypi.org/project/txaio/25.9.2/>`__
* `Documentation <https://txaio.readthedocs.io/en/v25.9.2/>`__


25.9.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v25.9.1>`__
* `PyPI Package <https://pypi.org/project/txaio/25.9.1/>`__
* `Documentation <https://txaio.readthedocs.io/en/v25.9.1/>`__


25.6.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v25.6.1>`__
* `PyPI Package <https://pypi.org/project/txaio/25.6.1/>`__
* `Documentation <https://txaio.readthedocs.io/en/v25.6.1/>`__


23.1.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v23.1.1>`__
* `PyPI Package <https://pypi.org/project/txaio/23.1.1/>`__
* `Documentation <https://txaio.readthedocs.io/en/v23.1.1/>`__


22.2.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v22.2.1>`__
* `PyPI Package <https://pypi.org/project/txaio/22.2.1/>`__
* `Documentation <https://txaio.readthedocs.io/en/v22.2.1/>`__


21.2.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v21.2.1>`__
* `PyPI Package <https://pypi.org/project/txaio/21.2.1/>`__


20.12.1
-------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v20.12.1>`__
* `PyPI Package <https://pypi.org/project/txaio/20.12.1/>`__


20.4.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v20.4.1>`__
* `PyPI Package <https://pypi.org/project/txaio/20.4.1/>`__


20.3.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v20.3.1>`__
* `PyPI Package <https://pypi.org/project/txaio/20.3.1/>`__


20.1.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v20.1.1>`__
* `PyPI Package <https://pypi.org/project/txaio/20.1.1/>`__


18.8.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v18.8.1>`__
* `PyPI Package <https://pypi.org/project/txaio/18.8.1/>`__


18.7.1
------

* `GitHub Release <https://github.com/crossbario/txaio/releases/tag/v18.7.1>`__
* `PyPI Package <https://pypi.org/project/txaio/18.7.1/>`__


--------------

Release Workflow (for Maintainers)
----------------------------------

This section documents the release process for maintainers.


Prerequisites
^^^^^^^^^^^^^

Before releasing, ensure you have:

* Push access to the repository
* PyPI credentials configured (or trusted publishing via GitHub Actions)
* ``just`` and ``uv`` installed


Step 1: Draft the Release
^^^^^^^^^^^^^^^^^^^^^^^^^

Generate changelog and release note templates:

.. code-block:: bash

   # Generate changelog entry from git history (for catching up)
   just prepare-changelog <version>

   # Generate release draft with templates for both files
   just draft-release <version>

This will:

* Add a changelog entry template to ``docs/changelog.rst``
* Add a release entry template to ``docs/releases.rst``
* Update the version in ``pyproject.toml``


Step 2: Edit Changelog
^^^^^^^^^^^^^^^^^^^^^^

Edit ``docs/changelog.rst`` and fill in the changelog details:

* **New**: New features and capabilities
* **Fix**: Bug fixes
* **Other**: Breaking changes, deprecations, other notes


Step 3: Validate the Release
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure everything is in place:

.. code-block:: bash

   just prepare-release <version>

This validates:

* Changelog entry exists for this version
* Release entry exists for this version
* Version in ``pyproject.toml`` matches
* All tests pass
* Documentation builds successfully


Step 4: Commit and Tag
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   git add docs/changelog.rst docs/releases.rst pyproject.toml
   git commit -m "Release <version>"
   git tag v<version>
   git push && git push --tags


Step 5: Automated Release
^^^^^^^^^^^^^^^^^^^^^^^^^

After pushing the tag:

1. GitHub Actions builds and tests the release
2. Wheels and source distributions are uploaded to GitHub Releases
3. PyPI publishing is triggered via trusted publishing (OIDC)
4. Read the Docs builds documentation for the tagged version


Manual PyPI Upload (if needed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If automated publishing fails:

.. code-block:: bash

   just download-github-release v<version>
   just publish-pypi "" v<version>
