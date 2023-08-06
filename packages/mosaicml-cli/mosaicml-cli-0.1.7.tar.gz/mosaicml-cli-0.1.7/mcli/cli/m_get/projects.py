"""CLI getter for projects"""
from dataclasses import dataclass, fields
from datetime import datetime
from typing import Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.models import ProjectConfig
from mcli.objects.projects.info.project_info import get_projects_list
from mcli.utils.utils_logging import FAIL, err_console


@dataclass
class ProjectDisplayItem(MCLIDisplayItem):
    created_by: str
    image: str
    repo: str
    branch: str
    creation_time: datetime
    last_update_time: datetime


class MCLIProjectDisplay(MCLIGetDisplay):
    """`mcli get projects` display class
    """

    def __init__(self, projects: List[ProjectConfig]):
        self.projects = projects

    def __iter__(self) -> Generator[ProjectDisplayItem, None, None]:
        for project in self.projects:
            data = {
                field.name: getattr(project, field.name) for field in fields(ProjectDisplayItem) if field.name != 'name'
            }
            yield ProjectDisplayItem(name=project.project, **data)


def get_projects(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    try:
        MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(f'{FAIL} MCLI not yet initialized. Please run `mcli init` which will walk you through '
                          'creating your first project.')
        return 1

    display = MCLIProjectDisplay(get_projects_list())
    display.print(output)
    return 0
