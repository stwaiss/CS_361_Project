import unittest
import webapp2
import jinja2
import os
import sys
from user import User
from course import Course
from faq import FAQ
from question import Question
import datetime
from google.appengine.ext import ndb

class AskMongussTest(unittest.TestCase):

	def ndb_test(self):
		res = unittest.TestResult()
		test = Course(parent=ndb.Key("CS337"),name="CS337")
		test.put()
		test2 = Course.query("CS337").fetch()
		
		self.assertTrue(test2)
		
		print res
		
	def ndb_test2(self):
		res = unittest.TestResult()
		test = Course.query("CS337").fetch()
		
		self.assertEqual(test[0].name, "CS337")
		print res
		
	def question_test(self):
		res = unittest.TestResult()
		test = Question(topic="Test",body="None",student="hessaj",instructor="jrock",course="CS361")
		self.assertTrue(test.topic)
		self.assertEqual(test.topic, "Test")
		self.assertTrue(test.body)
		self.assertTrue(test.student)
		self.assertTrue(test.instructor)
		self.assertTrue(test.course)
		self.assertFalse(test.answer)
		print res
		
	def faq_test(self):
		res = unittest.TestResult()
		test = FAQ(question="How?",answer="I don't know",course="CS361")
		self.assertTrue(test.question)
		self.assertEqual(test.question, "How?")
		self.assertTrue(test.answer)
		self.assertEqual(test.answer, "I don't know")
		self.assertTrue(test.course)
		self.assertEqual(test.course, "CS361")
		print res
		
	def user_test(self):
		res = unittest.TestResult()
		test = User(ePantherID="hessaj",isInstructor="0")
		self.assertEqual(test.ePantherID, "hessaj")
		self.assertFalse(isInstructor)
		print res
		
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