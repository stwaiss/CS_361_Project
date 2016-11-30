from google.appengine.ext import ndb

class List(ndb.Model):
    qanda = ndb.StringProperty()

class FAQ(ndb.Model):
    question = ndb.StringProperty()
    answer = ndb.StringProperty()
    ts = ndb.DateTimeProperty(auto_now_add=True)
    lists = ndb.StructuredProperty(List, repeated=True)

    def add_item(self, item):
        self.lists.append(item)
        self.put()