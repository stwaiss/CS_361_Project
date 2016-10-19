class FAQ:
    def __init__(self, q, a):
        self.question = q
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
