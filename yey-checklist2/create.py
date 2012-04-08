import helpers
import logging
import webapp2

from google.appengine.api import users
from google.appengine.ext.db import Key
from models import Checklist, Item

class CreateChecklist(webapp2.RequestHandler):
  def get(self):
    helpers.createResponse(self, 'create_cl.html')

  def post(self):
    checklist = Checklist(
          title=self.request.get('title'),
          public=bool(self.request.get('public')),
          description=self.request.get('description'),
          user=users.get_current_user(),
          deleted=False,
          )
    
    checklist.put()
    self.redirect('/')
    
class CreateItem(webapp2.RequestHandler):
  def addable(self, cl):
    '''
    @summary: New item can only be added to checklist created by a user, not a subscribed one.
    '''
    return cl.source == None
  
  def get(self):
    checklist = Checklist.get(Key.from_path('Checklist', long(self.request.get('cl_id'))))
    if not helpers.checkPermissionAndRespond(self, cl=checklist): return
    if not self.addable(checklist):
      helpers.createResponse(self, 'message_can_not_create_item.html')
      return 
    helpers.createResponse(self, 'create_item.html', {'checklist': checklist})
    
  def post(self):
    checklist = Checklist.get(self.request.get('checklist'))
    if not helpers.checkPermissionAndRespond(self, cl=checklist): return
    if not self.addable(checklist):
      helpers.createResponse(self, 'message_can_not_create_item.html')
      return
    
    item = Item(
        title=self.request.get('title'),
        difficulty=int(self.request.get('difficulty')),
        progress=0,
        checklist=checklist,
        deleted=False)

    if self.request.get('description') != '':
        item.description=self.request.get('description')
         
    item.put()
    self.redirect("/cl/" + str(checklist.key().id()))

class Subscribe(webapp2.RequestHandler):
  def post(self):
    cl = Checklist.get(Key.from_path('Checklist', long(self.request.get('cl_id'))))
    if not helpers.checkPermissionAndRespond(self, cl=cl, edit=False):
      return
    
    user = users.get_current_user()
    for checklist in Checklist.all().filter("user ==", user):
      if checklist.source.key() == cl.key():
        helpers.createResponse(self, 'message_already_subscribed.html', 
          {'old_checklist': cl, 'my_checklist': checklist})
        return
        
    new_cl = Checklist(
        title = cl.title,
        description = cl.description,
        user = user,
        progress = cl.progress,
        public = cl.public,
        source = cl,
        deleted = cl.deleted,
                         )
    new_cl.put()

    for item in cl.item_set:
      new_item = Item(
          title = item.title,
          description = item.description,
          progress = item.progress,
          progress_description = item.progress_description,
          difficulty = item.difficulty,
          original = item,
          checklist = new_cl,
          deleted = item.deleted,
                      )
      new_item.put()
    
    helpers.pushNotification(cl, "subscribed to your Checklist", user, cl.user, True)
    
    helpers.createResponse(self, 'message_subscribed.html')
    
app = webapp2.WSGIApplication([
    ('/create/checklist', CreateChecklist),
    ('/create/item', CreateItem),
    ('/subscribe', Subscribe),
    ])
