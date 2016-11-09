import unittest, types
from question import Question
from faq import FAQ
from person import Person
from student import Student
from instructor import Instructor

class Course(object):
    _students = list()
    _instructors = list()
    _questions = list()
    _faq = list()

    def __init__(self, name):
        if not isinstance(name, types.StringType):
            raise TypeError("FAQ.question only accepts String Objects")
        self._courseName = name

    def getName(self):
        return self._courseName

    # forces student list to only consist of student objects. Don't use course.student[0] = ...
    def addStudent(self, s):
        if not isinstance(s,Student):
            raise TypeError("Course.students only accepts Student Objects")
        self._students.append(s)

    # forces instructor list to only consist of instructor objects. Don't use course.instructor[0] = ...
    def addInstructor(self, i):
        if not isinstance(i, Instructor):
            raise TypeError("Course.instructor only accepts Instructor Objects")
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


class testCourse(unittest.TestCase):
    def test_init(self):
        cs361 = Course("cs361")

        self.assertEqual(cs361._courseName, "cs361", "__init__() did not store name correctly")
        self.assertEqual(len(cs361._questions), 0, "There's no __init__() to add questions list")
        self.assertEqual(len(cs361._students), 0, "There's no __init__() to add students list")
        self.assertEqual(len(cs361._instructors), 0, "There's no __init__() to add instructors list")
        self.assertEqual(len(cs361._faq), 0, "There's no __init__() to add faq list")

    def test_getName(self):
        cs361 = Course("cs361")
        self.assertEqual(cs361.getName(), "cs361", "getName() does not return expected string")
        self.assertEqual(cs361.getName(), cs361._courseName, "getName() does not return _courseName")

    if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(Course)
        unittest.TextTestRunner(verbosity=2).run(suite)