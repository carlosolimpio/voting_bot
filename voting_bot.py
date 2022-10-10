"""
Script used to automatically vote
"""
#!/usr/bin/python

import time
from robobrowser import RoboBrowser
import constants
import ignored_constants as iconstants

def print_result(index, browser):
    points_html = str(browser.parsed)
    result = f'Link {index + 1} voted with success! {points_html} points'
    print(result)

def print_log_in_status(html, user):
    if constants.ID_CREDITS in html:
        print(f'{user} logged with success.')
    else:
        constants.LOGIN_ERROR_MESSAGE

def main():
    print(constants.START_SCRIPT_MESSAGE)
    print(constants.ACCESSING_URL_MESSAGE)

    browser = RoboBrowser(history=True, parser=constants.HTML_PARSER)
    browser.open(iconstants.LOGIN_URL)

    # get log in form
    login_form = browser.get_form(id=constants.LOGIN_FORM)

    # fill log in form with credentials
    login_form[constants.USERNAME].value = iconstants.USERNAME
    login_form[constants.PASSWORD].value = iconstants.PASSWORD

    print(constants.LOGGING_IN_MESSAGE)

    # submit log in form
    browser.submit_form(login_form)

    html_logged = str(browser.parsed)
    print_log_in_status(html_logged, constants.USERNAME)

    if constants.VOTE_SITE in html_logged:
        index = iconstants.INDEX

        while constants.VOTE_SITE in html_logged:
            print(constants.VOTING_MESSAGE)

            result = browser.session.post(
                iconstants.HREF_URL,
                data={
                    constants.VOTE_LINK: iconstants.VOTE_LINKS[index],
                    constants.REF: constants.HREF_ZERO
                })
            browser._update_state(result)
            time.sleep(constants.VOTING_TIME)

            result = browser.session.get(
                iconstants.RELOAD_URL + iconstants.VOTE_LINKS[index],
                params={
                    constants.RELOAD_LINK: constants.RELOAD_ONE,
                    constants.RELOAD_ONE: iconstants.VOTE_LINKS[index]
                })
            browser._update_state(result)
            time.sleep(constants.RELOAD_TIME)

            result = browser.session.post(
                iconstants.HREF_URL,
                data={constants.CHECK: constants.POINTS}
            )
            browser._update_state(result)

            # Prints on the screen
            print_result(index, browser)

            # move from next vote_link's index
            index = index + 1

            # reaload page
            result = browser.session.get(iconstants.LOGIN_URL)
            browser._update_state(result)
            html_logged = str(browser.parsed)
            time.sleep(constants.RELOAD_TIME)

        print(constants.END_OF_PROGRAM_MESSAGE)
    else:
        result = html_logged.find(constants.NEXT_VOTE_AFTER_STRING)
        if result != -1:
            print(html_logged[result:result+28])


if __name__ == "__main__":
    main()
