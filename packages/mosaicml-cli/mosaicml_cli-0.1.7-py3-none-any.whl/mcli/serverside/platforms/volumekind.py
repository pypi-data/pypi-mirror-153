# pylint: disable=duplicate-code

""" A python VolumeKind Abstraction """
from enum import Enum


class VolumeKind(Enum):
    """ A python VolumeKind Abstraction """
    PERSISTENT_VOLUME_CLAIM = 1
    HOST_PATH_VOLUME_SOURCE = 2
    EMPTY_DIR_VOLUME_SOURCE = 3
    SECRET_VOLUME_SOURCE = 4
    CONFIG_MAP = 5
