import arrow

from conf import GITHUB_USERS_EXCLUDE


def pack(issues, prs):
    """
    Generates bundles from issues and pull requests, grouping them
    by key and title.
    """
    def startswith(pr, issue):
        return pr.title.startswith(issue.key)

    key_map = {
        issue.key: (
            issue,
            next(filter(prs, lambda pr: startswith(pr, issue)), None)
        )
        for issue in issues
    }
    for key, (issue, pr) in key_map.items():
        if pr is not None:
            yield Bundle(issue, pr)


class Issue:

    def __init__(self, data):
        self._data = data

    @property
    def key(self):
        """Returns the JIRA issue key."""
        return self._data.key

    def transition_date(self, from_, to):
        """
        Tries fetching a specific transition in all histories of the
        issue changelog, from a specific status, to a specific status.

        '?' can be used as a wild card in case you want to fetch a transition
        to something, not considering the `from` status, or vice-versa.
        """
        for history in self._data.changelog.histories:
            for transition in history.items:
                if (
                    (transition.fromString == from_ or from_ == '?')
                    and (transition.toString == to or to == '?')
                ):
                    return arrow.get(history.created)
        return None


class PullRequest:

    def __init__(self, data):
        self._data = data
        self._comments = None

    def get_comments(self):
        """
        Retrieves all comments from the PullRequest, this does an
        additional API call to GitHub.
        """
        if self._comments is not None:
            return self._comments
        self._comments = self._data.get_issue_comments()
        return self._comments

    @property
    def has_human_comments(self):
        """
        Returns `True` when at least one of the PullRequest comments
        was not written by a bot or integration.
        """
        for comment in self._get_comments():
            if comment.user.login not in GITHUB_USERS_EXCLUDE:
                return True
        return False

    @property
    def created_at(self):
        """Returns an arrow instance of the PullRequest `created_at`"""
        return arrow.get(self._data.created_at)

    @property
    def review_started(self):
        """Returns `True` if the a review was started in this PullRequest."""
        return (
            len(self._data.assignees)
            or self.has_human_comments
        ) and self.created_at.shift(minutes=30) < arrow.utcnow()


class Bundle:

    def __init__(self, issue, pr):
        self._issue = Issue(issue)
        self._pr = PullRequest(pr)

    @property
    def pr(self):
        return self._pr

    @property
    def issue(self):
        return self._issue
