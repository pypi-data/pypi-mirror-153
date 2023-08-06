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
GitLab Kanban Board Command Line Interface

This module provides a command line interface to create Kanban boards in GitLab.
Since Gitlab Kanban boards are created using labels, it has the ability to
create labels as well. Finally it can create Issues to populate a Kanban board
from a Comma Separated Value (CSV) file.
"""
import csv
import click
from tqdm import tqdm

from kanban.models.board import Board
from .models import GitLab, Label, Issue


@click.group()
@click.option(
    "-t",
    "--token",
    required=True,
    envvar="GITLAB_TOKEN",
    help="GitLab authorization token or set env GITLAB_TOKEN",
)
@click.option(
    "-p",
    "--project",
    required=True,
    envvar="GITLAB_PROJECT",
    help="The GitLab project ID or set env GITLAB_PROJECT",
)
@click.option(
    "-u",
    "--gitlab-url",
    required=False,
    envvar="GITLAB_URL",
    default="https://gitlab.com",
    help="GitLab URL [optional] defaults to https://gitlab.com",
)
@click.pass_context
def cli(ctx, token, project, gitlab_url):
    """GitLab Kanban Board Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["PROJECT"] = project
    ctx.obj["GITLAB_TOKEN"] = token
    ctx.obj["GITLAB"] = GitLab(project, token, gitlab_url)


######################################################################
# L A B E L S   C O M M A N D S
######################################################################


@cli.group()
def labels():
    """Create, list, update, delete Labels"""


# ---------------------------------------------------------------------
# CREATE LABELS
# ---------------------------------------------------------------------
@labels.command("create")
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="The CSV file with labels",
)
@click.pass_context
def create_labels(ctx, infile):
    """Creates labels for a project from a CVS file"""
    click.echo(f"Creating labels for project {ctx.obj['PROJECT']}...")
    click.echo(f"Processing {infile}...")
    label_data = csv_to_dict(infile)
    click.echo(f"Found {len(label_data)} labels...")
    click.echo("Sending to GitLab...")
    label = Label(ctx.obj["GITLAB"])
    for entry in tqdm(label_data, total=len(label_data)):
        label.create(entry)
    click.echo("Done")


# ---------------------------------------------------------------------
# LIST LABELS
# ---------------------------------------------------------------------
@labels.command("list")
@click.pass_context
def list_labels(ctx):
    """Returns all of the labels for a project"""
    click.echo(f"Getting labels for project {ctx.obj['PROJECT']}...")
    label = Label(ctx.obj["GITLAB"])
    results = label.all()
    click.echo(results)


# ---------------------------------------------------------------------
# DELETE LABELS
# ---------------------------------------------------------------------
@labels.command("delete")
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="The CSV file with the labels to delete",
)
@click.pass_context
def delete_labels(ctx, infile):
    """Deletes labels for a project from a CVS file"""
    click.echo(f"Deleting labels for project {ctx.obj['PROJECT']}...")
    click.echo(f"Processing {infile}...")
    label_data = csv_to_dict(infile)
    click.echo(f"Found {len(label_data)} labels...")
    click.echo("Sending to GitLab...")
    label = Label(ctx.obj["GITLAB"])
    for entry in tqdm(label_data, total=len(label_data)):
        label.delete_by_name(entry["name"])
    click.echo("Done")


######################################################################
# B O A R D S   C O M M A N D S
######################################################################


@cli.group()
def boards():
    """Create, list, update, delete Kanban Boards"""


# ---------------------------------------------------------------------
# LIST BOARDS
# ---------------------------------------------------------------------
@boards.command("list")
@click.pass_context
def list_boards(ctx):
    """Returns all of the kanban boards for a project"""
    click.echo(f"Getting kanban boards for project {ctx.obj['PROJECT']}...")
    board = Board(ctx.obj["GITLAB"])
    board_data = board.all()
    board_list = []
    for item in board_data:
        board_list.append(dict(id=item['id'], name=item['name']))
    click.echo(board_list)


# ---------------------------------------------------------------------
# CREATE BOARDS
# ---------------------------------------------------------------------
@boards.command("create")
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="The CSV file with list labels",
)
@click.option("--name", "-n", required=True, help="The name of the kanban board")
@click.pass_context
def create_boards(ctx, infile, name):
    """Creates kanban board for a project from a CVS file of labels"""
    click.echo(f"Creating kanban board for project {ctx.obj['PROJECT']}...")
    click.echo(f"Processing {infile}...")
    board = Board(ctx.obj["GITLAB"])
    # generate board
    board_data = {"name": name}
    click.echo("Sending to GitLab...")
    results = board.create(board_data)
    board_id = results["id"]
    board_data["id"] = board_id
    click.echo(f"Board {board_id} created")
    click.echo(board)

    # Create the labels
    click.echo("Creating labels...")
    label_data = csv_to_dict(infile)
    click.echo(f"Found {len(label_data)} labels...")
    label = Label(ctx.obj["GITLAB"])
    for entry in tqdm(label_data, total=len(label_data)):
        results = label.create(entry)
        data = {"label_id": results["id"]}
        results = board.create_list(board_id, data)

    # Get the new board
    results = board.find(board_id)
    click.echo(f"New board {name} created")
    click.echo(results)


# ---------------------------------------------------------------------
# DELETE BOARDS
# ---------------------------------------------------------------------
@boards.command("delete")
@click.option("--board_id", "-b", required=True, help="The id of the kanban board")
@click.pass_context
def delete_boards(ctx, board_id):
    """Deletes kanban board from a project"""
    click.echo(f"Deleting kanban board for project {ctx.obj['PROJECT']}...")
    # Find the board
    click.echo(f"Finding board with id {board_id}...")
    board = Board(ctx.obj["GITLAB"])
    board.delete_by_id(board_id)
    click.echo(f"Board {board_id} deleted.")


######################################################################
# I S S U E S   C O M M A N D S
######################################################################


@cli.group()
def issues():
    """Create, list, update, delete Issues"""


# ---------------------------------------------------------------------
# CREATE ISSUES
# ---------------------------------------------------------------------
@issues.command("create")
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="The CSV file with issues",
)
@click.pass_context
def create_issues(ctx, infile):
    """Creates issues for a project from a CVS file"""
    click.echo(f"Creating issues for project {ctx.obj['PROJECT']}...")
    click.echo(f"Processing {infile}...")
    issue_data = csv_to_dict(infile)
    click.echo(f"Found {len(issue_data)} issues...")
    click.echo("Sending to GitLab...")
    issue = Issue(ctx.obj["GITLAB"])
    for entry in tqdm(issue_data, total=len(issue_data)):
        issue.create(entry)
    click.echo("Done")


# ---------------------------------------------------------------------
# LIST ISSUES
# ---------------------------------------------------------------------
@issues.command("list")
@click.pass_context
def list_issues(ctx):
    """Returns all of the issues for a project"""
    click.echo(f"Getting issues for project {ctx.obj['PROJECT']}...")
    issue = Issue(ctx.obj["GITLAB"])
    results = issue.all()
    click.echo(results)


# ---------------------------------------------------------------------
# DELETE ISSUES
# ---------------------------------------------------------------------
@issues.command("delete")
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True),
    required=True,
    help="The CSV file with the issues to delete",
)
@click.pass_context
def delete_issues(ctx, infile):
    """Deletes issues for a project from a CVS file"""
    click.echo(f"Deleting issues for project {ctx.obj['PROJECT']}...")
    click.echo(f"Processing {infile}...")
    issue_data = csv_to_dict(infile)
    click.echo(f"Found {len(issue_data)} issues...")
    click.echo("Sending to GitLab...")
    issue = Issue(ctx.obj["GITLAB"])
    for entry in tqdm(issue_data, total=len(issue_data)):
        issue.delete(entry)
    click.echo("Done")


######################################################################
# U T I L I T I E S
######################################################################
def csv_to_dict(filename: str) -> list:
    """Converts a CSV file to a dictionary"""
    data = []
    with open(filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data
