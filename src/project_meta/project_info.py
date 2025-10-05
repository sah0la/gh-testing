"""Project information such as name, version and description."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from enum import Enum, unique
from typing import ClassVar

logger = logging.getLogger(__name__)


@unique
class _ProjectKey(Enum):
    """Keys for project information items and their default values."""

    NAME = "no-name"
    VERSION = "0.0.0"
    DESCRIPTION = "no-description"
    AUTHOR = "no-author"
    HOMEPAGE_URL = "no-homepage"


class _ProjectInfoBase(ABC):
    """Project information base class with singleton pattern."""

    _instances: ClassVar[dict[type[_ProjectInfoBase], _ProjectInfoBase]] = {}

    def __new__(cls: type[_ProjectInfoBase], *_: object, **__: dict[object, object]) -> _ProjectInfoBase:
        """Singleton pattern to ensure only one instance exists.

        :param *_: Positional arguments.
        :param **__: Keyword arguments.
        :return: Single instance of ProjectInfo.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]

    @abstractmethod
    def _get_item_impl(self, project_key: _ProjectKey) -> str:
        """Get a project item from the implementation.

        :param project_key: Key of the project item to retrieve.
        :return: Project item value.
        :raises ValueError: If the project key is unknown.
        """

    def _get_item(self, project_key: _ProjectKey) -> str:
        """Get a project item with a default fallback.

        :param project_key: Key of the project item to retrieve.
        :return: Project item value or default if not found.
        """
        try:
            value = self._get_item_impl(project_key)
            if value:
                return value
        except ValueError as err:
            logger.error(f"Error retrieving project key {project_key.name}: {err}")
        return project_key.value

    def get_project_name(self) -> str:
        """Get the project name.

        :return: Project name.
        """
        return self._get_item(_ProjectKey.NAME)

    def get_version(self) -> str:
        """Get the project version.

        :return: Project version.
        """
        return self._get_item(_ProjectKey.VERSION)

    def get_description(self) -> str:
        """Get the project description.

        :return: Project description.
        """
        return self._get_item(_ProjectKey.DESCRIPTION)

    def get_author(self) -> str:
        """Get the project author.

        :return: Project author.
        """
        return self._get_item(_ProjectKey.AUTHOR)

    def get_homepage_url(self) -> str:
        """Get the project homepage URL.

        :return: Project homepage URL.
        """
        return self._get_item(_ProjectKey.HOMEPAGE_URL)

    def __repr__(self) -> str:
        """Return a string representation of the project information.

        :return: String with project name and version.
        """
        return f"{self.get_project_name()} v{self.get_version()}"
