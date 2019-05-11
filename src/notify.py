import arrow
import json

from .clients import slack
from .conf import GITHUB_USERS_EXCLUDE


def notify_open_prs(prs_dict):
    should_notify = []
    for key, item in prs_dict.items():
        pr = item['pr']

        comments = list(pr.get_issue_comments())
        review_started = False
        for comment in comments:
            if comment.user.login not in GITHUB_USERS_EXCLUDE:
                review_started = True

        created_at = arrow.get(pr.created_at)
        if (not len(pr.assignees) and
                not review_started and
                created_at.shift(minutes=30) < arrow.utcnow()):
            should_notify += [item]

    if should_notify:
        text = '*Open PRs with no reviewers:*\n'
        for item in should_notify:
            pr = item['pr']
            ticket = item['ticket']

            created_at = arrow.get(pr.created_at)
            transition_date = created_at
            for history in ticket.changelog.histories:
                for transition_ in history.items:
                    if (transition_.fromString == 'To Do' and
                            transition_.toString == 'Code Review'):
                        transition_date = arrow.get(history.created)

            text += (
                '{}: _PR created_: {}, _Code Review column at_: {} - {}\n'
            ).format(ticket.key, created_at.strftime('%m/%d/%Y %H:%M'),
                     transition_date.strftime('%m/%d/%Y %H:%M'), pr.html_url)
        slack.notify(text)
