""" Project Information """
from __future__ import annotations

from pathlib import Path
from typing import List, Set

from mcli import config
from mcli.models import ProjectConfig
from mcli.utils.utils_file import list_yamls


def get_projects_directory() -> Path:
    return config.MCLI_PROJECTS_DIR


def get_projects_list() -> List[ProjectConfig]:
    project_dir = get_projects_directory()
    project_files = list_yamls(project_dir)
    found_projects = []
    for project_file in project_files:
        try:
            project = ProjectConfig.load(path=project_file)
            found_projects.append(project)
        except Exception as e:  # pylint: disable=broad-except
            print(f'Unable to create ProjectConfig: \n{e}')
    return found_projects


def get_all_used_images() -> Set[str]:
    # all_projects = get_projects_list()
    # TODO: Fix images
    return {'image'}
