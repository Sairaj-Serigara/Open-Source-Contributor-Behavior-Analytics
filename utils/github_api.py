import time
import requests

from config import (
    BASE_URL,
    HEADERS,
    MAX_RETRIES,
    RETRY_DELAY,
    REQUEST_TIMEOUT
)


def github_get(endpoint, params=None):
    """
    Makes a GET request to GitHub API with
    retry handling and rate-limit handling.
    """

    url = f"{BASE_URL}{endpoint}"

    for attempt in range(MAX_RETRIES):

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=REQUEST_TIMEOUT
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

                remaining = response.headers.get(
                    "X-RateLimit-Remaining"
                )

                if remaining == "0":

                    reset = int(
                        response.headers.get(
                            "X-RateLimit-Reset"
                        )
                    )

                    wait = max(
                        reset - int(time.time()),
                        0
                    ) + 5

                    print(
                        f"Rate limit reached."
                    )

                    print(
                        f"Sleeping {wait} seconds..."
                    )

                    time.sleep(wait)

                    continue

            # -------------------------
            # Other Errors
            # -------------------------

            print(
                f"GitHub Error {response.status_code}"
            )

            return None

        except requests.exceptions.RequestException:

            print(
                f"Retry {attempt + 1}/{MAX_RETRIES}"
            )

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
            params={
                "author": username,
                "per_page": PER_PAGE,
                "page": page
            }
        )

        if not data:
            break

        commits.extend(data)

        if len(data) < PER_PAGE:
            break

    return commits