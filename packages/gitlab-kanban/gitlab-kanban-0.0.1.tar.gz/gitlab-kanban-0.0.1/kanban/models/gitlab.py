######################################################################
# Copyright 2022 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
GitLab Module

This module contains the GitLab class which implements
the HTTP calls GET, POST, PUT, and DELETE to GitLab
"""
import logging
import requests

logger = logging.getLogger()


######################################################################
# G I T L A B   W R A P P E R   C L A S S
######################################################################
class GitLab:
    """A GitLab Wrapper"""

    def __init__(self, project: str, token: str, url: str = "https://gitlab.com"):
        self.project = project
        self.token = token
        self.url = url
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def __repr__(self):
        return f"<GitLab {self.project}>"

    def get(self, path: str) -> dict:
        """GET the GitLab URL for the path"""
        payload = []
        result = requests.get(
            f"{self.url}/api/v4/projects/{self.project}/{path}", headers=self.headers
        )
        if result.status_code == 200:
            payload = result.json()
        else:
            logger.error("GET failed: RC=%s message=%s", result.status_code, result)
        return payload

    def post(self, path: str, data: dict) -> dict:
        """POST to the GitLab URL for the path"""
        payload = {}
        headers = self.headers | {"Content-Type": "application/json"}
        result = requests.post(
            f"{self.url}/api/v4/projects/{self.project}/{path}",
            json=data,
            headers=headers,
        )
        if result.status_code == 201:
            payload = result.json()
        else:
            logger.error("POST failed: RC=%s message=%s", result.status_code, result.text)
        return payload

    def put(self, path: str, data: dict) -> dict:
        """PUT the GitLab URL for the path"""
        payload = {}
        headers = self.headers | {"Content-Type": "application/json"}
        result = requests.put(
            f"{self.url}/api/v4/projects/{self.project}/{path}",
            json=data,
            headers=headers,
        )
        if result.status_code == 200:
            payload = result.json()
        else:
            logger.error("PUT failed: RC=%s message=%s", result.status_code, result)
        return payload

    def delete(self, path: str) -> None:
        """DELETE from the GitLab URL for the path"""
        result = requests.delete(
            f"{self.url}/api/v4/projects/{self.project}/{path}", headers=self.headers
        )
        if result.status_code != 204:
            logger.error("DELETE failed: RC=%s message=%s", result.status_code, result)
