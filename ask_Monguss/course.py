from google.appengine.ext import ndb


class Course(ndb.Model):
    name = ndb.StringProperty(required=True)
    students = ndb.KeyProperty(repeated=True)
    instructors = ndb.KeyProperty(repeated=True)
    questions = ndb.KeyProperty(repeated=True)
    FAQ = ndb.KeyProperty(repeated=True)
