import types
from google.appengine.ext import ndb


class Reply(ndb.Model):
    body = ndb.StringProperty(required=True)
    status = ndb.IntegerProperty()
    instructor = ndb.KeyProperty()
    question = ndb.KeyProperty()