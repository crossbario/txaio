import abc
import six

@six.add_metaclass(abc.ABCMeta)
class ILoopMixin(object):
    """
    Some ideas for a Mixin-style API, similar to the FutureMixin that
    was in Autobahn.
    """

    @abc.abstractmethod
    def future_create(self, value=None, exception=None):
        pass

    @abc.abstractmethod
    def future_call(self, fun, *args, **kw):
        pass

    @abc.abstractmethod
    def future_resolve(self, value):
        pass

    @abc.abstractmethod
    def future_reject(self, exception=None):
        pass

    @abc.abstractmethod
    def future_gather(self, futures, **kw):
        pass



class FutureWrapper(object):
    """
    Writing down some ideas for a Thing That Wraps A Future or a
    Deferred, as per some #twisted feedback
    """

    def __init__(self, future):
        self.future = future

    def add_callbacks(self, callback, errback):
        """
        Same as txaio.add_callbacks(future, callback, errback) put we provide the future.
        """
        add_callbacks(self.future, callback, errback)

    def reject(self, exception=None):
        reject(self.future, exception=exception)

    @abc.abstractmethod
    def resolve(self, value):
        resolve(self.future, value)


@six.add_metaclass(abc.ABCMeta)
class IFailedFuture(object):
    """
    This defines the interface for a common object encapsulating a
    failure from either an asyncio task/coroutine or a Twisted
    Deferred.

    An instance implementing this interface is given to any
    ``errback`` callables you provde via ``add_future_callbacks``

    It is a subset of Twisted's Failure interface, because on Twisted
    backends it actually *is* a Failure.
    """

    @abc.abstractproperty
    def type(self):
        """
        The type of the exception. Same as the first item returned from
        ``sys.exc_info()``
        """

    @abc.abstractproperty
    def value(self):
        """
        An actual Exception instance. Same as the second item returned from
        ``sys.exc_info()``
        """

    @abc.abstractproperty
    def tb(self):
        """
        A traceback object from the exception. Same as the third item
        returned from ``sys.exc_info()``
        """

    @abc.abstractmethod
    def printTraceback(self, file=None):
        """
        Prints the exception and its traceback to the given ``file``. If
        that is ``None`` (the default) then it is printed to
        ``sys.stderr``.
        """

    @abc.abstractmethod
    def getErrorMessage(self):
        """
        Return a string describing the error.
        """

    # XXX anythign else make sense? Do we ape the *entire* Failure API?
