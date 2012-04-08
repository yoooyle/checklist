import helpers
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item

class EditChecklist(webapp2.RequestHandler):
  def get(self):
    checklist = Checklist.get(Key.from_path("Checklist", long(self.request.get('cl_id'))));
    if helpers.checkPermissionAndRespond(self, cl=checklist):
      helpers.createResponse(self, 'edit_cl.html', {'checklist_to_change': checklist})
    
  def post(self):
    checklist = Checklist.get(Key(self.request.get("key")))
    if helpers.checkPermissionAndRespond(self, cl=checklist):
      checklist.title = self.request.get('title')
      checklist.public = bool(self.request.get('public'))
      checklist.description = self.request.get('description')
      checklist.put()
    
      for copy in checklist.checklist_set:
        helpers.pushNotification(checklist, "edited the checklist", checklist.user, copy.user , True)
          
      self.redirect('/cl/' + str(checklist.key().id()))
    
class EditItem(webapp2.RequestHandler):
  def get(self):
    item = Item.get(Key.from_path("Item", long(self.request.get("item_id"))))
    if helpers.checkPermissionAndRespond(self, item=item):
      helpers.createResponse(self, 'edit_item.html', {'item': item})
    
  def post(self):
    item = Item.get(Key.from_path("Item", long(self.request.get("item_id"))))
    if helpers.checkPermissionAndRespond(self, item=item):
      item.title = self.request.get("title")
      item.description = self.request.get("description")
      item.difficulty = int(self.request.get("difficulty"))
    
      if item.original:
        if self.request.get('progress') != '' and \
          item.progress != int(self.request.get('progress')):
          item.progress = int(self.request.get('progress'))
          helpers.updateProgress(item.checklist, item.checklist.user)
          helpers.pushNotification(
              item, 
              "updated progress to " + str(item.progress) + " for item", 
              item.checklist.user, item.original.checklist.user, False)
        item.progress_description = self.request.get('progress_description')
      
      item.put()
    
      for copy in item.item_set:
        helpers.pushNotification(item, "edited the task", item.checklist.user, copy.checklist.user , False)

      self.redirect("/cl/" + str(item.checklist.key().id()) + "/" + str(item.key().id()))
    
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
    ('/edit/checklist', EditChecklist),
    ('/edit/item', EditItem),
    ('/tasks/updateprogress', UpdateProgress)
    ])
