import helpers
import logging
import webapp2  

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item, Subscription, SubscribedItem

class ListDashboard(webapp2.RequestHandler):
  '''
  List Subscriptions and My lists.
  '''
  def get(self):
    user = users.get_current_user()
    checklist_q = Checklist.all().filter("user ==", user).filter("deleted ==", False).order("title");
    cursor = self.request.get('cursor_cl')
    if cursor:
      checklist_q = checklist_q.with_cursor(cursor)
    checklists = checklist_q.fetch(20)
    
    cursor_cl = checklist_q.cursor()
    checklist_q = checklist_q.with_cursor(cursor_cl)

    subs_q = Subscription.all().filter("user ==", user).filter("deleted ==", False);
    cursor = self.request.get('cursor_sub')
    if cursor:
      subs_q = subs_q.with_cursor(cursor)
    subs = subs_q.fetch(20)
    
    cursor_sub = subs_q.cursor()
    subs_q = subs_q.with_cursor(cursor_sub)
    
    helpers.createResponse(self, 'dashboard_cls.html',
        {'checklists': checklists,
         'cursor_cl': cursor_cl,
         'subs': subs,
         'cursor_sub': cursor_sub,
         'more_subs': subs_q.count(1) == 1,
         'more_cls': checklist_q.count(1) == 1,
         })
    
class ListItemsAndCl(webapp2.RequestHandler):
  '''
  Main page for a CL.
  '''
  def get(self, **args):
    cl = Checklist.get(Key.from_path("Checklist", long(args['id'])))
    
    if not cl or cl.deleted: 
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False): return
    
    item_q = cl.item_set.filter("deleted ==", False).order("creation_time")
    cursor = self.request.get('cursor_item')
    if cursor:
      item_q = item_q.with_cursor(cursor)
    items = item_q.fetch(20)
    
    subs = []
    for sub in cl.subscription_set:
        subs.append(sub)
    
    cursor_item = item_q.cursor()
    item_q = item_q.with_cursor(cursor_item)
    helpers.createResponse(self, 'dashboard_items.html', 
        {'items': items,
        'cl': cl,
        'cursor_item': cursor_item,
        'more_items': item_q.count(1) == 1,
        'subs': subs,
        })
    
class ListSubItemsDashboard(webapp2.RequestHandler):
  '''
  Main page for a subscription.
  '''
  def get(self, **args):
    sub = Subscription.get(Key.from_path("Subscription", long(args['id'])))
    
    if not sub or sub.deleted: 
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, sub=sub, edit=False): return
    
    subItem_q = sub.subscribeditem_set.order("original")
    cursor = self.request.get('cursor_subItem')
    if cursor:
      subItem_q = subItem_q.with_cursor(cursor)
    subItems = subItem_q.fetch(20)
    
    cursor_subItem = subItem_q.cursor()
    subItem_q = subItem_q.with_cursor(cursor_subItem)

    helpers.createResponse(self, 'dashboard_subItems.html', 
        {'subItems': subItems,
        'sub': sub,
        'cursor_subItem': cursor_subItem,
        'more_subs': subItem_q.count(1) == 1,
        })    

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', ListDashboard),
    webapp2.Route(r'/sub/<id:[^/]+>', ListSubItemsDashboard),
    webapp2.Route(r'/l/<id:[^/]+>', ListItemsAndCl),
#    webapp2.Route(r'/.*', WrongUrl),
                                   ])
    