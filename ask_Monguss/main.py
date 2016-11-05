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

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
    postedUsername = ""
    postedPassword = ""

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/ePantherID_Log-in.html')
        self.response.write(template.render())

    def post(self):
        self.postedUsername = self.request.get('ePantherID')
        self.postedPassword = self.request.get('password')

class LoginHandler(webapp2.RequestHandler):
    def checkForMatch(self, postedUsername, postedPassword):
        #open text file
        users = open('usernames.txt', 'r')

        #iterate over text file looking for match
        for line in users:
            infoList = line.strip().split(',')

            if infoList[0] == MainHandler.postedUsername:
                if infoList[1] == MainHandler.postedPassword:
                    #return isInstructor value
                    if infoList[2] == 0:
                        return 0
                    else:
                        return 1
        #if user is not matched, return -1
        return -1

    def post(self):
        match = self.checkForMatch(MainHandler.postedUsername, MainHandler.postedPassword)
        values = {
            'credentials': match,
            'username': MainHandler.postedUsername,
            'password': MainHandler.postedPassword
        }
        template = JINJA_ENVIRONMENT.get_template('HTML/login_dummy.html')
        self.response.write(template.render(values))


class StudentLandingPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Student_home.html')
        self.response.write(template.render())

class InstructorLandingPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/Instructor_home.html')
        self.response.write(template.render())

class AccountCreationHandler(webapp2.RequestHandler):
    def get(self):
        #Render HTML
        pass

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





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/student', StudentLandingPage),
    ('/instructor', InstructorLandingPage),
    ('/create', AccountCreationHandler)

], debug=True)
