# Developers Guide

## Coding Style

> The rules and text here follows [Django](https://docs.djangoproject.com/en/1.8/internals/contributing/writing-code/coding-style/).

Please follow these coding standards when writing code for inclusion in **txaio**.

1. Unless otherwise specified, follow [PEP 8](https://www.python.org/dev/peps/pep-0008). However, remember that PEP 8 is only a guide, so respect the style of the surrounding code as a primary goal.
2. Use 4 spaces for indents.
3. Use CamelCase for classes and snake_case for variables, functions and members, and UPPERCASE for constants.
4. Everything that is not part of the public API must be prefixed with a single underscore.
5. Rules 3 and 4 apply to the public API exposed by **txaio** for **both** Twisted and asyncio users as well as everything within the library itself.
6. An exception to PEP 8 is our rules on line lengths. Don’t limit lines of code to 79 characters if it means the code looks significantly uglier or is harder to read. We allow up to 119 characters as this is the width of GitHub code review; anything longer requires horizontal scrolling which makes review more difficult. Documentation, comments, and docstrings should be wrapped at 79 characters, even though PEP 8 suggests 72.
7. Use hanging indents with each argument strictly on a separate line to limit line length (see also [here](http://stackoverflow.com/questions/15435811/what-is-pep8s-e128-continuation-line-under-indented-for-visual-indent/15435837#15435837) for an explanation why this is PEP8 compliant):

```python
raise ApplicationError(
    u"crossbar.error.class_import_failed",
    u"Session not derived of ApplicationSession"
)
```

Code must be checked for PEP8 compliance using [flake8](https://flake8.readthedocs.org/en/2.4.1/) with [pyflakes](https://pypi.python.org/pypi/pyflakes) and [pep8-naming](http://pypi.python.org/pypi/pep8-naming) plugins installed:

    flake8 --max-line-length=119 txaio

There is no automatic checker for rule 4, hence reviewers of PRs should manually inspect code for compliance.
