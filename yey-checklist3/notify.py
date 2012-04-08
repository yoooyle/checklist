import helpers
import logging
import webapp2

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext.db import Key, Model, ReferencePropertyResolveError
from models import Checklist, Item, Notification

class Notify(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    notifications_q = Notification.all().filter("user == ", user)\
        .filter("read ==", False).order("-time")
    notifications = []
    for n in notifications_q:
      try:
        n.item_cl.title
      except ReferencePropertyResolveError:
        n.delete()
      else:
        notifications.append(n)
      
    helpers.createResponse(self, 'notifications.html', {'notifications': notifications})

class QueueNotification(webapp2.RequestHandler):
  def post(self):
    notification = Notification(
        item_cl = Model.get(Key(self.request.get('key'))),
        message = self.request.get('message'),
        user = users.User(self.request.get('email')),
        is_cl = ("True" == self.request.get('is_cl')),
        time = datetime.now(),
        read = False)
    notification.put()
    
app = webapp2.WSGIApplication([
    ('/notifications', Notify),
    ('/notifications/add', QueueNotification),                               
    ])
