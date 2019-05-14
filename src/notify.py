import arrow
import json

from .clients import slack
from .conf import GITHUB_USERS_EXCLUDE


def notify_open_prs(bundles):
    bundle_template = (
        '{issue_key}: PR created {pr_created}, transitioned to code review '
        '{review_transition} - {pr_html}')
    bundles_texts = []

    for bundle in bundles:
        if not bundle.pr.review_started:
            continue

        transition = bundle.issue.transition_date(
            'To Do', 'Code Review')
        transition = transition.humanize() if transition else '?'

        bundles_texts.append(bundle_template.format(
            issue_key=bundle.issue.key,
            pr_created=bundle.pr.created_at.humanize(),
            review_transition=transition,
            pr_html=bundle.pr.html_url,
        ))

    if bundles_texts:
        slack.notify(
            '*Open PRs with no reviewers:*\n' + '\n'.join(bundles_texts))
