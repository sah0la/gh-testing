"""Project information based on the <project>.egg-info/PKG-INFO."""
from __future__ import annotations

from importlib import metadata
from typing import override

from project_meta.project_info import _ProjectInfoBase, _ProjectKey


class ProjectInfoPkg(_ProjectInfoBase):
    """Project information based on the <project>.egg-info/PKG-INFO.

    To access most of the information, the <project>.egg-info/PKG-INFO must be generated
    e.g. by installing project package via pip.
    """

    def __init__(self) -> None:
        """Initialize the project information."""
        super().__init__()
        self.project_metadata = None

        dists = metadata.packages_distributions().get(__package__)
        if dists:
            self.project_name = dists[0]
            self.version = metadata.version(self.project_name)
            self.project_metadata = metadata.metadata(self.project_name)

    @override
    def _get_item_impl(self, project_key: _ProjectKey) -> str:
        if not self.project_metadata:
            raise ValueError("PKG-INFO was not found")

        match project_key:
            case _ProjectKey.NAME:
                return self.project_name
            case _ProjectKey.VERSION:
                return self.version
            case _ProjectKey.DESCRIPTION:
                return self._get_pkg("Summary")
            case _ProjectKey.AUTHOR:
                return self._get_pkg("Author")
            case _ProjectKey.HOMEPAGE_URL:
                try:
                    # get homepage URL from Project-URL: homepage, https://...
                    urls = self._get_pkg("Project-URL")
                    url_dict = {k.strip(): v.strip() for k, v in (item.split(",") for item in urls.splitlines())}
                    return url_dict["homepage"]
                except (ValueError, KeyError):
                    return self._get_pkg("Home-page")
            case _:
                raise ValueError(f"Unknown project key: {project_key}")

    def _get_pkg(self, name: str) -> str:
        if not self.project_metadata:
            raise ValueError("PKG-INFO was not found")

        value = self.project_metadata.get(name)
        if not value:
            raise ValueError(f"Project key: {name} was not found in PKG-INFO")
        return value
