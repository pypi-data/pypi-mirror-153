# GitLab Kanban Board Command Line Interface

This project provides and command line interface for generating and manipulating Kanban boards on GitLab. It was built to help teams setting up their initial Kanban board with consistent labels and lists. It also has the ability to create stories that track assets.

## Installation

```bash
pip install gitlab-kanban
```

## Usage

You should set the following environment variables so that you don't have to specify them on the command line. This is particularly convenient when working in the same project for a while.


| Parameter| Variable | Description |
|-------|----------|-------------|
| -t/--token | GITLAB_TOKEN | You GitLab authorization token |
| -p/--project | GITLAB_PROJECT | The unique ID for your GitLab project |
| -u/--url | GETLAB_URL | The GitLab url if not the default https://gitlab.com |

By setting those environment variables you can eliminate the need for using `-t`, `-p` on every call.

You can us the `--help` flag to get help on all of the commands.

```text
$ kanban --help

Usage: kanban [OPTIONS] COMMAND [ARGS]...

  GitLab Kanban Board Command Line Interface

Options:
  -t, --token TEXT       GitLab authorization token or set env GITLAB_TOKEN
                         [required]
  -p, --project TEXT     The GitLab project ID or set env GITLAB_PROJECT
                         [required]
  -u, --gitlab-url TEXT  GitLab URL [optional] defaults to https://gitlab.com
  --help                 Show this message and exit.

Commands:
  boards  Create, Get, Update, Delete Kanban Boards
  issues  Create, Get, Update, Delete Issues
  labels  Create, Get, Update, Delete Labels
```

Each command has a series of subcommands to create the various artifacts.

## CSV Formats

These are the fields that are expected in each of the CSV files:

### Labels

The columns for the labels CSV is as follows:

```
"name","description","text_color","color"
```

| Column name | Description |
|-------------|-------------|
| name        | The label name |
| description | A description of the label |
| text_color  | The text color the label |
| color       | The background color the label |

Refer to `./samples` folder for examples

### Boards

Boards in GitLab are a collection of lists that are associated with labels. The format for a board, therefore, is the same as a label. When creating a board you pss in a name for the board and a label.csv file that has the labels for the bard lists. Once this will be created for each label.

Refer to `./samples` folder for examples

### Issues

The columns for the issues CSV is as follows:

```
"title","description","labels"
```

| Column name | Description |
|-------------|-------------|
| title       | The title of the issue |
| description | The body of the issues |
| labels      | A comma separated list of labels to assign to the issue |

Refer to `./samples` folder for examples

## Development setup

This repository contains the configuration files needed by the [Remote Container](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension of [Visual Studio Code](https://code.visualstudio.com/) that can be used with [Docker Desktop](https://www.docker.com/products/docker-desktop) to bring up a complete development environment simply by starting VSCode and choosing **Restart in Container**.  

You can also create a development environment manually using a Python virtual environment (`venv`) and `pip` 

```bash
python3 -m venv .venv
source .env/bin/activate
pip install -e '.[dev]'
```
