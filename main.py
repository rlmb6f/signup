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
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
    <style type="text/css">
        .error {
            color: black;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">SignUp</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""





username_form = """
    <form action="/" method="post">
        <label style="font-size: 3em">
            Signup
        </label>
    <br>
        <label>
            Username
            <input type="text" name="username" value = "%(username)s"/>%(username_error)s
        </label>
    <br>
        <label>
            Password
            <input type="password" name="password" value=""/>%(password_error)s

        </label>
    <br>
        <label>
            Verify Password
            <input type="password" name="verify" value=""/>%(verify_error)s

        </label>
    <br>
        <label>
            Email (optional)
            <input type="text" name="email" value='%(email)s'/>%(email_error)s
        </label>
        <br>
        <input type="submit" value="submit"/>
    </form>
    """

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASSWD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWD_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)



class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.signup.com/
    """
    parameters = dict()
    def write_form(self, username_error="", username= "", email= "", password_error= "", verify_error= "", email_error= ""):
        self.response.write(username_form % {'username_error':username_error, 'username': username, 'email': email,
                                            'password_error':password_error, 'verify_error':verify_error, 'email_error':email_error})


    def get(self):
        self.write_form()


    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""



        if not valid_username(username):
            self.write_form ("That's not a valid username", username, email, password_error, verify_error, email_error)


        elif not valid_password(password):
            self.write_form (username_error, username, email, "That's not a valid password", verify_error, email_error)

        elif password != verify:
            self.write_form (username_error, username, email, password_error, "Your passwords do not match", email_error)

        elif not valid_email(email):
            self.write_form (username_error, username, email, password_error, verify_error, "That's not a valid email")

        else:
            response = "Welcome, " + username +"!"
            self.response.write(response)


app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
