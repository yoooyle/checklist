import helpers
import logging
import webapp2

from google.appengine.api import taskqueue
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
    
    for subItem in item.subscribeditem_set:
      subItem.delete()
    
    taskqueue.add(url="/taskqueue/removesubscribeditem", params={'key': item.key()})
    taskqueue.add(url="/taskqueue/updateprogress", params={'cl_key': item.checklist.key()})
    self.response.write("ok")
        
app = webapp2.WSGIApplication([
    ('/delete/checklistdashboard', DeleteChecklistDashboard),
    ('/delete/itemdashboard', DeleteItemDashboard),  
                                   ])

