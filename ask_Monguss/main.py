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
from user import User
from course import Course
from faq import FAQ
from question import Question
import datetime
from google.appengine.ext import ndb
from test import AskMongussTest
from test import TestResult
import unittest

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # check if generic janedoe account exists, if not, populate info for starting point
        student = User.query(User.ePantherID == "janedoe").fetch()
        if len(student) == 0:
            # create new course
            course_key = Course(name="CS361").put()

            # create new users
            janedoe_key = User(ePantherID="janedoe", password="janedoe", isInstructor=0).put()
            jrock_key = User(ePantherID="jrock", password="jrock", isInstructor=1).put()

            # pull course info from key
            course = course_key.get()

            # update course instructors by appending an instructor
            course.instructors.append(jrock_key)
            course.put()

            # update course students by appending a student
            course.students.append(janedoe_key)
            course.put()

            # pull instructor from key and add a course
            instructor = jrock_key.get()
            instructor.courses.append(course_key)
            instructor.put()

            # pull student from key and add a course
            student = janedoe_key.get()
            student.courses.append(course_key)
            student.put()

        template = JINJA_ENVIRONMENT.get_template('HTML/Login.html')
        self.response.write(template.render())


class LoginHandler(webapp2.RequestHandler):
    def post(self):
        postedUsername = self.request.get('ePantherID')
        postedPassword = self.request.get('password')

        # check if user is ADMIN
        if postedUsername == postedPassword == "ADMIN":
            self.response.set_cookie('name', postedUsername, path='/')
            self.redirect('/ADMIN')
            return

        # check if user is in system
        user_list = User.query(User.ePantherID == postedUsername, User.password == postedPassword).fetch()

        if len(user_list) != 0:
            user = user_list[0]

            if user.isInstructor == 0:
                self.response.set_cookie('name', postedUsername, path='/')
                self.redirect('/student')
                return

            if user.isInstructor == 1:
                self.response.set_cookie('name', postedUsername, path='/')
                self.redirect('/instructor')
                return

        # user isn't in system so render error message
        else:
            values = {
                'badCombo': 1
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Login.html')
            self.response.write(template.render(values))
            return


class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        # pull value from cookie key
        name = self.request.cookies.get('name')

        # delete cookie
        self.response.delete_cookie('name')

        # render successful log out template
        value = {
            'username': name
        }

        template = JINJA_ENVIRONMENT.get_template('HTML/logout.html')
        self.response.write(template.render(value))


class AllFAQHandler(webapp2.RequestHandler):
    # only one of two screens that doesn't use user authentication
    def get(self):
        # check if user selected course from dropdown
        # if not, render dropdown only
        if self.request.get('course') == "":
            allCourses = Course.query().fetch()

            values = {
                "allCourses": allCourses
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/All FAQ.html')
            self.response.write(template.render(values))

        # if selected, render selected course FAQ
        else:
            allCourses = Course.query().fetch()
            course = Course.query(Course.name == self.request.get('course')).fetch()[0]

            values = {
                "allCourses": allCourses,
                "isChosen": 1,
                "courseName": self.request.get('course'),
                "faq": course.FAQ
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/All FAQ.html')
            self.response.write(template.render(values))


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        # static document, so render as normal
        template = JINJA_ENVIRONMENT.get_template('HTML/About.html')
        self.response.write(template.render())


class ChangePasswordHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get('name')
        all_users = User.query(User.ePantherID == name).fetch()

        if len(all_users) != 0:
            curUser = all_users[0]
            value = {
                'username': name,
                'incorrectPassword': 0,
                'isInstructor': curUser.isInstructor
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Change Password.html')
            self.response.write(template.render(value))

        else:
            self.redirect('/')

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get('name')
        all_users = User.query(User.ePantherID == name).fetch()

        if len(all_users) != 0:
            curUser = all_users[0]

            curPassword = self.request.get('curPassword')
            newPassword = self.request.get('newPassword')

            # check if passwords match, then set new password
            if curPassword == curUser.password:
                curUser.password = newPassword
                curUser.put()

                values = {
                    "isInstructor": curUser.isInstructor
                }

                template = JINJA_ENVIRONMENT.get_template('HTML/Change Password Successful.html')
                self.response.write(template.render(values))
                return

            # if current password doesn't match, render error
            else:
                values = {
                    'username': curUser.ePantherID,
                    'incorrectPassword': 1
                }

                template = JINJA_ENVIRONMENT.get_template('HTML/Change Password.html')
                self.response.write(template.render(values))
                return

        else:
            self.redirect('/')


class StudentLandingPageHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        students = User.query(User.ePantherID == name, User.isInstructor == 0).fetch()

        # if cookie is correct, render page
        if len(students) != 0:
            curStudent = students[0]

            # pull counts of answered and unanswered questions
            allQuestionsQuery = Question.query(Question.student == curStudent.key)
            allQuestionsCount = allQuestionsQuery.count()

            answeredQuestionsCount = Question.query(Question.student == curStudent.key, Question.answer != "").count()
            unansweredQuestionsCount = allQuestionsCount - answeredQuestionsCount

            values = {
                "username": curStudent.ePantherID,
                "totalQuestions": allQuestionsCount,
                "answeredQuestions": answeredQuestionsCount,
                "unansweredQuestions": unansweredQuestionsCount
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/Student Home.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class StudentAskHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        students = User.query(User.ePantherID == name, User.isInstructor == 0).fetch()

        # if cookie is correct, render page
        if len(students) != 0:
            curStudent = students[0]

            # if dropdown hasn't been selected, render dropdown only
            if self.request.get('course') == "":
                values = {
                    'username': curStudent.ePantherID,
                    'course': curStudent.courses,
                    'isChosen': 0
                    # 'instructor': curStudent.instructor
                }

                template = JINJA_ENVIRONMENT.get_template('HTML/Student Question Submission Form.html')
                self.response.write(template.render(values))

            # else, render page with selected course and that course's instructors
            else:
                course_name = self.request.get('course')
                course = Course.query(Course.name == course_name).fetch()[0]
                values = {
                    'username': curStudent.ePantherID,
                    'course': curStudent.courses,
                    'isChosen': 1,
                    'instructors': course.instructors,

                    # this allows for info to be passed from get and post methods
                    'hiddencourse': course_name
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/Student Question Submission Form.html')
                self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        students = User.query(User.ePantherID == name, User.isInstructor == 0).fetch()

        # if cookie is correct, render page
        if len(students) != 0:

            # pull all values from form
            body = self.request.get('body')
            topic = self.request.get('topic')
            student_key = students[0].key
            instructor_name = self.request.get('instructor')
            instructor_key = User.query(User.ePantherID == instructor_name).fetch()[0].key
            time = datetime.datetime.now()
            course_name = self.request.get('hiddencourse')
            course_key = Course.query(Course.name == course_name).fetch()[0].key

            # create question entity
            q = Question(body=body, topic=topic, student=student_key, instructor=instructor_key, course=course_key,
                         date_submitted=time, answer="")

            # put question to datastore
            q_key = q.put()

            # add question to student's list
            curStudent = User.query(User.ePantherID == name).fetch()[0]
            curStudent.questions.append(q_key)
            curStudent.put()

            # add question to course list
            course = Course.query(Course.name == self.request.get('hiddencourse')).fetch()[0]
            course.questions.append(q_key)
            course.put()

            self.redirect('/student')

        # else redirect to login page
        else:
            self.redirect('/')


class StudentFAQHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        students = User.query(User.ePantherID == name, User.isInstructor == 0).fetch()

        # if cookie is correct, render page
        if len(students) != 0:

            # check if user has selected course from drop down
            # if no, render empty page to allow selection from drop down
            if self.request.get('course') == "":
                curStudent = students[0]
                values = {
                    "username": curStudent,
                    "isChosen": 0
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/Student FAQ.html')
                self.response.write(template.render(values))

            # if yes, render page with course faq from course drop down
            else:
                curStudent = students[0]
                course = Course.query(Course.name == self.request.get('course')).fetch()[0]

                values = {
                    "username": curStudent,
                    "isChosen": 1,
                    "courseName": self.request.get('course'),
                    "faq": course.FAQ
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/Student FAQ.html')
                self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class StudentViewAllQuestionsHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        students = User.query(User.ePantherID == name, User.isInstructor == 0).fetch()

        # if cookie is correct, render page
        if len(students) != 0:

            curStudent = students[0]
            values = {
                "username": curStudent.ePantherID,
                "questions": curStudent.questions
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/Student View All Answers.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class InstructorLandingPageHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            curInstructor = instructors[0]

            # pull various landing page statistics
            totalQuestions = Question.query(Question.instructor == curInstructor.key).count()
            answeredQuestions = Question.query(Question.instructor == curInstructor.key, Question.answer != "").count()
            unansweredQuestions = totalQuestions - answeredQuestions

            values = {
                "username": curInstructor.ePantherID,
                "totalQuestions": totalQuestions,
                "answeredQuestions": answeredQuestions,
                "unansweredQuestions": unansweredQuestions
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/Instructor Home.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class InstructorViewAllQuestionsHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            curInstructor = instructors[0]

            chosenCourse = self.request.get('courseName')
            # check if a dropdown has been selected, if not, set isChosen to 0 and don't render table
            if chosenCourse == "":
                values = {
                    "username": curInstructor.ePantherID,
                    "courses": curInstructor.courses,
                    "isChosen": 0
                }

            else:
                selected_course = Course.query(Course.name == chosenCourse).fetch()[0]
                question_list = Question.query(Question.course == selected_course.key,
                                               Question.instructor == curInstructor.key).fetch()
                values = {
                    "username": curInstructor.ePantherID,
                    "courses": curInstructor.courses,
                    "isChosen": 1,
                    "courseName": selected_course.name,
                    "questionsForInstructor": question_list

                }
            template = JINJA_ENVIRONMENT.get_template('HTML/Instructor View Questions.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class InstructorAnswerHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            curInstructor = instructors[0]

            # get question key from page and turn back into question entity
            question_key_string = self.request.get('question_key')
            question_key = ndb.Key(urlsafe=question_key_string)
            question = question_key.get()

            values = {
                "username": curInstructor.ePantherID,
                "question": question
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/Instructor Give Answer.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            curInstructor = instructors[0]

            # get question key from page and turn back into question entity
            question_key_string = self.request.get('question_key')
            question_key = ndb.Key(urlsafe=question_key_string)
            question = question_key.get()

            # update fields of question and put back
            question.answer = self.request.get('answer')
            question.date_answered = datetime.datetime.now()
            question.put()

            self.redirect('/instructor/view_all')


        # else redirect to login page
        else:
            self.redirect('/')


class InstructorFaqHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:

            # check if dropdown has been selected, if not, render list of courses
            if self.request.get('course') == "":
                curInstructor = instructors[0]
                values = {
                    "username": curInstructor,
                    "isChosen": 0
                }

                template = JINJA_ENVIRONMENT.get_template('HTML/Instructor FAQ.html')
                self.response.write(template.render(values))

            # if a dropdown has been selected, render that course's FAQ
            else:
                curInstructor = instructors[0]
                course = Course.query(Course.name == self.request.get('course')).fetch()[0]

                values = {
                    "username": curInstructor,
                    "isChosen": 1,
                    "courseName": self.request.get('course'),
                    "faq": course.FAQ
                }
                template = JINJA_ENVIRONMENT.get_template('HTML/Instructor FAQ.html')
                self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class InstructorFaqAddHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            curInstructor = instructors[0]
            values = {
                "username": curInstructor
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/Instructor FAQ Add.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            # add faq item to data store
            question = self.request.get('question')
            answer = self.request.get('answer')
            courseName = str(self.request.get('course'))
            faq = FAQ(question=question, answer=answer)
            faq_key = faq.put()

            # add faq key to course item
            course = Course.query(Course.name == courseName).fetch()[0]
            course.FAQ.append(faq_key)
            course.put()

            # add course key to faq item
            faq.course = course.key
            faq.put()

            self.response.write('<meta http-equiv="refresh" content="0.5;url=/instructor/faq">')

        # else redirect to login page
        else:
            self.redirect('/')


class InstructorFaqDeleteHandler(webapp2.RequestHandler):
    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        instructors = User.query(User.ePantherID == name, User.isInstructor == 1).fetch()

        # if cookie is correct, render page
        if len(instructors) != 0:
            curInstructor = instructors[0]

            # get key from hidden field
            faq_key_string = self.request.get('faq_key')
            faq_key = ndb.Key(urlsafe=faq_key_string)
            faq = faq_key.get()

            # delete faq entry from course
            course = faq.course.get()
            course.FAQ.remove(faq_key)
            course.put()

            # delete faq item
            faq_key.delete()

            # redirect back to faq page
            self.redirect('/instructor/faq')

        # else redirect to login page
        else:
            self.redirect('/')


class ADMINHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        # if cookie is correct, render page
        if name == "ADMIN":
            # various calculations for statistics
            numberOfStudents = User.query(User.isInstructor == 0).count()
            numberOfInstructors = User.query(User.isInstructor == 1).count()
            numberOfCourses = Course.query().count()
            studentInstructorRatio = round(float(numberOfStudents) / float(numberOfInstructors), 3)
            totalQuestionsCount = Question.query().count()
            answeredQuestionsCount = Question.query(Question.answer != "").count()
            unansweredQuestionsCount = totalQuestionsCount - answeredQuestionsCount

            values = {
                "username": "ADMINISTRATOR",
                "numberOfStudents": numberOfStudents,
                "numberOfInstructors": numberOfInstructors,
                "numberOfCourses": numberOfCourses,
                "studentInstructorRatio": studentInstructorRatio,
                "totalQuestions": totalQuestionsCount,
                "answeredQuestions": answeredQuestionsCount,
                "unansweredQuestions": unansweredQuestionsCount
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/ADMIN.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


class ADMINAccountCreationHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        if name == "ADMIN":
            values = {
                "username": "ADMINISTRATOR"
            }
            template = JINJA_ENVIRONMENT.get_template('HTML/Account Creation.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")

        if name == "ADMIN":

            # pull form data
            username = self.request.get('ePantherID')
            password = self.request.get('password')
            credential = self.request.get('credential')

            # if instructor is selected, create new instructor and render success message
            if credential == "instructor":
                list = User.query(User.ePantherID == username).fetch()
                if len(list) == 0:
                    newUser = User(ePantherID=username, password=password, isInstructor=1)
                    newUser.put()
                    values = {
                        'username': username,
                        'password': password,
                        'isInstructor': 1
                    }
                    # Refresh and write error message
                    template = JINJA_ENVIRONMENT.get_template('HTML/Account Creation Successful.html')
                    self.response.write(template.render(values))
                    return

                else:
                    userAlreadyExists = 1
                    values = {
                        'userAlreadyExists': userAlreadyExists,
                        'username': username
                    }
                    # Refresh and write error message
                    template = JINJA_ENVIRONMENT.get_template('HTML/Account Creation.html')
                    self.response.write(template.render(values))
                    return

            # if student is selected, create new student and render success message
            if credential == "student":
                list = User.query(User.ePantherID == username).fetch()
                if len(list) == 0:
                    newUser = User(ePantherID=username, password=password, isInstructor=0)
                    newUser.put()
                    values = {
                        'username': username,
                        'password': password,
                        'isInstructor': 0
                    }
                    # Refresh and write error message
                    template = JINJA_ENVIRONMENT.get_template('HTML/Account Creation Successful.html')
                    self.response.write(template.render(values))
                    return

                else:
                    userAlreadyExists = 1
                    values = {
                        'userAlreadyExists': userAlreadyExists,
                        'username': username
                    }
                    # Refresh and write error message
                    template = JINJA_ENVIRONMENT.get_template('HTML/Account Creation.html')
                    self.response.write(template.render(values))
                    return

        # else redirect to login page
        else:
            self.redirect('/')


class ADMINCourseCreationHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        if name == "ADMIN":

            # pull current list of all students and instructors
            all_instructors = User.query(User.isInstructor == 1).fetch()
            all_students = User.query(User.isInstructor == 0).fetch()

            values = {
                "username": "ADMINISTRATOR",
                "all_instructors": all_instructors,
                "all_students": all_students
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Course Creation.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')

    def post(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        if name == "ADMIN":
            # create course exists flag
            preexisting = 0

            # store form data
            course_ID = self.request.get('courseID')
            selected_instructors_list = self.request.get_all('instructors')
            selected_students_list = self.request.get_all('students')

            # check if at least one student and one instructor have been check, if not, render error message
            if len(selected_students_list) == 0 or len(selected_instructors_list) == 0:
                all_instructors = User.query(User.isInstructor == 1).fetch()
                all_students = User.query(User.isInstructor == 0).fetch()

                values = {
                    "username": "ADMINISTRATOR",
                    "all_instructors": all_instructors,
                    "all_students": all_students,
                    "empty_checkboxes": 1,
                }

                template = JINJA_ENVIRONMENT.get_template('HTML/Course Creation.html')
                self.response.write(template.render(values))
                return

            # check if course exists
            existingCourseList = Course.query(Course.name == course_ID).fetch()

            if len(existingCourseList) != 0:
                preexisting = 1
                existingCourse = existingCourseList[0]

                # iterate over check boxes to check if already added or to add new instructors to courses
                for i in selected_instructors_list:
                    # pull instructor from list
                    instructor = User.query(User.ePantherID == i).fetch()[0]

                    if instructor.key not in existingCourse.instructors:
                        # add course key to instructor and put back
                        instructor.courses.append(existingCourse.key)
                        instructor.put()

                        # add instructor key to course and put back
                        existingCourse.instructors.append(instructor.key)
                        existingCourse.put()

                # iterate over check boxes to add students to courses
                for s in selected_students_list:
                    student = User.query(User.ePantherID == s).fetch()[0]

                    if student.key not in existingCourse.students:
                        # add course key to student and put back
                        student.courses.append(existingCourse.key)
                        student.put()

                        # add student key to course and put back
                        existingCourse.students.append(student.key)
                        existingCourse.put()

            else:
                # create new course and retain key
                course_key = Course(name=course_ID).put()
                course = course_key.get()

                # iterate over check boxes to add instructors to courses
                for i in selected_instructors_list:
                    instructor = User.query(User.ePantherID == i).fetch()[0]

                    # add course key to instructor and put back
                    instructor.courses.append(course_key)
                    instructor.put()

                    # add instructor key to course and put back
                    course.instructors.append(instructor.key)
                    course.put()

                # iterate over check boxes to add students to courses
                for s in selected_students_list:
                    student = User.query(User.ePantherID == s).fetch()[0]

                    # add course key to student and put back
                    student.courses.append(course_key)
                    student.put()

                    # add student key to course and put back
                    course.students.append(student.key)
                    course.put()

            final_instructors_list = Course.query(Course.name == course_ID).fetch()[0].instructors
            final_students_list = Course.query(Course.name == course_ID).fetch()[0].students
            values = {
                "courseID": course_ID,
                "preexisting": preexisting,
                "addedStudents": selected_students_list,
                "addedInstructors": selected_instructors_list,
                "allStudents": final_students_list,
                "allInstructors": final_instructors_list
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/Course Creation Successful.html')
            self.response.write(template.render(values))


        # else redirect to login page
        else:
            self.redirect('/')


class ADMINTestCaseHandler(webapp2.RequestHandler):
    def get(self):
        # check for correct cookie
        name = self.request.cookies.get("name")
        if name == "ADMIN":
            suite = unittest.TestLoader().loadTestsFromTestCase(AskMongussTest)
            output = unittest.TestResult()
            suite.run(output)

            numberOfErrors = len(output.errors)
            numberOfFailures = len(output.failures)
            numberSkipped = len(output.skipped)

            values = {
                "username": "ADMINISTRATOR",
                "output": output,
                "numberOfErrors": numberOfErrors,
                "numberOfFailures": numberOfFailures,
                "numberSkipped": numberSkipped,
                "errors": output.errors,
                "failures": output.failures,
                "skipped": output.skipped,
                "suite": suite
            }

            template = JINJA_ENVIRONMENT.get_template('HTML/test.html')
            self.response.write(template.render(values))

        # else redirect to login page
        else:
            self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),
    ('/all_faq', AllFAQHandler),
    ('/about', AboutHandler),
    ('/change_password', ChangePasswordHandler),
    ('/student', StudentLandingPageHandler),
    ('/student/ask', StudentAskHandler),
    ('/student/faq', StudentFAQHandler),
    ('/student/view_all', StudentViewAllQuestionsHandler),
    ('/instructor', InstructorLandingPageHandler),
    ('/instructor/view_all', InstructorViewAllQuestionsHandler),
    ('/instructor/answer', InstructorAnswerHandler),
    ('/instructor/faq', InstructorFaqHandler),
    ('/instructor/faq/faq_add', InstructorFaqAddHandler),
    ('/instructor/faq/faq_delete', InstructorFaqDeleteHandler),
    ('/ADMIN', ADMINHandler),
    ('/ADMIN/create_user', ADMINAccountCreationHandler),
    ('/ADMIN/create_course', ADMINCourseCreationHandler),
    ('/ADMIN/test', ADMINTestCaseHandler)
], debug=True)
