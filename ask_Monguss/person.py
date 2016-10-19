class Person:
    def __init__(self, ePantherID, password, isInstructor):
        self.ePantherID = ePantherID
        self.password = password

        #only accept 0 or 1

        #need to throw an error if invalid
        if isInstructor == 0 or isInstructor == 1:
            self.isInstructor = isInstructor

    def getePantherID(self):
        return self.ePantherID

    def getPassword(self):
        return self.password

    #returns 0 if student, 1 if instructor
    def getIsInstructor(self):
        return self.isInstructor

    def getEmail(self):
        return str(self.ePantherID) + '@uwm.edu'