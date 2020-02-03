from jira import JIRA

def find_issues(jira):
    # Dictionary to gather all issues seperated by types - example: {issue_type_name: [issue_number]}
    types_of_issues = {}

    # Search for assigned issues and gathers the ticket numbers into types_of_issues
    my_issues = jira.search_issues('assignee = currentUser() AND resolution = Unresolved order by updated DESC', maxResults=15)
    for issue_number in range(len(my_issues)): # CHANGE: just go into my_issues directly
        current_issue = jira.issue(my_issues[issue_number])
        issue_type_name = str(current_issue.fields.issuetype.name)
        types_of_issues[issue_type_name] = types_of_issues.get(issue_type_name, [])
        types_of_issues[issue_type_name].append(str(current_issue))

    # Display what type of issues are currently assigned
    print "\nAssigned Issues:\n________________\n"
    for key,value in types_of_issues.items():
        print key + ": " + str(len(value)) + " issue(s)"
    print '________________\n'

    # Return a Dictionary so that other scripts can go through all assigned issues and complete them
    return types_of_issues

if __name__== "__main__" :
    jira = JIRA(basic_auth=('chadlei', 'password1234567'), options={'server': 'https://issues.ngptools.com/jira/'})
    find_issues(jira)
