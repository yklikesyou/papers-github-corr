import requests
from util import valid_github_url_check, get_github_api_url


class GithubAPIServicer:
    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

    def _get_star_from_api(self, api_url: str):
        # get json from api url
        response = requests.get(api_url, auth=(self.user_id, self.token))
        if response.status_code != 200:
            raise RuntimeError(
                f"Can't get response from {api_url}!!! status_code: {response.status_code}")

        response_data = response.json()
        return response_data['stargazers_count'], response_data['subscribers_count'], response_data['forks_count'], response_data['open_issues_count']

    def get_github_star(self, github_url: str):

        # https://github.com/${USERNAME}/${REPO}
        if not valid_github_url_check(github_url):
            raise RuntimeError(
                f"The given url {github_url} is not github url!!!")

        username, repo = github_url.split("/")[-2:]
        api_url = get_github_api_url(username, repo)
        stars, watchers, forks, issues = self._get_star_from_api(api_url)
        return stars, watchers, forks, issues
