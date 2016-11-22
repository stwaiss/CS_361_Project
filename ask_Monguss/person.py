import types
from google.appengine.ext import ndb

class Person(ndb.Model):
    ePantherID = ndb.StringProperty()
    password = ndb.StringProperty()
    isInstructor = ndb.IntegerProperty()

    def getePantherID(self):
        return self.ePantherID

    def getPassword(self):
        return self.password

        # returns 0 if student, 1 if instructor

    def getIsInstructor(self):
        return self._isInstructor

    def printInfo(self):
        print str(self.ePantherID) + ", " + str(self.password) + ", " + str(self._isInstructor)
