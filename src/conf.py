from environs import Env
from pathlib import Path


BASE_DIR = Path(__file__).parents[0]

env = Env()
env.read_env(BASE_DIR)

with env.prefixed('JIRA_AUTH_'):
    JIRA_AUTH = {
        'options': {
            'server': env.str('SERVER'),
        },
        'basic_auth': (env.str('EMAIL'), env.str('PASS')),
    }

with env.prefixed('GITHUB_'):
    GITHUB_TOKEN = env.str('TOKEN')
    GITHUB_USERS_EXCLUDE = env.str('USERS_EXCLUDE').split(', ')

with env.prefixed('SLACK_'):
    SLACK_WEBHOOK_URL = env.str('WEBHOOK_URL')
    SLACK_WEBHOOK_USERNAME =  env.str('WEBHOOK_USERNAME')
    SLACK_WEBHOOK_USERNAME_ICON_URL = env.str('WEBHOOK_USERNAME_ICON_URL')
    SLACK_NOTIFY_CHANNEL = env.str('NOTIFY_CHANNEL')

ISSUES_JQL = env.str('ISSUES_JQL')
BOARDS_IDS = {165: {}}
