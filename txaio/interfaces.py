import abc
import six

@six.add_metaclass(abc.ABCMeta):
class ILoopMixin(object):
    """
    Some ideas for a Mixin-style API, similar to the FutureMixin that
    was in Autobahn.
    """

    @abs.abstractmethod
    def promise_create(self, value=None, exception=None):
        pass

    @abs.abstractmethod
    def promise_call(self, fun, *args, **kw):
        pass

    @abs.abstractmethod
    def promise_resolve(self, value):
        pass

    @abs.abstractmethod
    def promise_reject(self, exception=None):
        pass

    @abs.abstractmethod
    def promise_gather(self, promises, **kw):
        pass



@six.add_metaclass(abc.ABCMeta):
class IPromise(object):
    """
    Writing down some ideas for a Thing That Wraps A Future or a
    Deferred, as per some #twisted feedback
    """

    @abc.abastractproperty
    def future(self):
        """
        If we're wrapping a Future, return it. Else exception? or None?
        """

    @abc.abastractproperty
    def deferred(self):
        """
        If we're wrapping a Deferred, return it. Else exception? or None?
        """

    @abs.abstractmethod
    def add_callbacks(self, callback, errback):
        """
        Same as txaio.add_callbacks(promise, callback, errback) put we provide the promise.
        """

    @abs.abstractmethod
    def reject(self, exception=None):
        pass

    @abs.abstractmethod
    def resolve(self, value):
        pass




@six.add_metaclass(abc.ABCMeta)
class IFailedPromise(object):
    """
    This defines the interface for a common object encapsulating a
    failure from either an asyncio task/coroutine or a Twisted
    Deferred.

    An instance implementing this interface is given to any
    ``errback`` callables you provde via ``add_future_callbacks``
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
