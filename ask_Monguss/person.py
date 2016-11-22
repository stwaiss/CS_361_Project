import types


class Person(object):
    _ePantherID = ''
    _password = ''

    def __init__(self, ePantherID, password, isInstructor):
        if not isinstance(ePantherID, types.StringType):
            raise TypeError("ePantherID only accepts String Objects")
        self._ePantherID = ePantherID

        if not isinstance(password, types.StringType):
            raise TypeError("password only accepts String Objects")
        self._password = password
        # only accept 0 or 1
        #  need to throw an error if invalid

        if isInstructor == 0 or isInstructor == 1:
            self._isInstructor = isInstructor
        else:
            raise Warning("Person.__init__() received bad value for isInstructor")

    def getePantherID(self):
        return self._ePantherID

    def getPassword(self):
        return self._password

        # returns 0 if student, 1 if instructor

    def getIsInstructor(self):
        return self._isInstructor

    def printInfo(self):
        print str(self._ePantherID) + ", " + str(self._password) + ", " + str(self._isInstructor)
