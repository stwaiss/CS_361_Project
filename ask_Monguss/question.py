import types
from reply import Reply
from google.appengine.ext import ndb


class Question(ndb.Model):
    topic = ndb.StringProperty(required=True)
    body = ndb.StringProperty(required=True)
    faqAttachments = ndb.KeyProperty(repeated=True)
    replies = ndb.StructuredProperty(Reply)
    timestamp = ndb.DateTimeProperty(repeated=True)
    status = ndb.IntegerProperty()
    student = ndb.KeyProperty(required=True)
    instructor = ndb.KeyProperty(required=True)