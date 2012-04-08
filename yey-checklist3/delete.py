import helpers
import logging
import webapp2

from google.appengine.ext.db import Key
from models import Checklist, Item
    
class DeleteChecklistDashboard(webapp2.RequestHandler):
  def post(self):
    cl = Checklist.get(Key((self.request.get('key'))))
    if not helpers.checkPermissionAndRespond(self, cl=cl): return
      
    for item in cl.item_set:
      item.deleted = True
      item.put()
    cl.deleted = True
    cl.put()
    self.response.write('ok')
    
class DeleteItemDashboard(webapp2.RequestHandler):
  def post(self):
    item = Item.get(Key(self.request.get("key")))
    if not helpers.checkPermissionAndRespond(self, item=item): return

    item.deleted = True
    item.put()
    self.response.write("ok")
        
class Sweep(webapp2.RequestHandler):
  def get(self):
    for item in Item.all().filter("deleted ==", True):
      if item.item_set.count(1) == 0:
        item.delete()
    
    for cl in Checklist.all().filter("deleted ==", True):
      if cl.checklist_set.count(1) == 0:
        cl.delete()
                
app = webapp2.WSGIApplication([
    ('/delete/checklistdashboard', DeleteChecklistDashboard),
    ('/delete/itemdashboard', DeleteItemDashboard),  
    ('/tasks/delete', Sweep),                             
                               ])

