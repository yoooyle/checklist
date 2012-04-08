from google.appengine.api import users
from google.appengine.ext import db

class Checklist(db.Model):
  """Data Model for Checklist.
    
    A Checklist contains multiple ListItems. 
    A user can have multiple Checklist.
  """  
  title = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
  
class ListItem(db.Model):
  """Data Model for checklist Items.
  """
  # Item contents.
  title = db.StringProperty(required=True)
  details = db.TextProperty()
  link = db.LinkProperty()
  snapshot = db.BlobProperty()
  
  # Meta data about people.
  assigner = db.UserProperty(required=True)
  assignees = db.ListProperty(users.User)
  
  # Meta data about time.
  created = db.DateTimeProperty(auto_now_add=True)
  deadline = db.DateTimeProperty()

  # Other Meta data.
  priority = db.RatingProperty()
  finished = db.BooleanProperty()
  checklist = db.ReferenceProperty(Checklist)