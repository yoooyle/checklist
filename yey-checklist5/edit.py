import helpers
import logging
import webapp2

from google.appengine.api import users, taskqueue
from google.appengine.ext.db import Key
from models import Checklist, Item, Subscription, SubscribedItem

class EditChecklistDashboard(webapp2.RequestHandler):
  def post(self):
    value = self.request.get("value")
    key, tmp, field = self.request.get("id").rpartition("_")
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
    key, tmp, field = self.request.get("id").rpartition("_")
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
    
class EditSubItemDashboard(webapp2.RequestHandler):
  def post(self):
    subItem = SubscribedItem.get(Key(self.request.get('key')))
    subItem.finished = (self.request.get('finished') == 'finished')
    subItem.put()
    
    total, finished = 0, 0
    sub = subItem.subscription
    for subItem in sub.subscribeditem_set:
      total += 1
      if subItem.finished:
        finished += 1
    sub.progress = finished*100/total
    sub.put()
      
app = webapp2.WSGIApplication([
    ('/edit/checklistdashboard', EditChecklistDashboard),
    ('/edit/itemdashboard', EditItemDashboard),
    ('/edit/subitemdashboard', EditSubItemDashboard),
    ])
