from google.appengine.ext import db

class Notification(db.Model):
  """
  Notification object contains info to locate the entity that has changed.
  """
  item_cl = db.ReferenceProperty(db.Model, required=True)
  message = db.StringProperty(required=True)
  user = db.UserProperty(required=True)
  read = db.BooleanProperty(required=True)
  time = db.DateTimeProperty(auto_now_add=True)
  is_cl = db.BooleanProperty(required=True)
  
class Checklist(db.Model):
  """
  Checklist Model
  """
  # References Properties.
  # Original checklist. Exist if this checklist is a subscriber of another list.
  source = db.SelfReferenceProperty()
  
  # Basic info about cecklist.
  title = db.StringProperty(required=True)
  description = db.TextProperty()
  user = db.UserProperty(required=True)

  # Weighted progress of items. Out of 100.
  progress = db.RatingProperty()
  
  # Permission.
  public = db.BooleanProperty(required=True)
  
  deleted = db.BooleanProperty(required=True)
  
class Item(db.Model):
  # Basic info
  title = db.StringProperty(required=True)
  description = db.TextProperty()
  progress = db.RatingProperty()
  progress_description = db.TextProperty()
  difficulty = db.RatingProperty()
  
  # References.
  original = db.SelfReferenceProperty()
  checklist = db.ReferenceProperty(Checklist, required=True)
  
  deleted = db.BooleanProperty(required=True)
