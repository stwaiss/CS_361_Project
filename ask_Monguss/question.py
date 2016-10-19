class Question:
    def __init__(self, body, faqAttachments):
        self.body = body
        self.faqAttachments = list()

        for i in range(0, len(faqAttachments), 1):
            self.faqAttachments.append(faqAttachments(i))

        self.replies = list()
        self.timestamps = list()
        self.currentStatus = 0

    def getBody(self):
        return self.body

    def getCurrentStatus(self):
        return self.currentStatus