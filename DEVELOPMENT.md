# Development

Notes specific to **txaio**: development setup, running the tests, and supported runtimes. The
contribution workflow shared by all WAMP projects — GitHub issue first, red → green tests, and the
AI-assistance disclosure — is in [CONTRIBUTING.md](CONTRIBUTING.md).

## Reporting bugs

In addition to what CONTRIBUTING.md asks for, please include:

- the txaio version: `python -c "import txaio; print(txaio.__version__)"`
- the networking framework in use: **Twisted** or **asyncio**

## Development setup

Development is driven by [`just`](https://github.com/casey/just) and [`uv`](https://github.com/astral-sh/uv);
run `just` to list all recipes. Every recipe takes the name of a managed virtual environment:
`cpy314`, `cpy313`, `cpy312`, `cpy311` (CPython) or `pypy311` (PyPy).

```bash
git clone https://github.com/crossbario/txaio.git
cd txaio
git submodule update --init --recursive
just create cpy314
just install-dev cpy314
```

## Running the tests

```bash
just test cpy314            # the test suite
just test pypy311           # the same on PyPy
just check cpy314           # formatting, typing and the other checks
```

**Supported runtimes:** CPython 3.11–3.14 and PyPy 3.11. txaio exists to let code run unmodified on
**both Twisted and asyncio**, so every change must behave the same on both frameworks.

## Code style

`ruff` enforces formatting and linting (`just check-format cpy314`); the line length is 88. Add
docstrings for public APIs, and type hints for new code (`just check-typing cpy314`).

## Documentation

The documentation is reStructuredText, built with Sphinx: `just docs cpy314`.
