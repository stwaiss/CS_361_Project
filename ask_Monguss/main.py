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
import time
import datetime
from google.appengine.ext import ndb

questionList = list()

#Mockup help
sampleStudent = Student("Sample Student","abc123")
sampleInstructor = Instructor("Sample Instructor","abc123")
sampleCourse = Course("Sample Course")
sampleInstructor.addCourse(sampleCourse)
sampleStudent.addCourse(sampleCourse)
sampleCourse.addStudent(sampleStudent)
sampleCourse.addQuestion(Question("This is a default question."))

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
                    elif infoList[2] == str(2):
                        return 2
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
            self.response.set_cookie('name', self.postedUsername, path='/')
            self.redirect('/student')
            return

        elif self.match == 1:
            self.response.set_cookie('name', self.postedUsername, path='/')
            self.redirect('/instructor')
            return

        elif self.match == 2:
            self.response.set_cookie('name', self.postedUsername, path='/')
            self.redirect('/ADMIN')
            return


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.cookies.get("name")
        self.response.delete_cookie(name)
        value = {
            'username':name
        }

        template = JINJA_ENVIRONMENT.get_template('HTML/logout.html')
        self.response.write(template.render(value))


class StudentLandingPageHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.cookies.get("name")


        template = JINJA_ENVIRONMENT.get_template('HTML/Student_home.html')
        self.response.write(template.render(questions=self.user.getQuestionsFromGlobal()))


class StudentAskHandler(webapp2.RequestHandler):
    def get(self):
        values = {
            'user':self.user._ePantherID,
            'course': self.user._courses,
            'instructor': self.instructor
        }

        template = JINJA_ENVIRONMENT.get_template('HTML/Student_Submission_Form.html')
        self.response.write(template.render(values))

    def post(self):
        q = Question(str(self.request.get('textbox')))
        q._student = self.request.get('user')
        q._instructor = self.request.get('instructor')
        q.timestamp = datetime.datetime.now().strftime('%m-%d-%Y')

        self.user.addQuestion(q)
        print "Question posted successfully. Redirecting..."
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
        self.response.write(template.render(instructor = self.user.getQuestionsFromGlobal()))



# FAQ add question/ delete question
render_parameter = {}
render_parameter['prev_question'] = ''
render_parameter['prev_answer'] = ''

render_parameter_q = {}
render_parameter_q['prev_q'] = ''

class List(ndb.Model):
    qanda = ndb.StringProperty()

class Faq(ndb.Model):
    question = ndb.StringProperty()
    answer = ndb.StringProperty()
    ts = ndb.DateTimeProperty(auto_now_add=True)
    lists = ndb.StructuredProperty(List, repeated=True)

    def add_item(self, item):
        self.lists.append(item)
        self.put()


class FaqHandler(webapp2.RequestHandler):
    def get(self):
        faqs = list(Faq.query().order(Faq.ts))
        render_parameter = {}
        render_parameter['faqs'] = faqs
        template = JINJA_ENVIRONMENT.get_template('HTML/InstructorFAQ.html')
        self.response.write(template.render(render_parameter))

class FaqAddHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/FAQadd.html')
        output = template.render(render_parameter)
        self.response.write(output)
        render_parameter['prev_question'] = ''
        render_parameter['prev_answer'] = ''

    def post(self):
        question = self.request.get('question')

        answer = self.request.get('answer')
        faq = Faq(question=question, answer=answer)
        faq.put()
        render_parameter['prev_question'] = question
        render_parameter['prev_answer'] = answer
        self.response.write('<meta http-equiv="refresh" content="0.5;url=/instructor/faq">')

class DeleteHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('HTML/FAQdelete.html')
        faqs = Faq.query().fetch(projection=[Faq.question])
        render_parameter_q['faqs'] = faqs
        self.response.write(template.render(render_parameter_q))
        render_parameter_q['prev_q'] = ''

    def post(self):
        question = self.request.get('question')
        faqs = list(Faq.query().fetch())
        render_parameter_q['prev_q'] = question
        for q in faqs:
          q.key.delete()
        self.redirect('/instructor/faq')

class ADMINHandler(webapp2.RequestHandler):
    def get(self):
        numberOfStudents = len(Student.query())
        numberOfInstructors = len(Instructor.query())
        numberOfCourses = len(Course.query())
        studentInstructorRatio = numberOfStudents/numberOfInstructors


        values = {
            "numberOfStudents":numberOfStudents,
            "numberOfInstructors": numberOfInstructors,
            "numberOfCourses": numberOfCourses,
            "studentInstructorRatio":studentInstructorRatio
        }

        template = JINJA_ENVIRONMENT.get_template('HTML/ADMIN.html')
        self.response.write(template.render(values))

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/student', StudentLandingPageHandler),
    ('/student/ask', StudentAskHandler),
    ('/student/faq', StudentFAQHandler),
    ('/student/view_all', StudentViewAllQuestionsHandler),
    ('/instructor', InstructorLandingPageHandler),
    ('/instructor/create', AccountCreationHandler),
    ('/instructor/view_all', InstructorViewAllQuestionsHandler),
    ('/instructor/faq', FaqHandler),
    ('/instructor/faq/faqadd', FaqAddHandler),
    ('/instructor/faq/faqdelete', DeleteHandler),
    ('/ADMIN', ADMINHandler)

], debug=True)
