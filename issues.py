from conf import GITHUB_TOKEN, JIRA_AUTH, ISSUES_JQL
from github import Github
from jira import JIRA
from notify import notify_open_prs


jac = JIRA(**JIRA_AUTH)
gh = Github(GITHUB_TOKEN)


board_id = 166
sprints = jac.sprints(board_id)
for sprint in sprints:
    if sprint.state == 'ACTIVE':
        break
issues = jac.search_issues(
    jql_str=ISSUES_JQL.format(sprint.name), expand='changelog')


prs_dict = {}
for issue in issues:
    prs = [item.as_pull_request() for item in gh.search_issues(issue.key)]
    for pr in prs:
        if pr.title.startswith(issue.key):
            prs_dict[issue.key] = {'pr': pr, 'ticket': issue}

notify_open_prs(prs_dict)
