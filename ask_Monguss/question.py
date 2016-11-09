import types
from reply import Reply

class Question(object):
    _body = ''
    _faqAttachments = list()
    _replies = list()
    _timestamp = ''
    _student = ''
    _instructor = ''
    _title = ''
    _status = ''


    def __init__(self, body):
        if not isinstance(body, types.StringType):
            raise TypeError("FAQ.question only accepts String Objects")
        self._body = body

        self._replies = list()
        self._timestamps = list()

    def getBody(self):
        return self._body
		
	def getTitle(self):
		return self._title
		
	def getStudent(self):
		return self._student
		
	def getInstructor(self):
		return self._instructor

    #forces replies list to only consist of reply objects. Don't use question.replies[0] = ...
    def addReply(self, r):
        if not isinstance(r, Reply):
            raise TypeError("Question.replies only accepts Question Objects")
        self.questions.append(r)