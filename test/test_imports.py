import pytest


def test_use_twisted():
    pytest.importorskip('twisted')

    import txaio
    txaio.use_twisted()
    assert txaio.using_twisted
    assert not txaio.using_asyncio


def test_use_twisted_no_twisted():
    # make sure we DO NOT have Twisted installed
    try:
        import twisted  # noqa
        return
    except ImportError:
        pass  # no Twisted

    import txaio
    try:
        txaio.use_twisted()
        assert "Should have gotten ImportError"
    except ImportError:
        pass

    assert not txaio.using_twisted
    assert txaio.using_asyncio


def test_use_asyncio():
    pytest.importorskip('asyncio')

    import txaio
    txaio.use_asyncio()
    assert txaio.using_asyncio
    assert not txaio.using_twisted
