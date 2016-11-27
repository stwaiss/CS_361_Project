from course import Course
from person import Person
from question import Question
from google.appengine.ext import ndb

class Instructor(Person):
    courses = ndb.LocalStructuredProperty(Course, repeated=True)
    questions = ndb.LocalStructuredProperty(Question, repeated=True)