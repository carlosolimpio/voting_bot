#!/usr/bin/python

from robobrowser import RoboBrowser
import time
import constants
import ignored_constants as iconstants

def printResult(index, browser):
	points_html = str(browser.parsed)
	result = 'Link %d voted with success! %s points' %(index+1, points_html)
	print(result)

def printLogInStatus(html, user):
	if constants.ID_CREDITS in html:
		print('%s logged with success.' %(user))
	else:
		constants.LOGIN_ERROR

print(constants.START_MESSAGE)
print(constants.ACCESSING_URL_MESSAGE)

browser = RoboBrowser(history=True, parser=constants.HTML_PARSER)
browser.open(iconstants.LOGIN_URL)

# get form
login_form = browser.get_form(id=constants.LOGIN_FORM)

# fill with credentials
login_form[constants.USERNAME].value = iconstants.USERNAME
login_form[constants.PASSWORD].value = iconstants.PASSWORD

print(constants.LOGGING_IN_MESSAGE)

# submit form
browser.submit_form(login_form)

html_logged = str(browser.parsed)
printLogInStatus(html_logged, user)

index = iconstants.INDEX

if constants.VOTE_SITE in html_logged:
	while constants.VOTE_SITE in html_logged:

		print(constants.VOTING_MESSAGE)

		r = browser.session.post(iconstants.HREF_URL, data={constants.VOTE_LINK: iconstants.VOTE_LINKS[index], constants.REF: constants.HREF_ZERO})
		browser._update_state(r)
		time.sleep(constants.VOTING_TIME)

		r = browser.session.get(iconstants.RELOAD_URL + iconstants.VOTE_LINKS[index], params={constants.RELOAD_LINK: constants.RELOAD_ONE, constants.RELOAD_ONE: iconstants.VOTE_LINKS[index]})
		browser._update_state(r)
		time.sleep(constants.RELOAD_TIME)

		r = browser.session.post(iconstants.HREF_URL, data={constants.CHECK: constants.POINTS})
		browser._update_state(r)

		# Prints on the screen
		printResult(index, browser)

		# move from next vote_link's index
		index = index + 1

		#reaload page
		r = browser.session.get(login_url)
		browser._update_state(r)
		html_logged = str(browser.parsed)
		time.sleep(constants.RELOAD_TIME)

	print(constants.END_OF_PROGRAM_MESSAGE)

else:
	r = html_logged.find(constants.NEXT_VOTE_AFTER_STRING)
	if r != -1:
		print(html_logged[r:r+28])
	
