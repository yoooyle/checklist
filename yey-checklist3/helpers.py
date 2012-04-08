import jinja2
import os
from google.appengine.api import taskqueue, users

jinja_environment = jinja2.Environment(
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
template_root = "templates/"

def pushNotification(item_cl, message, user, to, is_cl):
  '''
  @param item_cl: item or checklist this notification is about.
  @param message: the message associated with notification.
  @param user: the user who sends.
  @param to: the user who receives.
  @param is_cl: True if item_cl is a Checklist.
  '''
  taskqueue.add(url="/notifications/add", params={
     'key': item_cl.key(),
     'message': user.nickname() + ' ' + message + ' ' + item_cl.title,
     'email': to.email(),
     'is_cl': is_cl})
  
def updateProgress(cl, user):
  '''
    @summary: 
      Update a checklist's progress when the progress of its items are changed.
    @param cl: the checklist whose progress needs to be re-calculated.
    @param user: the user who requested this update. This is used to check for
    permission.
  '''
  taskqueue.add(url="/tasks/updateprogress", params={
      'cl': cl.key(),
      'email': user.email()})
  
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
