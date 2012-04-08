import jinja2
import os
import webapp2

from google.appengine.api import taskqueue, users
from google.appengine.ext.db import Key
from models import Checklist, Item, SubscribedItem

jinja_environment = jinja2.Environment(
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
template_root = "templates/"
  
class updateProgress(webapp2.RequestHandler):
  def post(self):
      cl = Checklist.get(Key(self.request.get("cl_key")))
      for sub in cl.subscription_set:
        total, finished = 0, 0
        for subItem in sub.subscribeditem_set:
          total += 1
          if subItem.finished:
            finished += 1
        if sub.progress != finished*100/total:
          sub.progress = finished*100/total
          sub.put()
    
# This is a cron job. misnomer          
class Sweep(webapp2.RequestHandler):
  def get(self):
    for item in Item.all().filter("deleted ==", True):
      if item.item_set.count(1) == 0:
        item.delete()
    
    for cl in Checklist.all().filter("deleted ==", True):
      if cl.checklist_set.count(1) == 0:
        cl.delete()          
        
class updateSubscription(webapp2.RequestHandler):
  '''
  Add new item to subscriptions once item creation.
  '''
  def post(self):
    item = Item.get(Key(self.request.get('key')))
    for sub in item.checklist.subscription_set:
      new_sub = SubscribedItem(
          subscription=sub,
          original=item,
          finished=False,
          deleted=False,                               
                               )
      new_sub.put()

class removeSubscribedItem(webapp2.RequestHandler):
  '''
  Remove subscribedItem upon item removal.
  '''
  def post(self):
    item = Item.get(Key(self.request.get('key')))
    for subItem in item.subscribeditem_set:
      subItem.delete()
    
app = webapp2.WSGIApplication([
    ('/taskqueue/updateprogress', updateProgress),
    ('/taskqueue/delete', Sweep),             
    ('/taskqueue/updatesubscription', updateSubscription),
    ('/taskqueue/removesubscribeditem', removeSubscribedItem),                
                               ])     
def checkPermission(user=None, cl=None, item=None, sub=None, edit=True):
  '''
  @summary: 
    Check if the user has permission to perform certain action.
  @param edit: edit permission or view permission.
  '''
  if not user:
    user = users.get_current_user()
    
  if cl:
    if cl.user != user:
      if edit:
        return False
      else:
        return cl.public
  elif item:
    if item.checklist.user != user:
      if edit:
        return False
      else:
        return item.checklist.public
  elif sub:
    if sub.user != user:
      if edit:
        return False
              
  return True
  
def checkPermissionAndRespond(request, user=None, cl=None, item=None, sub=None, edit=True):
  '''
  @summary: Check permission. If permission is denied, respond with a default message.
  '''
  if not checkPermission(user, cl, item, sub, edit):
    template = jinja_environment.get_template('templates/message_permission_denied.html')
    request.response.out.write(template.render({
        'user': users.get_current_user(),
        'logout_url': users.create_logout_url('/'),
        }))
    return False
  return True
        
def basicTemplateValues(extras):
  '''
  @summary: Add common template values to values.
  '''
  base = { 'user': users.get_current_user(), 'logout_url': users.create_logout_url('/')}
  base.update(extras)
  return base
  
def createResponse(requestHandler, template, extras={}):
  '''
  @summary: Take care of jinja2 template fetch and render.
  @param requestHandler: usually the "self" parameter in a requestHandler
  @param template: name of template under the template root directory.
  @param extras: extra template values except basic ones.
  '''
  template = jinja_environment.get_template(template_root + template)
  requestHandler.response.out.write(template.render(basicTemplateValues(extras)))
