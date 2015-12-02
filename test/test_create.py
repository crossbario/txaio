import txaio


def test_illegal_args(framework):
    try:
        txaio.create_future(result=1, error=RuntimeError("foo"))
        assert False
    except ValueError:
        pass


def test_create_result(framework):
    f = txaio.create_future(result='foo')
    if txaio.using_twisted:
        assert f.called
    else:
        assert f.done()


def test_create_error(framework):
    f = txaio.create_future(error=RuntimeError("test"))
    if txaio.using_twisted:
        assert f.called
    else:
        assert f.done()
    # cancel the error; we expected it
    txaio.add_callbacks(f, None, lambda _: None)
