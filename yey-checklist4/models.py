from google.appengine.ext import db
  
class Checklist(db.Model):
  """
  Checklist Model
  """
  title = db.StringProperty(required=True)
  description = db.TextProperty()
  user = db.UserProperty(required=True)
  public = db.BooleanProperty(required=True)
  deleted = db.BooleanProperty(required=True)
  creation_time = db.DateTimeProperty(auto_now_add=True)
  edit_time = db.DateTimeProperty(auto_now=True)

class Subscription(db.Model):
  user = db.UserProperty(required=True)
  progress = db.RatingProperty()
  source = db.ReferenceProperty(Checklist, required=True)
  deleted = db.BooleanProperty(required=True)
    
class Item(db.Model):
  # Basic info
  title = db.StringProperty(required=True)
  description = db.TextProperty()
  difficulty = db.RatingProperty()
  checklist = db.ReferenceProperty(Checklist, required=True)
  deleted = db.BooleanProperty(required=True)
  creation_time = db.DateTimeProperty(auto_now_add=True)
  edit_time = db.DateTimeProperty(auto_now=True)

class SubscribedItem(db.Model):
  subscription = db.ReferenceProperty(Subscription, required=True)
  original = db.ReferenceProperty(Item, required=True)
  finished = db.BooleanProperty(required=True)
  deleted = db.BooleanProperty(required=True)

