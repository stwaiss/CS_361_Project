import datetime

class Timestamp(object):
    def __init__(self):

        #self.timestamps is a list of timestamp strings, generated from
        #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") when a status becomes changed
        self.timestamps = list()

        #self.statuses is the associated status with each item in the self.timestamps list.
        #I.E., if len(self.timestamps) == 3, then the associated status would be "Teacher Replied"
        self.statuses = list(
            "Student Posted", "Teacher Viewed",
            "Teacher Replied", "Student Viewed")

    def updateTimestamp(self):
        if len(self.timestamps) < 5:
            self.timestamps.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def getCurrentTimestamp(self):
        return self.timestamps(len(self.timestamps) - 1)

    def getCurrentStatus(self):
        return self.statuses(len(self.timestamps) - 1)