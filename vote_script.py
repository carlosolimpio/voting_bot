#!/usr/bin/python
'''
@author: Carlos Olimpio
This script was made with study purposes.

'''
from robobrowser import RoboBrowser
import time

def printResult(index, browser):
	points_html = str(browser.parsed)
	result = 'Link %d voted with success! %s points' %(index+1, points_html)
	print result

def printLogInStatus(html, user):
	if 'id="credits"' in html:
		print '%s logged with success.' %(user)
	else:
		'Login Erro.'

user = 'username'
passw = 'password'
login_url = 'http://www.thewebsitehere.com'

print '*****Starting vote_scpit.py*****'
print 'Accessing URL...'

browser = RoboBrowser(history=True, parser='html.parser')
browser.open(login_url)

#get form
login_form = browser.get_form(id='login_form')

#fill with credentials
login_form['username'].value = user
login_form['password'].value = passw

print 'Logging in...'

#submit form
browser.submit_form(login_form)

html_logged = str(browser.parsed)
printLogInStatus(html_logged, user)

href = 'http://www.thewebsitehere.com'
vote_links = ['7', '9', '10', '11', '13', '14']
index = 0

reload_url = 'http://www.thewebsitehere.com'

if 'vote_topsite' in html_logged:
	while 'vote_topsite' in html_logged:

		print 'Voting...'

		r = browser.session.post(href, data={'vote_link': vote_links[index], 'ref': '0'})
		browser._update_state(r)
		time.sleep(31)	#sleeps 31 secs

		r = browser.session.get(reload_url + vote_links[index], params={'reload_link': '1', 'link': vote_links[index]})
		browser._update_state(r)
		time.sleep(2)

		r = browser.session.post(href, data={'check': 'points'})
		browser._update_state(r)

		#Prints on the screen
		printResult(index, browser)

		#move from next vote_link's index
		index = index + 1

		#reaload page
		r = browser.session.get(login_url)
		browser._update_state(r)
		html_logged = str(browser.parsed)	
		time.sleep(3)

	print 'End of program.'

else:
	r = html_logged.find('Next vote after:')
	if r != -1:
		print html_logged[r:r+28]
	
