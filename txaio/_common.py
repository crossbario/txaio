
from txaio.interfaces import IBatchedTimer


class _BatchedCall(object):
    """
    Wraps IDelayedCall-implementing objects, implementing only the API
    which txaio promised in the first place: .cancel

    Do not create these yourself; use _BatchedTimer.call_later()
    """

    def __init__(self, timer, index, the_call):
        # XXX WeakRef?
        self._timer = timer
        self._index = index
        self._call = the_call

    def cancel(self):
        self._timer._remove_call(self._index, self)
        self._timer = None

    def __call__(self):
        return self._call()


class _BatchedTimer(IBatchedTimer):
    """
    Internal helper.

    Instances of this are returned from
    :meth:`txaio.make_batched_timer` and that is the only way they
    should be instantiated. You may depend on methods from the
    interface class only (:class:`txaio.IBatchedTimer`)
    """

    def __init__(self, bucket_seconds, chunk_size,
                 seconds_provider, delayed_call_creator):
        self._bucket_seconds = bucket_seconds
        self._chunk_size = chunk_size
        self._get_seconds = seconds_provider
        self._create_delayed_call = delayed_call_creator
        self._buckets = dict()  # real seconds -> (IDelayedCall, list)

    def call_later(self, delay, func, *args, **kwargs):
        """
        IBatchedTimer API
        """
        # "quantize" the delay to the nearest bucket (note: always
        # doing floor essentially, so e.g. 29.9 with 5s buckets still
        # gets you "25s from now") -- arguably would be better to
        # "properly round"? Minimizes average error, but some delays
        # get longer ... hmm.
        real_time = int(self._get_seconds() + delay)
        real_time -= (real_time % self._bucket_seconds)
        call = _BatchedCall(self, real_time, lambda: func(*args, **kwargs))
        try:
            self._buckets[real_time][1].append(call)
        except KeyError:
            # new bucket; need to add "actual" underlying IDelayedCall
            delayed_call = self._create_delayed_call(
                real_time,
                self._notify_bucket, real_time,
            )
            self._buckets[real_time] = (delayed_call, [call])
        return call

    def _notify_bucket(self, real_time):
        """
        Internal helper. This 'does' the callbacks in a particular bucket.

        :param real_time: the bucket to do callbacks on
        """
        (delayed_call, calls) = self._buckets[real_time]
        del self._buckets[real_time]
        errors = []

        def notify_one_chunk(calls, chunk_size):
            for call in calls[:chunk_size]:
                try:
                    call()
                except Exception as e:
                    errors.append(e)
            calls = calls[chunk_size:]
            if calls:
                self._create_delayed_call(
                    0,
                    lambda: notify_one_chunk(calls, chunk_size),
                )
            else:
                # done all calls; make sure there were no errors
                if len(errors):
                    msg = u"Error(s) processing call_later bucket:\n"
                    for e in errors:
                        msg += u"{}\n".format(e)
                    raise RuntimeError(msg)
        notify_one_chunk(calls, self._chunk_size)

    def _remove_call(self, real_time, call):
        """
        Internal helper. Removes a (possibly still pending) call from a
        bucket. It is *not* an error of the bucket is gone (e.g. the
        call has already happened).
        """
        try:
            (delayed_call, calls) = self._buckets[real_time]
        except KeyError:
            # no such bucket ... error? swallow?
            return
        # remove call; if we're empty, cancel underlying
        # bucket-timeout IDelayedCall
        calls.remove(call)
        if not calls:
            del self._buckets[real_time]
            delayed_call.cancel()
