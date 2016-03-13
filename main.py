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

def valid_day(day):
	if day.isdigit():
		if int(day) >= 1 and int(day) <= 31:
			return day
		else:
			return None

months = ["january", "fabruary", "march", "april", "may", "june", "july", "august", "september", "octuber", "november", "december"]

def valid_month(month):
	for i in months:
		if month.lower() == i.lower():
			return month.capitalize()
	return None

def valid_year(year):
	if year and year.isdigit():
		year = int(year)
		if year >= 1900 and year <= 2020:
			return year

import cgi
def escape_html(s):
	return cgi.escape(s, quote = True)

def rot(s):
	s = s.lower()
	arr = list(s)
	newStr = ""
	for each in arr:
		each = ord(each)
		if each >= ord('a') and each <= ord('z'):
			each = each + 13
			if each >= ord('z'):
				each = each - 26
			each = chr(each)
			newStr = newStr + each
		else:
			newStr = newStr + chr(each)
	return newStr

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return USER_RE.match(username)

USER_PS = re.compile(r"^.{3,20}$")
def valid_password(password):
	return USER_PS.match(password)

USER_EM = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return USER_EM.match(email)

def valid_verify(pass1, pass2):
	if pass1 == pass2:
		return True



form = """
	<form method="post">
		What is your Birthday
		<br><br>
		<label>Month<input type="text" name="month" value="%(month)s"></label><br><br>
		<label>Day<input type="text" name="day" value="%(day)s"></label><br><br>
		<label>Year<input type="text" name="year" value="%(year)s"></label><br><br>
		<br>
		<div style="color: red">%(error)s</div>
		<br>
		<input type="submit">
	</form>
"""

rot13 = """
	<form method="post">
		<textarea name="rotting" id="" cols="30" rows="10">%(rotValue)s</textarea>
		<input type="submit">
	</form>
"""

signup = """
	<form method="post">
		<label>Username : <input type="text" name="username"><span style="color: red;"> %(usererror)s</span></label><br><br>
		<label>Password : <input type="password" name="password"><span style="color: red;"> %(passerror)s</span></label><br><br>
		<label>Verify Password : <input type="password" name="verify"><span style="color: red;"> %(verifyerror)s</span></label><br><br>
		<label>Email : <input type="text" name="email"><span style="color: red;"> %(submiterror)s</span></label><br>
		<br>
		<input type="submit">
	</form>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error":error, "month": escape_html(month), "day": escape_html(day), "year": escape_html(year)})

    def get(self):
    	# self.response.headers['content-type'] = 'text/plain'
        self.write_form()
	
	

    def post(self):
    	user_month = self.request.get('month')
    	user_day = self.request.get('day')
    	user_year = self.request.get('year')

    	month = valid_month(user_month)
    	day = valid_day(user_day)
    	year = valid_year(user_year)

    	if not (month and day and year):
    		self.write_form("Not look good to me", user_month, user_day, user_year)
    	else:
    		self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! it's great")


class RotHandler(webapp2.RequestHandler):
	def write_rot(self, val=""):
		self.response.out.write(rot13 % {"rotValue": val})

	def get(self):
		self.write_rot()

	def post(self):
		n = self.request.get('rotting')
		value = rot(n)
		self.write_rot(value)

class SignupHandler(webapp2.RequestHandler):
	def write_signup(self, usererror="", passerror="", verifyerror="", submiterror=""):
		self.response.out.write(signup % {"usererror": usererror, "passerror": passerror, "verifyerror": verifyerror, "submiterror": submiterror})

	def get(self):
		self.write_signup()


	def post(self):
		user_name = self.request.get('username')
		user_password = self.request.get('password')
		user_verify = self.request.get('verify')
		user_mail = self.request.get('email')

		user = valid_username(user_name)
		upass = valid_password(user_password)
		vpass = valid_verify(user_password, user_verify)
		vemail = valid_email(user_mail)


		if not (user and upass and vpass and vemail):
			self.write_signup("Not look good to me!")
		else:
			self.redirect('/welcome')

class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Welcome")

app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler), ('/rot', RotHandler), ('/signup', SignupHandler), ('/welcome', WelcomeHandler)], debug=True)