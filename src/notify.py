import arrow
import json

from .clients import slack
from .conf import GITHUB_USERS_EXCLUDE


def notify_open_prs(bundles):
    notifiable_bundles = []
    for bundle in bundles:
        if bundle.review_started:
            notifiable_bundles.append(bundle)

    if notifiable_bundles:
        text = '*Open PRs with no reviewers:*\n'
        for bundle in notifiable_bundles:
            for history in bundle.histories:
                for transition_ in history.items:
                    if (transition_.fromString == 'To Do' and
                            transition_.toString == 'Code Review'):
                        transition_date = arrow.get(history.created)

            text += (
                '{}: _PR created_: {}, _Code Review column at_: {} - {}\n'
            ).format(
                bundle.key, bundle.created_at.strftime('%m/%d/%Y %H:%M'),
                 transition_date.strftime('%m/%d/%Y %H:%M'), bundle.pr.html_url
            )
        slack.notify(text)
