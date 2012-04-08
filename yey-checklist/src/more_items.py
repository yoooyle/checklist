import logging
import jinja2
import os
import webapp2  

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import db
from models import Checklist, ListItem

jinja_environment = jinja2.Environment(
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
  
class MoreItems(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    
    if user:
      query = self.request.query.split('&')
      cl_key, cursor = query[0], query[1]
      cl = Checklist.get(db.Key(cl_key))
      query = cl.listitem_set.with_cursor(cursor)
      items = query.fetch(10)
      
#    self.response.out.write("<tr></tr>")
    template = jinja_environment.get_template('templates/more_items.html')
    template_values = {
        'items': items,
                       }
    self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/ajax/moreitems', MoreItems),
                               ])   