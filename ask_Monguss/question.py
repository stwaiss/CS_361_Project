import types
from google.appengine.ext import ndb


class Question(ndb.Model):
    # all required fields
    topic = ndb.StringProperty(required=True)
    body = ndb.StringProperty(required=True)
    student = ndb.KeyProperty(required=True)
    instructor = ndb.KeyProperty(required=True)
    course = ndb.KeyProperty(required=True)

    answer = ndb.StringProperty()
    date_submitted = ndb.DateTimeProperty()
    date_answered = ndb.DateTimeProperty()
