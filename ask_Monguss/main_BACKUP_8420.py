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

        values = {
            'credentials': self.match,
            'username': self.postedUsername,
            'password': self.postedPassword
        }
        template = JINJA_ENVIRONMENT.get_template('HTML/login_dummy.html')
        self.response.write(template.render(values))


class StudentLandingPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Student_home.html')
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
		#
        #open file
        #check file for matching user name
        #if matched, give error, if not, write to file

class StudentAskHandler(webbapp2.RequestHandler):
		def get(self):
			template = JINJA_ENVIRONMENT.get_template('HTML/Student_Submission_Form.html')
			self.response.write(template.render())
        username=self.request.get('ePantherID')
        password=self.request.get('password')
        credential=self.request.get('credential')

<<<<<<< HEAD
	def post(self):
		q = new question()
		q._body = self.request.post('textbox')
		q._instructor = self.request.post('instructor')
		q._student = self.request.post('user')
		q._title = q.getBody[:10]
		
		addQuestion(q)
		postQuestionToGlobal()
		
		self.redirect('/student')
=======
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

class StudentAskHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Student_Submission_Form.html')
        self.response.write(template.render())

    def post(self):
		q = new question()
		q._body = self.request.post('textbox')
		q._student = self.request.post('user')
		q._instructor = self.request.post('instructor')
		q._title = q.getBody[:10]
		
        self.redirect('/student')
>>>>>>> origin/master

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
	('/instructor', InstructorLandingPage),
	('/student', StudentLandingPageHandler),
	('/instructor', InstructorLandingPageHandler),
	('/create', AccountCreationHandler),
	('/create', AccountCreationHandler),
	('/ask', StudentAskHandler)

], debug=True)
