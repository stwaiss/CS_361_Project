import unittest
import HTMLTestRunner
import sys
from user import User
from course import Course
from faq import FAQ
from question import Question

class AskMongussTest(unittest.TestCase):
    def test_course(self):
        course = Course.query(Course.name == "CS361").fetch()[0]
        self.assertTrue(course.name == "CS361")

    def test_faq(self):
        cs361 = Course.query(Course.name == "CS361").fetch()[0]
        faq = FAQ(question="How?",answer="I don't know",course=cs361.key)
        self.assertTrue(faq.question)
        self.assertEqual(faq.question, "How?")
        self.assertTrue(faq.answer)
        self.assertEqual(faq.answer, "I don't know")
        self.assertTrue(faq.course)
        self.assertEqual(faq.course, Course.query(Course.name == "CS361").fetch()[0].key)

    def test_question(self):
        course = Course.query(Course.name == "CS361").fetch()[0]
        student = User.query(User.ePantherID == "janedoe").fetch()[0]
        instructor = User.query(User.ePantherID == "jrock").fetch()[0]
        question = Question(topic="Syllabus", body="When is the last day of class?",
                        answer="", student=student.key, instructor=instructor.key,
                        course=course.key)

        self.assertEqual(question.topic, "Syllabus")
        self.assertNotEqual(question.topic, "Exam")


    def test_user(self):
        test = User(ePantherID="hessaj", password="hessaj", isInstructor="0")
        self.assertEqual(test.ePantherID, "hessaj")
        self.assertFalse(test.isInstructor == 1)


class TestResult(object):

    """Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testcase, exceptioninfo), where exceptioninfo is the
    formatted traceback of the error that occurred.
    """

    _previousTestClass = None
    _testRunEntered = False
    _moduleSetUpFailed = False

    def __init__(self, stream=None, descriptions=None, verbosity=None):
        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = False
        self.buffer = False
        self._stdout_buffer = None
        self._stderr_buffer = None
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        self._mirrorOutput = False

        # List containing all the run tests, their index and their result. This is the new line of code.
        self.tests_run = []


    ###
    ### New function added
    ###

    def getTestsReport(self):
        """Returns the run tests as a list of the form [test_description, test_index, result]"""
        return self.tests_run
        ### Rest of the code

    ###
    ### Modified the functions so that we add the test case to the tests run list.
    ### -1 means Failure. 0 means error. 1 means success. 
    ###

    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """

        self.errors.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True
        self.tests_run.append([test.shortDescription(), self.testsRun, 0])

    def addFailure(self, test, err):

        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info()."""
        self.failures.append((test, self._exc_info_to_string(err, test)))
        self._mirrorOutput = True
        self.tests_run.append([test.shortDescription(), self.testsRun, -1])



    def addSuccess(self, test):
        "Called when a test has completed successfully"
        self.tests_run.append([test.shortDescription(), self.testsRun, 1])

if __name__ == '__main__':
    HTMLTestRunner.main()