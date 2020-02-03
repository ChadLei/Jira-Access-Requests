Access Request Script
=============

This script handles all incoming access request type tasks that involved creating new users in Crowd as well as reactivating/deactivating users. Currently does not support updating user information since requests are unique and tickets are not strict on input format.

Required Libraries
=============

crowd
jira
emoji (for visual purposes)

To Run
=============

```python
python access_requests.py
```

Files
=============

Main files:

*access_requests.py*

* The main file to run to start the script. This file does all the adding/reactivating/deactivating requested in a ticket.

*email_sender.py*

* Sends welcome email to new/reactivated users and also comes with functions that send completion-notification and fail-notification emails if desired.

*issue_finder.py*

* Finds issues currently assigned to the current user.

Extra files (not needed/connected to main files):

*function_tester.py*

* Used to test functions before applying it to access_requests.py

*jira_api.py*

* Used to play around with the jira api and to learn more

Helpful Links
=============

Crowd Python API: https://github.com/pycontribs/python-crowd
Example quickstart: https://pypi.org/project/jira/
To find field names from Jira: https://jira.readthedocs.io/en/master/jirashell.html
Access request screen: https://issues.ngptools.com/jira/secure/admin/ConfigureFieldScreen.jspa?id=12040