import types
from reply import Reply
from google.appengine.ext import ndb


class Question(ndb.Model):
    # all required fields
    topic = ndb.StringProperty(required=True)
    body = ndb.StringProperty(required=True)
    student = ndb.KeyProperty(required=True)
    instructor = ndb.KeyProperty(required=True)
    course = ndb.KeyProperty(required=True)

    answer = ndb.StringProperty()
    faqAttachments = ndb.KeyProperty(repeated=True)
    replies = ndb.StructuredProperty(Reply, repeated=True)
    timestamp = ndb.DateTimeProperty()
