import helpers
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item, Subscription, SubscribedItem

class CreateChecklist(webapp2.RequestHandler):
  def post(self):
    checklist = Checklist(
          title=self.request.get('title'),
          public=True,
          user=users.get_current_user(),
          deleted=False,
          )
    
    checklist.put()
    helpers.createResponse(self, 'new_cl.html', {'cl':checklist})
      
class CreateItem(webapp2.RequestHandler):
  def post(self):
    checklist = Checklist.get(Key(self.request.get('cl_key')))
    if not helpers.checkPermissionAndRespond(self, cl=checklist): return
    
    item = Item(
        title=self.request.get('title'),
        checklist=checklist,
        deleted=False)

    item.put()
    helpers.createResponse(self, 'new_item.html', {'item': item})

class Subscribe(webapp2.RequestHandler):
  def post(self):
    cl = Checklist.get(Key.from_path('Checklist', long(self.request.get('cl_id'))))
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False):
      return
    
    user = users.get_current_user()
    
    for sub in Subscription.all().filter("user ==", user).filter("deleted ==", False):
      if sub.source.key() == cl.key():
        helpers.createResponse(self, 'message_already_subscribed.html', 
          {'old_checklist': cl})
        
    sub = Subscription(
        user=user,
        source=cl,
        deleted=False,                       
                       )        

    sub.put()

    for item in cl.item_set:
      subItem = SubscribedItem(
          subscription=sub,
          original=item,
          finished=False,
          deleted=False,                               
                               )
      subItem.put()
    
    helpers.createResponse(self, 'message_subscribed.html')
    
app = webapp2.WSGIApplication([
    ('/create/checklist', CreateChecklist),
    ('/create/item', CreateItem),
    ('/subscribe', Subscribe),
    ])
