import person
import question


class Student(person):
    def __init__(self, ePantherID, password, credential = 0):
        super(Student, self).__init__(ePantherID, password, credential)
        courses = list()
        questions = list()

    def getClassByName(self, name):
        for i in range(0, len(self.courses), 1):
            if self.courses(i).getName() == name:
                return self.courses(i)
        return -1
