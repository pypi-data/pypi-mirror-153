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
Label Class

This model manipulates a Label in GitLab
"""
import logging
import urllib.parse
from .gitlab import GitLab

logger = logging.getLogger()

HTML_COLORS = [
    "black",
    "silver",
    "gray",
    "white",
    "maroon",
    "red",
    "purple",
    "fuchsia",
    "green",
    "lime",
    "olive",
    "yellow",
    "navy",
    "blue",
    "teal",
    "aqua",
]


class Label:
    """Manipulates a Label in GitLab"""

    gitlab: GitLab = None

    def __init__(self, gitlab: GitLab):
        """Constructor"""
        self.gitlab = gitlab

    def create(self, data: dict) -> dict:
        """Creates a label in GitLab"""
        results = self.gitlab.post("labels", data)
        if not results:
            logger.error("Create Label failed!")
        return results

    def delete_by_name(self, name: str):
        """Deletes a label in GitLab by name"""
        name = urllib.parse.quote(name)
        self.gitlab.delete(f"labels/{name}")

    def delete_by_id(self, label_id: str):
        """Deletes a label in GitLab by id"""
        self.gitlab.delete(f"labels/{label_id}")

    def delete(self, data: dict):
        """Deletes a label in GitLab"""
        self.delete_by_name(data["name"])

    def delete_all(self):
        """Deletes all label in the Project"""
        labels = self.all()
        for label in labels:
            self.delete_by_id(label["id"])

    def all(self) -> list:
        """Returns all of the labels"""
        return self.gitlab.get("labels")

    def find(self, label_id: str) -> dict:
        """Find a label by it's id"""
        result = self.gitlab.get(f"labels/{label_id}")
        return result

    def find_by_name(self, name: str) -> list:
        """Find a label by it's name"""
        labels = self.all()
        result = [label for label in labels if label["name"] == name]
        return result
