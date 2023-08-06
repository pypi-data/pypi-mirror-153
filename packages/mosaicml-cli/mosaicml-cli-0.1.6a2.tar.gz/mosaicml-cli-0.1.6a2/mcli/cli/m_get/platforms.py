"""CLI getter for platforms"""
from dataclasses import dataclass
from typing import Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform
from mcli.utils.utils_logging import FAIL, err_console


@dataclass
class PlatformDisplayItem(MCLIDisplayItem):
    context: str
    namespace: str


class MCLIPlatformDisplay(MCLIGetDisplay):
    """`mcli get platforms` display class
    """

    def __init__(self, platforms: List[MCLIPlatform]):
        self.platforms = platforms

    def __iter__(self) -> Generator[PlatformDisplayItem, None, None]:
        for platform in self.platforms:
            yield PlatformDisplayItem(name=platform.name,
                                      context=platform.kubernetes_context,
                                      namespace=platform.namespace)


def get_platforms(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(f'{FAIL} MCLI not yet initialized. Please run `mcli init` and then `mcli create platform` '
                          'to create your first platform.')
        return 1

    display = MCLIPlatformDisplay(conf.platforms)
    display.print(output)
    return 0
