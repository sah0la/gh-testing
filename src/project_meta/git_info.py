"""Module to retrieve git metadata for the project."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import git


@dataclass
class GitInfo:
    """Dataclass to hold git information.

    :param branch: Current git branch name.
    :param commit: Current git commit SHA.
    :param dirty: Boolean indicating if there are uncommitted changes.
    """

    @staticmethod
    def create(repo_path: Path) -> GitInfo:
        """Get the project git metadata.

        :param repo_path: Path to the git repository.
        :return: GitInfo dataclass.
        """
        try:
            repo = git.Repo(repo_path)
            sha = repo.head.object.hexsha[:7]
            branch_name = repo.active_branch.name
            return GitInfo(branch=branch_name, commit=sha, dirty=repo.is_dirty())
        except git.exc.InvalidGitRepositoryError:
            # Fallback for when the project is not a git repo (e.g., in a CI/CD build)
            return GitInfo(branch="NA", commit="", dirty=True)

    branch: str
    commit: str
    dirty: bool

    def __str__(self) -> str:
        """Return a string representation of the git information.

        :return: String with branch name and short commit SHA, e.g., 'main-abc1234-dirty'
        """
        if not self.commit:
            return "unknown-version"
        return f"{self.branch}-{self.commit[:7]}{'-dirty' if self.dirty else ''}"
