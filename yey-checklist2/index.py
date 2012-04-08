import helpers
import logging
import webapp2  

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item

class ListChecklists(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    checklist_q = Checklist.all().filter("user =", user).filter("deleted ==", False).order("title")
    cursor = self.request.get('cursor')
    if cursor:
      checklist_q = checklist_q.with_cursor(cursor)
    checklists = checklist_q.fetch(7)
    
    helpers.createResponse(self, 'list_cls.html', 
        {'checklists': checklists,
        'checklists_cursor': checklist_q.cursor()})

    
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
        'item_cursor': item_q.cursor()})
    
class ListItem(webapp2.RequestHandler):
  def get(self, **args):
    item = Item.get(Key.from_path("Item", long(args['id_item'])))
    
    if not item or item.deleted:
      helpers.createResponse(self, 'message_not_exist.html')
      return
    
    if not helpers.checkPermissionAndRespond(self, item=item, edit=False): return
    
    helpers.createResponse(self, 'list_item.html', {'item': item})
      
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', ListChecklists),
    webapp2.Route(r'/cl/<id:[^/]+>', ListItems),
    webapp2.Route(r'/cl/<id_cl:[^/]+>/<id_item:[^/]+>', ListItem),    
                               ])
    