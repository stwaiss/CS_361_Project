from google.appengine.ext import ndb
from course import Course


class User(ndb.Model):
    ePantherID = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    isInstructor = ndb.IntegerProperty(required=True)
    #courses = ndb.SructuredProperty(Course, repeated=True)