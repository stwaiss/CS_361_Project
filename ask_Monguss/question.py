from reply import Reply

class Question(object):
    def __init__(self, body, faqAttachments):
        self.body = body

        #faqAttachments is a list of ints, representing the indexes of applicable faqs from Course.faq[]
        self.faqAttachments = faqAttachments

        self.replies = list()
        self.timestamps = list()

    def getBody(self):
        return self.body

    #forces replies list to only consist of reply objects. Don't use question.replies[0] = ...
    def addReply(self, r):
        if not isinstance(r, Reply):
            raise TypeError("Question.replies only accepts Question Objects")
        self.questions.append(r)