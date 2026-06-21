from github_api import github_get
from config import BASE_URL


def get_contributors(owner, repo, limit=50):
    """
    Fetch top contributors for a repository.
    """
    url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"
    params = {"per_page": limit}
    data = github_get(url, params)
    if not data:
        return []
    contributors = []
    for contributor in data:
        contributors.append(
            {
                "repository": repo,
                "username": contributor["login"],
                "id": contributor["id"],
                "contributions": contributor["contributions"],
                "profile_url": contributor["html_url"],
            }
        )

    return contributors
