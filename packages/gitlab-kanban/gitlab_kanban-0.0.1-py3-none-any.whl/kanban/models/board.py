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
Board Class

This model manipulates a Board in GitLab
"""
import logging
import urllib.parse
from .gitlab import GitLab

logger = logging.getLogger()


class Board:
    """Manipulates a Board in GitLab"""

    gitlab: GitLab = None

    def __init__(self, gitlab: GitLab):
        """Constructor"""
        self.gitlab = gitlab

    def create(self, data: dict) -> dict:
        """Creates a board in GitLab"""
        results = self.gitlab.post("boards", data)
        if not results:
            logger.error("Create board failed!")
        return results

    def create_list(self, board_id: str, data: dict):
        """Creates a board list in GitLab"""
        results = self.gitlab.post(f"boards/{board_id}/lists", data)
        if not results:
            logger.error("Create board list failed!")
        return results

    def delete_by_name(self, name: str):
        """Deletes a board in GitLab by name"""
        name = urllib.parse.quote(name)
        self.gitlab.delete(f"boards/{name}")

    def delete_by_id(self, board_id: str):
        """Deletes a board in GitLab by id"""
        self.gitlab.delete(f"boards/{board_id}")

    def delete(self, data: dict):
        """Deletes a board in GitLab"""
        self.delete_by_name(data["id"])

    def delete_all(self):
        """Deletes all board in the Project"""
        boards = self.all()
        for board in boards:
            self.delete_by_id(board["id"])

    def all(self) -> list:
        """Return all boards"""
        return self.gitlab.get("boards")

    def find(self, board_id: str) -> dict:
        """Find a board by it's id"""
        result = self.gitlab.get(f"boards/{board_id}")
        return result

    def find_by_name(self, name: str) -> list:
        """Find a board by it's name"""
        boards = self.all()
        result = [board for board in boards if board["name"] == name]
        return result
