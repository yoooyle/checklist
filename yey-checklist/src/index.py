import logging
import jinja2
import os
import webapp2  

from google.appengine.api import users
from models import Checklist, ListItem



jinja_environment = jinja2.Environment(
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
  
class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    checklists, user_url, cl_cursor, item_cursors, items = None, None, None, None, None
    
    if not user:
      user_url = users.create_login_url(self.request.uri)
    else:
      user_url = users.create_logout_url("/")
      q = Checklist.all().filter("user =", user).order("title")
      checklists = q.fetch(5)
      item_queries = [ cl.listitem_set for cl in checklists ]
      items = [ q.fetch(10) for q in item_queries ]
      cl_cursor = q.cursor()
      item_cursors = [ q.cursor() for q in item_queries ]
     
    template = jinja_environment.get_template('templates/index.html')
    template_values = {
        'checklists': checklists,
        'cl_cursor': cl_cursor,
        'items': items,
        'item_cursors': item_cursors,
        'user': user,
        'user_url': user_url
                       }
    self.response.out.write(template.render(template_values))
    
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ],
                              debug=True)
