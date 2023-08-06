"""Models of GitLab artifacts"""

from .gitlab import GitLab
from .board import Board
from .label import Label
from .issue import Issue

__all__ = ('GitLab', 'Board', 'Label', 'Issue')
