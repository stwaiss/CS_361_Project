from question import Question
from faq import FAQ


class Course(object):
    _students = list()
    _instructors = list()
    _questions = list()
    _faq = list()


    def __init__(self, name):
        self._courseName = name

    def getName(self):
        return self._courseName

    # forces student list to only consist of student objects. Don't use course.student[0] = ...
    def addStudent(self, s):
        if not isinstance(s,Student):
            raise TypeError("Course.students only accepts Question Objects")
        self._students.append(s)

    # forces instructor list to only consist of instructor objects. Don't use course.instructor[0] = ...
    def addInstructor(self, i):
        if not isinstance(i, Instructor):
            raise TypeError("Course.instructor only accepts Question Objects")
        self._instructors.append(i)

    # forces questions list to only consist of question objects. Don't use courses.questions[0] = ...
    def addQuestion(self, q):
        if not isinstance(q, Question):
            raise TypeError("Course.questions only accepts Question Objects")
        self._questions.append(q)

    # forces faq list to only consist of faq objects. Don't use course.faq[0] = ...
    def addFAQ(self, f):
        if not isinstance(f, FAQ):
            raise TypeError("Course.faq only accepts FAQ Objects")
        self._faq.append(f)