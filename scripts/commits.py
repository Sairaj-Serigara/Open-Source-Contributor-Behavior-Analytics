from github_api import github_get
from config import BASE_URL

def get_last_commit(owner, repo, username):

    url = f"{BASE_URL}/repos/{owner}/{repo}/commits"

    params = {
        "author": username,
        "per_page": 1
    }

    commits = github_get(url, params)

    if not commits:
        return None

    return commits[0]["commit"]["author"]["date"]