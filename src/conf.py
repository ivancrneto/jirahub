import os


JIRA_AUTH = {
    'options': {
        'server': os.environ['JIRA_AUTH_SERVER'],
    },
    'basic_auth': (os.environ['JIRA_AUTH_EMAIL'],
                   os.environ['JIRA_AUTH_PASS']),
}

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
GITHUB_USERS_EXCLUDE = os.getenv('GITHUB_USERS_EXCLUDE').split(', ')


SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']
SLACK_WEBHOOK_USERNAME =  os.environ['SLACK_WEBHOOK_USERNAME']
SLACK_WEBHOOK_USERNAME_ICON_URL = os.environ['SLACK_WEBHOOK_USERNAME_ICON_URL']
SLACK_NOTIFY_CHANNEL = os.environ['SLACK_NOTIFY_CHANNEL']
