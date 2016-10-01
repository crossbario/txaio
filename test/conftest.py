import pytest

# here's a little voodoo -- any generic tests depend on this 'framework'
# fixture, which (sneakily using internal-only APIs) ensures that each
# tests runs twice: once enabled for Twisted and once enabled for
# asyncio.
#
# ...but there's a catch: not all environments support both, so we
# catch ImportError and skip those tests.
#
# To write a test that only works on one or the other framework, use
# the framework_tx or framework_aio fixtures instead


@pytest.fixture(
    params=['twisted', 'asyncio'],
)
def framework(request):
    """
    This is a framework that uses txaio internals to set up a
    framework to use, as the 'official' way is to call .use_twisted()
    or .use_asyncio() -- but we want to test with both frameworks if
    they're available.
    """

    try:
        if request.param == 'twisted':
            return framework_tx()
        elif request.param == 'asyncio':
            return framework_aio()
    except ImportError:
        pytest.skip()


@pytest.fixture
def framework_uninitialized():
    import txaio
    from txaio import _unframework
    txaio._use_framework(_unframework)
    txaio._explicit_framework = None
    return _unframework


@pytest.fixture
def framework_tx():
    try:
        import txaio
        from txaio import tx
        tx._loggers = set()
        txaio._use_framework(tx)
        txaio._explicit_framework = 'twisted'
        return tx
    except ImportError:
        pytest.skip()


@pytest.fixture
def framework_aio():
    try:
        import txaio
        from txaio import aio
        aio._loggers = set()
        txaio._use_framework(aio)
        txaio._explicit_framework = 'asyncio'
        return aio
    except ImportError:
        pytest.skip()
