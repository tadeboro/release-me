from __future__ import print_function

import requests


class Client:

    """
    Guthub client
    """

    ENDPOINT = "https://api.github.com"

    def __init__(self, token):
        self.headers = {
            "User-Agent": "tadeboro",
            "Authorization": "Token {}".format(token),
        }
        self._validate_token()

    def _validate_token(self):
        if self._get().status_code != 200:
            raise Exception("Invalid token")

    def _get(self, path=""):
        return requests.get("{}/{}".format(self.ENDPOINT, path),
                            headers=self.headers)

    def get_repo(self, repo_name):
        resp = self._get("repos/{}".format(repo_name))
        if resp.status_code != 200:
            raise Exception("Invalid repo name")
        return resp.json()

    def list_releases(self, repo_name):
        resp = self._get("repos/{}/releases".format(repo_name))
        return resp.json()

    def create_release(self, repo, tag, body, name=None):
        data = {
            "tag_name": tag,
            "name": name if name else tag,
            "body": body,
        }
        resp = self._post(repo, data)
