from google.appengine.ext import ndb


class FAQ(ndb.Model):
    question = ndb.StringProperty()
    answer = ndb.StringProperty()
    course = ndb.KeyProperty()
    ts = ndb.DateTimeProperty(auto_now_add=True)