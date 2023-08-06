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
Issue Class

This model manipulates a Issue in GitLab
"""
import logging
from .gitlab import GitLab

logger = logging.getLogger()


class Issue:
    """Manipulates a Issue in GitLab"""

    gitlab: GitLab = None

    def __init__(self, gitlab: GitLab):
        """Constructor"""
        self.gitlab = gitlab

    def create(self, data: dict) -> dict:
        """Creates a issue in GitLab"""
        results = self.gitlab.post("issues", data)
        if not results:
            logger.error("Create Issue failed!")
        return results

    def delete_by_id(self, issue_id: str):
        """Deletes a issue in GitLab by id"""
        self.gitlab.delete(f"issues/{issue_id}")

    def delete(self, data: dict):
        """Deletes a issue in GitLab"""
        issues = self.find_by_title(data["title"])
        for issue in issues:
            self.delete_by_id(issue["iid"])

    def delete_all(self):
        """Deletes all issue in the Project"""
        issues = self.all()
        for issue in issues:
            self.delete_by_id(issue["iid"])

    def all(self) -> list:
        """Returns all of the issues"""
        return self.gitlab.get("issues")

    def find(self, issue_id: str) -> dict:
        """Find an issue by it's id"""
        result = self.gitlab.get(f"issues/{issue_id}")
        return result

    def find_by_title(self, title: str) -> list:
        """Find a issue by it's title"""
        issues = self.all()
        result = [issue for issue in issues if issue["title"] == title]
        return result
