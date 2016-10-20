import types

class Reply(object):
    def __init__(self, body):
        if isinstance(body, types.StringType):
            raise TypeError("Reply.body only accepts String Objects")
        self.body = body
        self.timestamps = list()
        self.currentStatus = 0
