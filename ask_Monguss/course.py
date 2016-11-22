from google.appengine.ext import ndb


class Course(ndb.Model):
    name = ndb.StringProperty()
    students = ndb.KeyProperty(repeated=True)
    instructors = ndb.KeyProperty(repeated=True)
    questions = ndb.KeyProperty(repeated=True)
    FAQ = ndb.KeyProperty(repeated=True)
