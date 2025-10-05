"""Project information based on the pyproject.toml."""
from io import TextIOWrapper  # noqa: F401
from pathlib import Path
from typing import Any, override

from project_meta.project_info import _ProjectInfoBase, _ProjectKey


class ProjectInfoPyProject(_ProjectInfoBase):
    """Project information based on the pyproject.toml."""

    def __init__(self, project_root: Path, pyproject_data: dict[str, Any]) -> None:
        """Initialize the project information from pyproject.toml data.

        :param project_root: Path to the project's root directory.
        :param pyproject_data: Parsed pyproject.toml data.
        """
        super().__init__()
        self.project_root = project_root
        self.pyproject_data = pyproject_data

    @override
    def _get_item_impl(self, project_key: _ProjectKey) -> str:
        match project_key:
            case _ProjectKey.NAME:
                return self._get_value(['project', 'name'])
            case _ProjectKey.VERSION:
                return self._get_version()
            case _ProjectKey.DESCRIPTION:
                return self._get_value(['project', 'description'])
            case _ProjectKey.AUTHOR:
                return ", ".join(author.get("name") for author in self._get_pyproject(['project', 'authors']))
            case _ProjectKey.HOMEPAGE_URL:
                return self._get_value(['urls', 'homepage'])
            case _:
                raise ValueError(f"Unknown project key: {project_key}")

    def _get_pyproject(self, elements: list[str]) -> Any:
        # Navigate through nested elements
        data = self.pyproject_data
        for element in elements:
            data = data.get(element, {})
        return data

    def _get_value(self, elements: list[str]) -> str:
        value = self._get_pyproject(elements)
        if not value:
            raise ValueError(f"[{']['.join(elements)}] was not found in pyproject.toml")
        return str(value)

    def _get_version(self) -> str:
        """Read the version from the pyproject.toml [project][version], dynamic section [tool.setuptools.dynamic] or 'VERSION' file.

        This does not support [tool.setuptools_scm] version scheme.
        :return: Project version.
        :raises ValueError: If the version is not found in any of the expected locations.
        """
        # Try to read version from [project][version] section first
        try:
            return self._get_value(['project', 'version'])
        except ValueError:
            pass
        try:
            # Fallback: Try to read it from [tool.setuptools.dynamic] section
            version_file_name = self.project_root / self._get_value(['tool', 'setuptools', 'dynamic', 'version', 'file'])
        except ValueError:
            # Fallback: Try the default VERSION file
            version_file_name = self.project_root / "VERSION"
        try:
            with open(file=version_file_name, encoding="utf-8") as file_ver:  # type: TextIOWrapper
                project_version = str(file_ver.read().strip())
        except FileNotFoundError as err:
            raise ValueError("Project version is not defined by [project][version] or [tool.setuptools.dynamic]") from err
        return str(project_version)
