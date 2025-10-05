"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
from pathlib import Path
from typing import IO, BinaryIO  # noqa: F401

import tomli

from project_meta.git_info import GitInfo
from project_meta.project_info_pkg import ProjectInfoPkg
from project_meta.project_info_pyproject import ProjectInfoPyProject

# Get the path to the project's root folder
project_root = Path(__file__).parent.parent.parent

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
html_extra_path = ['../_build/htmlcov']  # coverage html report

# https://www.sphinx-doc.org/en/master/usage/extensions/#third-party-extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.autosummary',
    # 'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'sphinx_reports',
    'sphinx.ext.coverage',
    ]
autodoc_typehints = "description"
autodoc_inherit_docstrings = True
autodoc_member_order = 'groupwise'
autoclass_content = "both"
autosummary_generate = True


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

with open(file=project_root / "pyproject.toml", mode="rb") as file_pyproject:  # type: BinaryIO
    pyproject_data = tomli.load(file_pyproject)

# project_info = ProjectInfoPyProject(project_root=project_root, pyproject_data=pyproject_data)
project_info = ProjectInfoPkg()
project = project_info.get_project_name()
description = project_info.get_description()
homepage_url = project_info.get_homepage_url()
author = project_info.get_author()
version = project_info.get_version()
git_info = GitInfo.create(repo_path=project_root)
# The full version, including alpha/beta/rc tags
release = f"{version} (git: {git_info!s})"

# noinspection PyShadowingBuiltins
copyright = f'%Y, {author}'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = 'sphinx_rtd_theme'
# The theme will read from this dictionary
html_context = {
    "display_github": True,  # Integrate GitHub
    "github_user": author,
    "github_repo": project_info.get_project_name(),
    "github_version": git_info.branch,
    "conf_py_path": f"/{Path(__file__).parent.relative_to(project_root)}/",
    }


# -- Options for coverage reports -----------------------------------
tr_report_file = project_root / "docs/tests_results.xml"

report_codecov_packages = {
    "src": {
        "name":        "src",
        "json_report": project_root / "docs/_build/coverage.json",
        "fail_below":  80,
        "levels":      "default",
        },
    }

report_doccov_packages = {
    "src": {
        "name":       "src",
        "directory":  "src",
        "fail_below": 80,
        "levels":     "default",
        },
    }

# Path to the JUnit XML report file
pytest_junit_xml = '../test_results.xml'


# -- Prolog for reStructuredText files --------------------------------------
rst_prolog = f"""
.. |project| replace:: {project_info.get_project_name()}
.. |description| replace:: {description}
.. |author| replace:: {author}
.. |homepage| raw:: html

   <a href="{homepage_url}">GitHub</a>
"""
