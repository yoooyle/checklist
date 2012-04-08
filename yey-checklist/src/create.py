import logging
import webapp2  

from datetime import datetime
from google.appengine.api import users
from models import Checklist, ListItem

logging.basicConfig(filename='cl.log', level=logging.DEBUG, filemode='w')
    
class CreateChecklist(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    
    if user:
      checklist = Checklist(
          title=self.request.get('title'), 
          user=user)
      checklist.put()
    self.redirect('/')
    
class CreateListItem(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      checklist = Checklist.get(self.request.get('checklist_key'))
      listitem = ListItem(
          title=self.request.get('title'),
          assigner=user,
          assignees=[user],
          priority=int(self.request.get('priority')),
          finished=bool(self.request.get('finished')),
          checklist=checklist)
      
      if self.request.get('link') != '':
        listitem.link = self.request.get('link')
      if self.request.get('deadline') != '':
        # TODO: replace this with deadline
        listitem.deadline=datetime.now()
      if self.request.get('details') != '':
        listitem.details=self.request.get('detail')
         
      listitem.put()
    self.redirect('/')
    
app = webapp2.WSGIApplication([
    ('/create/checklist', CreateChecklist),
    ('/create/listitem', CreateListItem)
    ],
                              debug=True)

      
    