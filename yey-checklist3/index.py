import helpers
import logging
import webapp2  

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item, Subscription, SubscribedItem

class ListDashboard(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    checklist_q = Checklist.all().filter("user ==", user).filter("deleted ==", False);
    cursor = self.request.get('cursor_cl')
    if cursor:
      checklist_q = checklist_q.with_cursor(cursor)
    checklists = checklist_q.fetch(10)
    
    checklist_q = checklist_q.with_cursor(checklist_q.cursor())
    
    subs_by_cl = []
    for cl in checklists:
      subs = []
      for sub in cl.subscription_set:
        subs.append(sub)
      subs_by_cl.append(subs)
        
    subs_q = Subscription.all().filter("user ==", user).filter("deleted ==", False);
    cursor = self.request.get('cursor_sub')
    if cursor:
      subs_q = subs_q.with_cursor(cursor)
    subs = subs_q.fetch(10)
    
    subs_q = subs_q.with_cursor(subs_q.cursor())
    
    helpers.createResponse(self, 'dashboard_cls.html',
        {'checklists': checklists,
         'cursor_cl': checklist_q.cursor(),
         'subs_by_cl': subs_by_cl,
         'subs': subs,
         'cursor_sub': subs_q.cursor(),
         'more_subs': subs_q.count(1) == 1,
         'more_cls': checklist_q.count(1) == 1,
         })
    
class ListItemsDashboard(webapp2.RequestHandler):
  def get(self, **args):
    cl = Checklist.get(Key.from_path("Checklist", long(args['id'])))
    
    if not cl or cl.deleted: 
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False): return
    
    item_q = cl.item_set.filter("deleted ==", False).order("title")
    cursor = self.request.get('cursor_item')
    if cursor:
      item_q = item_q.with_cursor(cursor)
    items = item_q.fetch(10)
    
    item_q = item_q.with_cursor(item_q.cursor())
    
    helpers.createResponse(self, 'dashboard_items.html', 
        {'items': items,
        'checklist': cl,
        'cursor_item': item_q.cursor(),
        'more_items': item_q.count(1) == 1,
        })
    
class ListSubItemsDashboard(webapp2.RequestHandler):
  def get(self, **args):
    sub = Subscription.get(Key.from_path("Subscription", long(args['id'])))
    
    if not sub or sub.deleted: 
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, sub=sub, edit=False): return
    
    subItem_q = sub.subscribeditem_set.filter("deleted ==", False).order("original")
    cursor = self.request.get('cursor_subItem')
    if cursor:
      subItem_q = subItem_q.with_cursor(cursor)
    subItems = subItem_q.fetch(10)

    helpers.createResponse(self, 'dashboard_subItems.html', 
        {'subItems': subItems,
        'sub': sub,
        'cursor_subItem': subItem_q.cursor()})    
    
class ListItems(webapp2.RequestHandler):
  def get(self, **args):
    cl = Checklist.get(Key.from_path("Checklist", long(args['id'])))
    
    if not cl or cl.deleted: 
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False): return
    
    item_q = cl.item_set.filter("deleted ==", False).order("title")
    cursor = self.request.get('cursor')
    if cursor:
      item_q = item_q.with_cursor(cursor)
    items = item_q.fetch(7)

    helpers.createResponse(self, 'list_items.html', 
        {'items': items,
        'checklist': cl,
        'item_cursor': item_q.cursor(),
        'subscribe': users.get_current_user() != cl.user },
                           )    
      
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', ListDashboard),
    webapp2.Route(r'/cl/subscribe/<id:[^/]+>', ListItems),
    webapp2.Route(r'/cl/<id:[^/]+>', ListItemsDashboard), 
    webapp2.Route(r'/sub/<id:[^/]+>', ListSubItemsDashboard),  
                               ])
    