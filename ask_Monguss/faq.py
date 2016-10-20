import types

class FAQ(object):
    def __init__(self, q, a):
        # forces faq question to be a string.
        if not isinstance(q, types.StringType):
            raise TypeError("FAQ.question only accepts String Objects")
        self.question = q

        # forces faq answer to be a string.
        if not isinstance(a, types.StringType):
            raise TypeError("FAQ.answer only accepts String Objects")
        self.answer = a
        self.timestamp = ''

    def __init__(self, q, a, ts):
        self.question = q
        self.answer = a
        self.timestamp = ts

    def addTimestamp(self, ts):
        if self.timestamp == '':
            self.timestamp = ts

    def getQuestion(self):
        return self.question

    def getAnswer(self):
        return self.answer

    def getTimestamp(self):
        return self.timestamp
