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

app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler), ('/rot', RotHandler)], debug=True)