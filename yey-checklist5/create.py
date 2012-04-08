import helpers
import logging
import webapp2

from google.appengine.api import users, taskqueue
from google.appengine.ext.db import Key
from models import Checklist, Item, SubscribedItem

class CreateChecklist(webapp2.RequestHandler):
  def post(self):
    checklist = Checklist(
          title=self.request.get('title'),
          public=True,
          user=users.get_current_user(),
          deleted=False,
          subscribers=0,
          )
    
    checklist.put()
    self.response.write("/l/" + str(checklist.key().id()))
      
class CreateItem(webapp2.RequestHandler):
  def post(self):
    checklist = Checklist.get(Key(self.request.get('cl_key')))
    if not helpers.checkPermissionAndRespond(self, cl=checklist): return
    
    item = Item(
        title=self.request.get('title'),
        checklist=checklist,
        deleted=False)

    item.put()
    
    taskqueue.add(url="/taskqueue/updatesubscription", params={'key': item.key()})
    taskqueue.add(url="/taskqueue/updateprogress", params={'cl_key': item.checklist.key()})
    helpers.createResponse(self, 'new_item.html', {'item': item})

app = webapp2.WSGIApplication([
    ('/create/checklist', CreateChecklist),
    ('/create/item', CreateItem),
    ])
