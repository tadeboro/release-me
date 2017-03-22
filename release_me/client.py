# coding: utf-8
# Copyright (c) 2017 Tadej Borovšak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import requests
import logging


fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fh = logging.FileHandler("tmp.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(fmt)

logger = logging.getLogger(__name__)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


class GithubClientError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "GithubClientError: {}".format(self.msg)


class GithubClient:
    """
    Github client
    """

    ENDPOINT = "https://api.github.com"
    RELEASES_TMPL = "repos/{}/releases"
    RELEASE_TMPL = "repos/{}/releases/{}"

    def __init__(self, token):
        logger.debug("Initializing Github client")
        self.headers = {
            "User-Agent": "tadeboro",
            "Authorization": "Token {}".format(token),
        }
        self._validate_token()

    def _validate_token(self):
        logger.debug("Validating OAuth token")
        if self._get().status_code != 200:
            logger.error("Invalid token")
            raise GithubClientError("Invalid token")

    def _do_request(self, method, path, **kwargs):
        url = "{}/{}".format(self.ENDPOINT, path)
        return method(url, headers=self.headers, **kwargs)

    def _get(self, path=""):
        logger.debug("GET '{}'".format(path))
        return self._do_request(requests.get, path)

    def _post(self, path, data):
        logger.debug("POST '{}' ({})".format(path, data))
        return self._do_request(requests.post, path, json=data)

    def _delete(self, path):
        logger.debug("DELETE '{}'".format(path))
        return self._do_request(requests.delete, path)

    def get_repo(self, repo):
        resp = self._get("repos/{}".format(repo))
        return resp.status_code == 200, resp.json()

    def get_release(self, repo, tag):
        resp = self._get("repos/{}/releases/tags/{}".format(repo, tag))
        return resp.status_code == 200, resp.json()

    def create_release(self, repo, tag, body):
        data = {
            "tag_name": tag,
            "name": tag,
            "body": body,
        }
        resp = self._post("repos/{}/releases".format(repo), data)
        return resp.status_code == 201, resp.json()

    def delete_release(self, repo, id):
        resp = self._delete("repos/{}/releases/{}".format(repo, id))
        success = resp.status_code == 204
        return success, {} if success else resp.json()
