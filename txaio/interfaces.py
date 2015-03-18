import abc
import six


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
