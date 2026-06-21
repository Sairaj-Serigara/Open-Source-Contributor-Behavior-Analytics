import time
import requests
import os
import json

MAX_COMMITS = 200
PER_PAGE = 100

from config import BASE_URL, HEADERS, MAX_RETRIES, RETRY_DELAY, REQUEST_TIMEOUT


def github_get(endpoint, params=None):
    """
    Makes a GET request to GitHub API with
    retry handling and rate-limit handling.
    """

    url = f"{BASE_URL}{endpoint}"
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT
            )
            # -------------------------
            # Success
            # -------------------------
            if response.status_code == 200:
                return response.json()

            # -------------------------
            # Rate Limit
            # -------------------------
            if response.status_code == 403:
                remaining = response.headers.get("X-RateLimit-Remaining")
                if remaining == "0":
                    reset = int(response.headers.get("X-RateLimit-Reset"))
                    wait = max(reset - int(time.time()), 0) + 5
                    print(f"Rate limit reached.")
                    print(f"Sleeping {wait} seconds...")
                    time.sleep(wait)
                    continue

            # Other Errors

            print(f"GitHub Error {response.status_code}")
            return None

        except requests.exceptions.RequestException:

            print(f"Retry {attempt + 1}/{MAX_RETRIES}")

            time.sleep(RETRY_DELAY)

    return None


def get_recent_commits(owner, repo, username):
    """
    Returns up to MAX_COMMITS recent commits
    made by one contributor.
    """

    commits = []

    pages = MAX_COMMITS // PER_PAGE

    for page in range(1, pages + 1):

        data = github_get(
            f"/repos/{owner}/{repo}/commits",
            params={"author": username, "per_page": PER_PAGE, "page": page},
        )

        if not data:
            break

        commits.extend(data)

        if len(data) < PER_PAGE:
            break

    return commits


def get_repository_pull_requests(owner, repo, max_prs=1000):

    cache_dir = "data/raw/pr_cache"
    os.makedirs(cache_dir, exist_ok=True)

    cache_file = os.path.join(cache_dir, f"{repo}_prs.json")

    # -----------------------------
    # Load cache if available
    # -----------------------------
    if os.path.exists(cache_file):

        print(f"Loading cached PRs for {repo}")

        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------
    # Download from GitHub
    # -----------------------------
    prs = []

    per_page = 100
    pages = max_prs // per_page

    for page in range(1, pages + 1):

        print(f"Downloading {repo} PR page {page}")

        endpoint = f"/repos/{owner}/{repo}/pulls"

        params = {
            "state": "all",
            "sort": "updated",
            "direction": "desc",
            "per_page": per_page,
            "page": page,
        }

        data = github_get(endpoint, params)

        if not data:
            break

        prs.extend(data)

        if len(data) < per_page:
            break

    # -----------------------------
    # Save cache
    # -----------------------------
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(prs, f)

    print(f"Saved cache -> {cache_file}")

    return prs


def get_repository_issues(owner, repo, max_issues=1000):
    cache_dir = "data/raw/issues_cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, f"{repo}_issues.json")

    # -----------------------------
    # Load cache
    # -----------------------------
    if os.path.exists(cache_file):
        print(f"Loading cached issues for {repo}")
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    issues = []
    per_page = 100
    pages = max_issues // per_page

    for page in range(1, pages + 1):
        print(f"Downloading {repo} issue page {page}")
        endpoint = f"/repos/{owner}/{repo}/issues"
        params = {
            "state": "all",
            "sort": "updated",
            "direction": "desc",
            "per_page": per_page,
            "page": page,
        }

        data = github_get(endpoint, params)

        if not data:
            break
        issues.extend(data)
        if len(data) < per_page:
            break
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(issues, f)
    print(f"Saved cache -> {cache_file}")
    return issues
