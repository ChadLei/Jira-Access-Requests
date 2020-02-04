import crowd
import os, sys, getpass
import time
from jira import JIRA
from email_sender import send_email
from issue_finder import find_issues

app_url = 'https://crowd.ngptools.com/crowd/'
app_user = 'crowd-automation'
app_pass = 'password'

''' Adds user, adds attributes, adds groups, transitions workflow to complete, and finally sends an email to new user '''
def activate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    print 'Attempting to add new user ....'
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
        print "---- Failed to add - attempting to reactivate user instead. ----"
        return reactivate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated)

''' Reactivates user, adjusts attributes, and transitions workflow to complete'''
def reactivate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    print 'Attempting to reactivate user ....'
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

''' Deactivates user, adjusts attributes, and transitions workflow to complete'''
def deactivate_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    print 'Attempting to deactivate user ....'
    if cs.set_active(username, False):
        print "---- " + username + " has been successfully deactivated!"
        if cs.set_user_attribute(username,'Ticket Number',ticket_number) & cs.set_user_attribute(username,'lastAuthenticated',lastAuthenticated):
            print "---- Attributes have been adjusted! ----"
        jira.transition_issue(issue, '971')
        return 1
    else:
        print "---- Failed to deactivate - please check the user for further information. ----"
        return 0

''' IN PROGRESS - figure out if this type of ticket needs to be automated or done manually: Adjusts user attributes/groups and transitions workflow to complete'''
def update_user(jira, issue, cs, username, first_name, last_name, display_name, password, email, ticket_number, lastAuthenticated):
    print ticket_number + "'s request type is to update existing user - please complete this manually."
    return 0

jira = JIRA(basic_auth=('chadlei', 'password1234567'), options={'server': 'https://issues.ngptools.com/jira/'})
cs = crowd.CrowdServer(app_url, app_user, app_pass)

email = 'Jennifer.hodroge@vmlyr.com'
password = 'password1234'
username = 'jeffbelbeck'
name = 'Jennifer Hodroge'

request_types = {
    'New User': activate_user,
    'Deactivate User': deactivate_user,
    'Reactivate User': reactivate_user,
    'Update Existing User': update_user
}

# print str(request_types['New User'])
# print cs.add_user(username, password=password, email=email)



# found_email = 'Not found'
# retry_limit = 5
# try_attempts = 0
# while (found_email == 'Not found') & (try_attempts < retry_limit):
#     try:
#         cs = crowd.CrowdServer(app_url, app_user, app_pass)
#         found_email = cs.search('user', 'name', 'chadlee')['users'][0]['email']
#         try_attempts += 1
#     except (IndexError, TypeError):
#         try_attempts += 1
#         continue
# print found_email
# access_requests = find_issues(jira)['Access Request']
# for request in access_requests:
#     ticket_number = request
#     issue = jira.issue(ticket_number)
#     email = str(issue.fields.customfield_13917)
#     print email.split(' ')[0]

def search_user_email(cs, email):
    ''' Same as the user_exists function, we check for a user's info multiple times to ensure user does/doesn't exist '''
    found_email = 'Not found'
    retry_limit = 5
    try_attempts = 0
    while (found_email == 'Not found') & (try_attempts < retry_limit):
        try:
            cs = crowd.CrowdServer(app_url, app_user, app_pass)
            found_email = cs.search('user', 'email', email)['users'][0]
            try_attempts += 1
        except (IndexError, TypeError):
            try_attempts += 1
            continue
    return found_email

while True:
    print search_user_email(cs, 'bjenki37')['name']
    time.sleep(1)
