import requests
from config import GITHUB_TOKEN

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def github_get(url, params=None, return_response=False):
    """
    Generic GET request to GitHub API.
    """

    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    if response.status_code == 200:
        if return_response:
            return response
        return response.json()

    print(f"Error {response.status_code}: {response.text}")
    return None