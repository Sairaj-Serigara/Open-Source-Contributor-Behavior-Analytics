from github_api import github_get
from config import BASE_URL


def get_recent_contributors(owner, repo, limit=50):
    recent = []
    seen = set()
    page = 1

    while len(recent) < limit:
        url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
        commits = github_get(url, {"per_page": 100, "page": page})
        if not commits:
            break
        for commit in commits:
            author = commit.get("author")
            if author is None:
                continue
            username = author["login"]
            if username in seen:
                continue
            seen.add(username)
            recent.append(
                {
                    "repository": repo,
                    "username": username,
                    "id": author["id"],
                    "profile_url": author["html_url"],
                    "contributions": None,
                }
            )

            if len(recent) == limit:
                break
        page += 1
    return recent
