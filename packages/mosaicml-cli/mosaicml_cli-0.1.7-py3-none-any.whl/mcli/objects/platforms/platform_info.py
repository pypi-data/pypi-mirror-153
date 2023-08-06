"""Helpers for platform info"""
from typing import List

from mcli.config import MCLIConfig
from mcli.models import MCLIPlatform


def get_platform_list() -> List[MCLIPlatform]:
    conf = MCLIConfig.load_config()
    return conf.platforms
