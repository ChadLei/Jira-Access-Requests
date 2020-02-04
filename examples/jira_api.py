from jira import JIRA

'''
Helpful Links:

Example quickstart: https://pypi.org/project/jira/
To find field names from Jira: https://jira.readthedocs.io/en/master/jirashell.html
Access request screen: https://issues.ngptools.com/jira/secure/admin/ConfigureFieldScreen.jspa?id=12040
'''

def main():
    #jira = JIRA('https://jira.atlassian.com')
    jira = JIRA(basic_auth=('chadlei', 'password1234567'), options={'server': 'https://issues.ngptools.com/jira/'})

    ticket_number = 'COLLAB-20535'
    issue = jira.issue(ticket_number)
    first_name = issue.fields.customfield_13915
    last_name = issue.fields.customfield_13916
    email = issue.fields.customfield_13917

    if issue.fields.issuetype.name == 'Access Request':
        print 'hell yea'

    # print(issue.fields.project.key)
    # print(issue.fields.reporter.displayName)

	# project = jira.project('BRAND')
	# print(project.name)                 # 'JIRA'
	# print(project.lead.displayName)     # 'John Doe [ACME Inc.]'

	# versions = jira.project_versions(project)
	# for i in [v.name for v in reversed(versions)]:
	# 	if i == "2020_04.0":
	# 		print(i)


if __name__== "__main__" :
     main()
