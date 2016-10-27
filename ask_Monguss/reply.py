import types


class Reply(object):
    _body = ''
    _timestamps = list()
    _currentStatus = 0

    def __init__(self, body):
        if isinstance(body, types.StringType):
            raise TypeError("Reply.body only accepts String Objects")
        self._body = body
