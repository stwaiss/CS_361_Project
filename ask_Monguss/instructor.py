import person


class Instructor(person):
    def __init__(self, ePantherID, password, credential = 1):
        super(Instructor, self).__init__(ePantherID, password, credential)
        courses = list()
        questions = list()