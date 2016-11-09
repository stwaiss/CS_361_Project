#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from student import Student
from instructor import Instructor
from course import Course
from faq import FAQ
from question import Question
from timestamp import Timestamp
from reply import Reply

questionList = list()

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
    def checkForMatch(self, username, password):
        # open text file
        users = open('usernames.txt', 'r')

        # iterate over text file looking for match
        for line in users:
            infoList = line.strip().split(',')

            if infoList[0] == username:
                if infoList[1] == password:
                    # return isInstructor value
                    if infoList[2] == 0:
                        return 0
                    else:
                        return 1
        # if user is not matched, return -1
        return -1

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/ePantherID_Log-in.html')
        self.response.write(template.render())


class LoginHandler(webapp2.RequestHandler):
    postedUsername = ""
    postedPassword = ""
    match = -1

    def checkForMatch(self, username, password):
        # open text file
        users = open('usernames.txt', 'r')

        # iterate over text file looking for match
        for line in users:
            infoList = line.strip().split(',')

            if infoList[0] == str(username):
                if infoList[1] == str(password):
                    # return isInstructor value
                    if infoList[2] == str(0):
                        return 0
                    elif infoList[2] == str(1):
                        return 1
        # if user is not matched, return -1
        return -1

    def post(self):
        self.postedUsername = self.request.get('ePantherID')
        self.postedPassword = self.request.get('password')

        self.match = self.checkForMatch(self.postedUsername, self.postedPassword)

        if self.match == -1:
            values = {
                'credentials': self.match
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/ePantherID_Log-in.html')
            self.response.write(template.render(values))
            return

        elif self.match == 0:
            self.redirect('/student')
            return

        elif self.match == 1:
            self.redirect('/instructor')
            return


class StudentLandingPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Student_home.html')
        self.response.write(template.render())


class StudentAskHandler(webapp2.RequestHandler):
	def get(self):
		user = Student("jacksonj", "abc123")
		cs361 = Course("cs361")
		user.addCourse("cs361")
		cs361.addStudent(user)
		cs361.addInstructor(Instructor("rock", "123abc"))
		template = JINJA_ENVIRONMENT.get_template('HTML/Student_Submission_Form.html')
		self.response.write(template.render(user=user._ePantherID,course=user._courses,instructor=cs361._instructors))

	def post(self):
		q = question()
		q._body = self.request.get('textbox')
		q._student = self.request.get('user')
		q._instructor = self.request.get('instructor')
		q._title = q.getBody[:10]
		
		self.user.addQuestion(q)
		self.user.postQuestionToGlobal()
	
		self.redirect('/student')

class StudentFAQHandler(webapp2.RequestHandler):
   def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/FAQ.html')
        self.response.write(template.render())

class StudentViewAllQuestionsHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Student_View_All_Answers.html')
        self.response.write(template.render())


class InstructorLandingPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Instructor_home.html')
        self.response.write(template.render())


class AccountCreationHandler(webapp2.RequestHandler):
    def get(self):
        #Render HTML
        template = JINJA_ENVIRONMENT.get_template('HTML/AccountCreation.html')
        self.response.write(template.render())

    def post(self):
        pass
        # username = self.request.get("epantherID")
        # password = self.request.get("password")
        #
        # type = self.request.get("type")
        #
        #open file
        #check file for matching user name
        #if matched, give error, if not, write to file

        username=self.request.get('ePantherID')
        password=self.request.get('password')
        credential=self.request.get('credential')

        users=open('usernames.txt', 'r')

        userAlreadyExists = 0
        for line in users:
            infoList = line.strip().split(',')

            if infoList[0] == str(username):
                userAlreadyExists = 1
                values = {
                    'userAlreadyExists': userAlreadyExists,
                    'username': username
                }
                #Refresh and write error message
                template = JINJA_ENVIRONMENT.get_template('HTML/AccountCreation.html')
                self.response.write(template.render(values))
                break

        #### GAE does not support writing to local text files.
        # if credential == "instructor":
        #    users.write(username + ',' + password + ',1')
        # elif credential == "student":
        #    users.write(username + ',' + password + ',0')

        users.close()


class InstructorViewAllQuestionsHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Instructor View Questions.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/student', StudentLandingPageHandler),
    ('/student/ask', StudentAskHandler),
    ('/student/faq', StudentFAQHandler),
    ('/student/view_all', StudentViewAllQuestionsHandler),
    ('/instructor', InstructorLandingPageHandler),
    ('/instructor/create', AccountCreationHandler),
    ('/instructor/view_all', InstructorViewAllQuestionsHandler)

], debug=True)
