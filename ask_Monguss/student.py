import unittest
from person import Person
from course import Course
from question import Question


class Student(Person):
	_courses = list()
	_questions = list()
	_name = ''

	def __init__(self, ePantherID, password):
		super(Student, self).__init__(ePantherID, password, 0)

	def getCourseByName(self, name):
		for i in range(0, len(self._courses), 1):
			if self._courses[i].getName() == name:
				return self._courses[i]
		return -1

	def getCourseByIndex(self, i):
		return self._courses[i]

    #forces courses list to only consist of course objects. Don't use student.courses[0] = ...
	def addCourse(self, c):
		if not isinstance(c, Course):
			raise TypeError("Student.questions only accepts Course Objects")
		self._courses.append(c)

    #forces questions list to only consist of question objects. Don't use student.questions[0] = ...
	def addQuestion(self, q):
		if not isinstance(q, Question):
			raise TypeError("Student.questions only accepts Question Objects")
		self._questions.append(q)

	def getQuestion(self, i):
		return self._questions[i]
		
	def getQuestionsFromGlobal(self):
		global questionList
		tempList = list()
		
		for q in questionList:
			if q.getStudent == self._ePantherID:
				tempList.append(question)
				
		self._questions = tempList
				
	def postQuestionToGlobal(self):
		global questionList
		
		for Question in self._questions:
			for I in questionList:
				if Question.getTitle == I.getTitle:
					continue
				else:
					questionList.append(Question)
	

class testStudent(unittest.TestCase):
    def testStudentInit(self):
        jsmith = Student("jsmith", "1234abc")
        self.assertEqual(jsmith.getePantherID(), "jsmith", "EPantherID does not match")
        self.assertEqual(jsmith.getPassword(), "1234abc", "Password does not match")
        self.assertEqual(jsmith.getEmail(), "jsmith@uwm.edu", "Email does not match")
        self.assertEqual(jsmith.getIsInstructor(), 0, "jsmith is a student, not an instructor")

    def test_addCourse_and_getCourseByName(self):
        cs250 = Course("cs250")
        cs251 = Course("cs251")
        cs351 = Course("cs351")
        cs361 = Course("cs361")

        jdoe = Student("jdoe", "1234abc")
        jdoe.addCourse(cs250)
        jdoe.addCourse(cs251)
        jdoe.addCourse(cs351)
        jdoe.addCourse(cs361)

        #checks if error is raised when bad parameter is passed
        with self.assertRaises(TypeError):
            jdoe.addCourse(-20)

        self.assertEqual(jdoe.getCourseByName("cs250"), cs250, "getCourse() did not return correctly")
        self.assertEqual(jdoe.getCourseByName("ee234"), -1, "getCourse() did not return correctly")

    def test_addQuestion_and_getQuestion(self):
        jdoe = Student("jdoe", "1234abc")

        q1 = Question("q1", [1,4])
        q2 = Question("q2", [])

        jdoe.addQuestion(q1)
        jdoe.addQuestion(q2)
        self.assertEqual(jdoe.getQuestion(0), q1, "getQuestion() did not return correctly")
        self.assertEqual(jdoe.getQuestion(1), q2, "getQuestion() did not return correctly")

        self.assertEqual(jdoe.getQuestion(0).getBody(), "q1", "getBody() did not return correctly")
        self.assertEqual(jdoe.getQuestion(1).getBody(), "q2", "getBody() did not return correctly")

    if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(Student)
        unittest.TextTestRunner(verbosity=2).run(suite)

