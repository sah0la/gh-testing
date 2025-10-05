from dataclasses import dataclass


@dataclass
class GitInfo:
    """Dataclass to hold git information."""

    branch: str
    commit: str
    dirty: bool

    def __str__(self) -> str:
        """Return a string representation of the git information.

        :return: String in the format 'branch-commit-sha-dirty' or 'unknown-version' if not available.
        """
        if not self.commit:
            return "unknown-version"
        return f"{self.branch}-{self.commit[:7]}{'-dirty' if self.dirty else ''}"

def get_git_info() -> GitInfo:
    """Get the current git branch and commit SHA.

    :return: String with branch name and commit SHA, e.g., 'main-abc1234-dirty'
    """
    try:
        repo_path = project_root
        repo = git.Repo(repo_path)
        sha = repo.head.object.hexsha[:7]
        branch_name = repo.active_branch.name
        return GitInfo(branch=branch_name, commit=sha, dirty=repo.is_dirty())
    except git.exc.InvalidGitRepositoryError:
        # Fallback for when the project is not a git repo (e.g., in a CI/CD build)
        return GitInfo(branch="NA", commit="", dirty=True)
