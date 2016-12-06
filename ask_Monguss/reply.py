import types
from google.appengine.ext import ndb


class Reply(ndb.Model):
    body = ndb.StringProperty(required=True)
    timestamp = ndb.DateTimeProperty()
    instructor = ndb.KeyProperty()
    question = ndb.KeyProperty()