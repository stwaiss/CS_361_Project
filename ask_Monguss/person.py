class Person(object):
    def __init__(self, ePantherID, password, isInstructor):
        self._ePantherID = ePantherID
        self._password = password

        #only accept 0 or 1

        #need to throw an error if invalid
        if isInstructor == 0 or isInstructor == 1:
            self._isInstructor = isInstructor

    def getePantherID(self):
        return self._ePantherID

    def getPassword(self):
        return self._password

    #returns 0 if student, 1 if instructor
    def getIsInstructor(self):
        return self._isInstructor

    def getEmail(self):
        return str(self._ePantherID) + '@uwm.edu'