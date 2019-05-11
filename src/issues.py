from .conf import (
    ISSUES_JQL,
    JIRA_BOARDS,
)
from .clients import (
    github,
    jira,
)
from .notify import notify_open_prs


def check_prs_missing_reviewer():
    boards_ids = JIRA_BOARDS.keys()
    prs_dict = {}
    for board_id in boards_ids:
        sprints = jira.sprints(board_id)
        for sprint in sprints:
            if sprint.state == 'ACTIVE':
                break
        issues = jira.search_issues(
            jql_str=ISSUES_JQL.format(sprint.name), expand='changelog')

        for issue in issues:
            prs = [item.as_pull_request() for
                   item in github.search_issues(issue.key)]
            for pr in prs:
                if pr.title.startswith(issue.key):
                    prs_dict[issue.key] = {'pr': pr, 'ticket': issue}

    notify_open_prs(prs_dict)


if __name__ == '__main__':
    check_prs_missing_reviewer()
