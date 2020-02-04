#!/usr/bin/env python

import emoji
import crowd
import os, sys, getpass
import time
from datetime import datetime
from jira import JIRA
from email_sender import send_email
from email_sender import panic_email
from email_sender import completion_email
from issue_finder import find_issues

app_url = 'https://crowd.ngptools.com/crowd/'
app_user = 'crowd-automation'
app_pass = 'password'

'''EDGE CASE: new user request -> same email -> different way to spell username but its for the same person'''
def activate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    ''' Adds a new user accordingly '''
    print 'Attempting to add new user ....'
    if check_for_existing_user(cs, username):
        print 'User might already exist - stand by ....'
        if search_user_info(cs, email) == 'Not found': # User exists but email wasn't found: You are trying to add a user with the same name as someone
            username = username_picker(username)
            return add_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated)
        else: # User exists & email found: The request type is wrong, so the requester actually wants to update exisiting user info instead
            print "---- Failed to add - attempting to reactivate user instead. ----"
            return reactivate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated)
    else:
        return add_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated)

def username_picker(username):
    ''' If username already exists, then this will add a number to the new username in order to distinguish them '''
    if username[-1].isalpha(): # Checks if character is a alphabet
        username = username + str(1)
    else:
        username = username[:-1] + str(int(username[-1])+1)
    return username

def add_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    ''' Adds user, adds attributes, adds groups, transitions workflow to complete, and finally sends an email to new user '''
    if cs.add_user(username, first_name=first_name, last_name=last_name, display_name=display_name, password=password, email=email):
        print "---- " + username + " has been successfully added! ----"
        if cs.set_user_attribute(username,'Ticket Number',ticket_number) & cs.set_user_attribute(username,'lastAuthenticated',lastAuthenticated):
            print "---- Attributes have been added! ----"
        if cs.add_user_to_group(username,'confluence-users') & cs.add_user_to_group(username,'jira-developers') & cs.add_user_to_group(username,'jira-users'):
            print "---- User has been added to groups! ----"
        jira.transition_issue(issue, '971')
        send_email(username, email)
        return 1
    else:
        print "---- Failed to add user for some reason ----"
        return 0

def reactivate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    ''' Reactivates user, adjusts attributes, and transitions workflow to complete '''
    print 'Attempting to reactivate user ....'

    # Double checks if correct username is being reactivated by searching by unique email
    found_info = search_user_info(cs, email)
    if found_info != 'Not found':
        username = found_info['name']

    if cs.set_active(username, True):
        print "---- " + username + " has been successfully reactivated! ----"
        if cs.set_user_attribute(username,'Ticket Number',ticket_number) & cs.set_user_attribute(username,'lastAuthenticated',lastAuthenticated):
            print "---- Attributes have been adjusted! ----"
        jira.transition_issue(issue, '971')
        send_email(username, email)
        return 1
    else:
        print "---- Failed to reactivate - please check the user for further information. ----"
        return 0

def deactivate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    ''' Deactivates user, adjusts attributes, and transitions workflow to complete '''
    print 'Attempting to deactivate user ....'

    # Double checks if correct username is being deactivated by searching by unique email
    found_info = search_user_info(cs, email)
    if found_info != 'Not found':
        username = found_info['name']

    if cs.set_active(username, False):
        print "---- " + username + " has been successfully deactivated!"
        if cs.set_user_attribute(username,'Ticket Number',ticket_number) & cs.set_user_attribute(username,'lastAuthenticated',lastAuthenticated):
            print "---- Attributes have been adjusted! ----"
        jira.transition_issue(issue, '971')
        return 1
    else:
        print "---- Failed to deactivate - please check the user for further information. ----"
        return 0

def update_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    ''' IN PROGRESS - figure out if this type of ticket needs to be automated or done manually: Adjusts user attributes/groups and transitions workflow to complete'''
    print ticket_number + "'s request type is to update existing user - please complete this manually."
    return 0

def check_for_existing_user(cs, username):
    ''' The Crowd API's user_exists function sometimes returns None despite the user existing, so check multiple times to ensure user does/does not exist. '''
    retry_limit = 7
    try_attempts = 0
    user_exists = cs.user_exists(username)
    while (user_exists is None) & (try_attempts < retry_limit): # Returns None if user does not yet exist
        cs = crowd.CrowdServer(app_url, app_user, app_pass)
        user_exists = cs.user_exists(username)
        try_attempts += 1
    return True if user_exists else False

def search_user_info(cs, email):
    ''' Same as the user_exists function, we check for a user's info multiple times to ensure user does/doesn't exist '''
    found_info = 'Not found'
    retry_limit = 6
    try_attempts = 0
    while (found_info == 'Not found') & (try_attempts < retry_limit):
        try:
            cs = crowd.CrowdServer(app_url, app_user, app_pass)
            found_info = cs.search('user', 'email', email)['users'][0]
            try_attempts += 1
        except (IndexError, TypeError):
            try_attempts += 1
            continue
    return found_info

def complete_request():
    count = 0
    try:
        # Create the jira object and find issues currently assigned (MODIFY W/ YOUR OWN CREDNTIALS)
        jira = JIRA(basic_auth=('chadlei', 'password1234567'), options={'server': 'https://issues.ngptools.com/jira/'})
        access_requests = find_issues(jira)['Access Request']
        # access_requests = [1]

        for request in access_requests: # CHANGE: loop thru issue numbers in access_requests
            # Retrieve ticket information from Jira
            # ticket_number = 'COLLAB-' + '20560'
            ticket_number = request
            issue = jira.issue(ticket_number)
            first_name = issue.fields.customfield_13915
            last_name = issue.fields.customfield_13916
            display_name = first_name + ' ' + last_name
            email = str(issue.fields.customfield_13917).split(' ')[0] # We split it here just in case the ticket doesn't include the full email address
            request_type = str(issue.fields.customfield_15611)

            # Ensure ticket has not been completed already
            if str(issue.fields.status) in ('Done','Closed'):
                print 'Issue has been resolved already - continuing on ....\n'
                continue

            # User information/attributes to add
            password = 'password1234'
            username = (first_name + last_name).encode('utf-8').replace(" ", "")
            lastAuthenticated = int(round(time.time()))

            # Create the Crowd object
            cs = crowd.CrowdServer(app_url, app_user, app_pass)

            # Switch case depending on request_type
            request_types = {
                'New User': activate_user,
                'Deactivate User': deactivate_user,
                'Reactivate User': reactivate_user,
                'Update Existing User': update_user
            }

            # Calls appropriate function based off of request_type
            print 'Current ticket: ' + ticket_number
            print 'Request type: ' + request_type
            success = request_types[request_type](jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated)

            # The Crowd API's user_exists function sometimes returns None/False despite the user existing, so check multiple times to ensure user does/does not exist.
            # SIDE NOTE: this could be turned into a helper function
            retry_limit = 5
            try_attempts = 0
            while (success == 0) & (try_attempts < retry_limit) & (request_type != 'Update Existing User'): # Returns None if user does not yet exist
                print "[Reattempt #" + str(try_attempts+1) + " to [" + request_type + "]]"
                cs = crowd.CrowdServer(app_url, app_user, app_pass)
                success = request_types[request_type](jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated)
                try_attempts += 1
                time.sleep(1)
            if success == 0:
                print "Failed to complete ticket - moving onto the next"
                panic_email(username, ticket_number, request_type)
            else:
                completion_email(username, ticket_number, request_type)

            # Adds to the count of completed tickets
            count += success
            print ''
        return count
    except KeyError as e: # KeyError would mean that there aren't currently any access request tickets in queue
        print emoji.emojize(":winking_face_with_tongue:") + ' WOOHOO currently no access request tickets in queue WOOHOO ' + emoji.emojize(":winking_face_with_tongue:") + '\n'
        return count

if __name__ == '__main__':
    count = 0
    while True:
        count += complete_request()
        print 'Last ran at: ' + str(datetime.now().strftime("%H:%M"))
        print str(count) + ' ticket(s) completed since starting.'
        print 'Now we play the waiting game....'
        time.sleep(1800)
