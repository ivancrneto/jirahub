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
    boards_ids = {165: {}}
    prs_dict = {}

    for sprint in jira.active_sprints(boards_ids):
        for issue in jira.issues_in_sprint(sprint):
            prs = [item.as_pull_request() for
                   item in github.search_issues(issue.key)]
            for pr in prs:
                if pr.title.startswith(issue.key):
                    prs_dict[issue.key] = {'pr': pr, 'ticket': issue}

    notify_open_prs(prs_dict)


if __name__ == '__main__':
    check_prs_missing_reviewer()
