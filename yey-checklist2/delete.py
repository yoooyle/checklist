import helpers
import logging
import webapp2

from google.appengine.ext.db import Key
from models import Checklist, Item

class DeleteChecklist(webapp2.RequestHandler):
  def post(self):
    cl = Checklist.get(Key.from_path('Checklist', long(self.request.get('cl_id'))))
    if not helpers.checkPermissionAndRespond(self, cl=cl): return
      
    for item in cl.item_set:
      item.deleted = True
      item.put()
    cl.deleted = True
    cl.put()
      
    for copy in cl.checklist_set:
      helpers.pushNotification(cl, "deleted the checklist", cl.user, copy.user , True)
        
    helpers.createResponse(self, 'message_deleted.html')

class DeleteItem(webapp2.RequestHandler):
  def post(self):
    item = Item.get(Key.from_path('Item', long(self.request.get('item_id'))))
    if not helpers.checkPermissionAndRespond(self, item=item): return

    item.deleted = True
    item.put()
    for copy in item.item_set:
      helpers.pushNotification(item, "deleted the task", item.checklist.user, copy.checklist.user , False)

    helpers.createResponse(self, 'message_deleted.html')
        
class Sweep(webapp2.RequestHandler):
  def get(self):
    for item in Item.all().filter("deleted ==", True):
      if item.item_set.count(1) == 0:
        item.delete()
    
    for cl in Checklist.all().filter("deleted ==", True):
      if cl.checklist_set.count(1) == 0:
        cl.delete()
                
app = webapp2.WSGIApplication([
    ('/delete/checklist', DeleteChecklist),
    ('/delete/item', DeleteItem),  
    ('/tasks/delete', Sweep),                             
                               ])

