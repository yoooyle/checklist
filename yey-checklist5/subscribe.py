import helpers
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Subscription, SubscribedItem

class Subscribe(webapp2.RequestHandler):
  def post(self):
    cl = Checklist.get(Key.from_path('Checklist', long(self.request.get('cl_id'))))
    subscribe = self.request.get('subscribe')
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False):
      return
    
    user = users.get_current_user()
    if subscribe == 'false':
      for sub in Subscription.all().filter("user ==", user).filter("deleted ==", False):
        if sub.source.key() == cl.key():
          for subItem in sub.subscribeditem_set:
            subItem.delete()
          sub.delete()
      cl.subscribers = cl.subscribers - 1
      self.response.write("unsubscribed")
    else:
      sub = Subscription(
          user=user,
          source=cl,
          deleted=False,                       
                       )        

      sub.put()

      for item in cl.item_set.filter("deleted ==", False):
        subItem = SubscribedItem(
            subscription=sub,
            original=item,
            finished=False,
            deleted=False,                               
                               )
        subItem.put()

      cl.subscribers = cl.subscribers + 1
      self.response.write("subscribed")
      
    cl.put()
    
  def get(self, **args):
    cl = Checklist.get(Key.from_path("Checklist", long(args['id'])))
    
    if not cl or cl.deleted: 
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False): return
    
    item_q = cl.item_set.filter("deleted ==", False).order("creation_time")
    cursor = self.request.get('cursor')
    if cursor:
      item_q = item_q.with_cursor(cursor)
    items = item_q.fetch(20)

    user = users.get_current_user()
    subscribed = False
    for sub in Subscription.all().filter("user ==", user).filter("deleted ==", False):
      if sub.source.key() == cl.key():
        subscribed = True
        break
   
    helpers.createResponse(self, 'dashboard_subscribe.html', 
        {'items': items,
        'cl': cl,
        'cursor_item': item_q.cursor(),
        'subscribed': subscribed,
        },
                           )   
    
app = webapp2.WSGIApplication([
    ('/subscribe', Subscribe),
    webapp2.Route(r'/subscribe/<id:[^/]+>', Subscribe),
    ])       