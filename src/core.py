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


class Bundle:

    def __init__(self, issue, pr):
        self._issue = issue
        self._pr = pr
