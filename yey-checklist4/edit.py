import helpers
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item

class EditChecklistDashboard(webapp2.RequestHandler):
  def post(self):
    value = self.request.get("value")
    key, field = self.request.get("id").split("_")
    checklist = Checklist.get(Key(key))
    if helpers.checkPermissionAndRespond(self, cl=checklist):
      if field == 'title':
        checklist.title = value
      elif field == 'public':
        checklist.public = value.lower() not in ['no', 'false']
      elif field == 'description':
        checklist.description = value

      checklist.put()
      self.response.write(value)
    
class EditItemDashboard(webapp2.RequestHandler):    
  def post(self):
    value = self.request.get("value")
    key, field = self.request.get("id").split("_")
    item = Item.get(Key(key))

    if helpers.checkPermissionAndRespond(self, item=item):
      if field == "title":
        item.title = value
      elif field == "difficulty":
        item.difficulty = int(value)
      elif field == "description":
        item.description = value
      
      item.put()
      self.response.write(value)
    
class UpdateProgress(webapp2.RequestHandler):
  def post(self):
    cl = Checklist.get(Key(self.request.get('cl')))
    if helpers.checkPermission(users.User(self.request.get('email')), cl=cl):
      difficulty_sum, weighted_progress = 0, 0
      for item in cl.item_set:
        difficulty_sum += item.difficulty
        weighted_progress += item.difficulty*item.progress
      cl.progress = weighted_progress/difficulty_sum
      cl.put()
      
app = webapp2.WSGIApplication([
    ('/edit/checklistdashboard', EditChecklistDashboard),
    ('/edit/itemdashboard', EditItemDashboard),
    ('/tasks/updateprogress', UpdateProgress)
    ])
