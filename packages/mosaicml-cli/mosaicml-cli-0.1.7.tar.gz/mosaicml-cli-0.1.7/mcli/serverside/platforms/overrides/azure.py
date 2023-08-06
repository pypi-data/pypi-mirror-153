# pylint: disable=duplicate-code

""" The Azure Platform """

from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import PlatformInstances


class AzurePlatform(GenericK8sPlatform):
    """ The Azure Platform """

    allowed_instances: PlatformInstances = PlatformInstances()
