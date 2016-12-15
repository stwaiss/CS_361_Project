import unittest
import webapp2
import jinja2
import os
from user import User
from course import Course
from faq import FAQ
from question import Question
import datetime
from google.appengine.ext import ndb

class AskMongussTest(unittest.TestCase):

	def ndb_test(self):
		test = Course(parent=ndb.Key("CS337"),name="CS337")
		test.put()
		test2 = Course.query("CS337").fetch()
		
		self.assertTrue(test2)
		
	def ndb_test2(self):
		test = Course.query("CS337").fetch()
		
		self.assertEqual(test[0].name, "CS337")
		
	def question_test(self):
		test = Question(topic="Test",body="None",student="hessaj",instructor="jrock",course="CS361")
		self.assertTrue(test.topic)
		self.assertEqual(test.topic, "Test")
		self.assertTrue(test.body)
		self.assertTrue(test.student)
		self.assertTrue(test.instructor)
		self.assertTrue(test.course)
		self.assertFalse(test.answer)
		
	def faq_test(self):
		test = FAQ(question="How?",answer="I don't know",course="CS361")
		self.assertTrue(test.question)
		self.assertEqual(test.question, "How?")
		self.assertTrue(test.answer)
		self.assertEqual(test.answer, "I don't know")
		self.assertTrue(test.course)
		self.assertEqual(test.course, "CS361")
		
	def user_test(self):
		test = User(ePantherID="hessaj",isInstructor="0")
		self.assertEqual(test.ePantherID, "hessaj")
		self.assertFalse(isInstructor)

if __name__ == '__main__':
    HTMLTestRunner.main()