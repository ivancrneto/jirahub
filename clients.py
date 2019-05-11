import requests

from github import Github
from jira import JIRA

from conf import (
    GITHUB_TOKEN,
    JIRA_AUTH,
    SLACK_WEBHOOK_URL,
    SLACK_WEBHOOK_USERNAME,
    SLACK_WEBHOOK_USERNAME_ICON_URL,
    SLACK_NOTIFY_CHANNEL,
)


class Slack:
    WEBHOOK_URL = SLACK_WEBHOOK_URL

    def __init__(self, username=None, channel=None, icon_url=None):
        self.username = username or SLACK_WEBHOOK_USERNAME,
        self.channel = channel or SLACK_NOTIFY_CHANNEL,
        self.icon_url = icon_url or SLACK_WEBHOOK_USERNAME_ICON_URL

    def notify(text, channel=None):
        payload = {
            'text': text,
            'username': self.username,
            'channel': channel or self.channel,
            'icon_url': self.icon_url,
        }
        requests.post(self.WEBHOOK_URL, json=payload)


jira = JIRA(**JIRA_AUTH)
github = Github(GITHUB_TOKEN)
slack = Slack()
