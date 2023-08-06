""" Microk8s Platform Definition """
from typing import Dict, List

from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import PlatformInstances


class Microk8sPlatformInstances(PlatformInstances):
    """ Only one allowed instance type: no GPUs """

    available_instances: Dict[GPUType, List[int]] = {GPUType.NONE: [0]}


class Microk8sPlatform(GenericK8sPlatform):
    """ Microk8s Platform Overrides """

    allowed_instances: PlatformInstances = Microk8sPlatformInstances()
