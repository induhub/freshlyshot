#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
from google.appengine.ext import ndb
import hashlib
jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
from google.appengine.api import mail

class subscription(ndb.Model):
    email_id = ndb.StringProperty(required=True)
    activation_link = ndb.StringProperty(required=True)
    activated=ndb.BooleanProperty(required=True)
    account_created=ndb.DateTimeProperty(auto_now_add=True)
    account_activated_stamp=ndb.DateTimeProperty(auto_now_add=False)
    ip_address=ndb.StringProperty(required=True)


class VerificationHandler(webapp2.RequestHandler):
    def get(self, activation_link):
        self.response.write('verified!')
        '''
        if activation link in database:'''
        subscriber_exists=subscription.query(subscription.activation_link==activation_link).get()
        if subscriber_exists!=None:
            subscriber_exists.activated=True
            subscriber_exists.put()
        else:
            self.response.write('bad link!')
    
            
    
class SubscribeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('form.html')
        context = {}
        html = template.render(context)
        self.response.write(html)

    def post(self):
         x = self.request.get('email_id')
         subscriber_exists=subscription.query(subscription.email_id==x).get()
         if subscriber_exists==None:         
             linkxyz=hashlib.sha256(x+'alex').hexdigest()
             activated=False
             ip=self.request.remote_addr
             subscribe=subscription(email_id=x,activation_link=linkxyz,activated=activated,ip_address=ip)
             subscribe.put()
             template = jinja_environment.get_template('verification.html')
             context = {'verify':linkxyz}
             mail_html = template.render(context)
             #self.response.write(html)
             # mail bhejo
             mail.send_mail(sender="indusnow28@gmail.com",
              to=x,
              subject="Your account has been approved",body="no html version",    
              html=mail_html)
              
             self.response.write('new email submitted!!!')
         else:
             self.response.write('email exists!!!')
             
            
         
app = webapp2.WSGIApplication([
    ('/',SubscribeHandler),('/verify/(?P<activation_link>.*)', VerificationHandler)
], debug=True)







    
    


       

        
