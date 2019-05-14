import itertools

from .clients import (
    github,
    jira,
)
from .core import pack
from .notify import notify_open_prs


def check_prs_missing_reviewer():
    bundles = []
    for sprint in jira.active_sprints():
        issues = jira.issues_in_sprint(sprint)
        prs = [
            item.as_pull_request()
            for item in github.search_issues(' '.join(keys))
        ]
        itertools.chain(bundles, pack(issues, prs))

    notify_open_prs(prs_dict)


if __name__ == '__main__':
    check_prs_missing_reviewer()
