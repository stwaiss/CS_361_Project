import datetime

class Timestamp(object):
    def __init__(self):

        #self.timestamps is a list of timestamp strings, generated from
        #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") when a status becomes changed
        self.timestamps = list()

        #self.statuses is the associated status with each item in the self.timestamps list.
        #I.E., if len(self.timestamps) == 3, then the associated status would be "Teacher Replied"
        #Python 2.7 doesn't have a "Java Enum" equivalent
        self.statuses = {
            '1': 'Student Posted',
            '2': 'Teacher Viewed',
            '3': 'Teacher Replied',
            '4': 'Student Viewed'
        }
