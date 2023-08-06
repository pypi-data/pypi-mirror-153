""" R6Z3 Platform Definition """
from typing import Optional

from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.utils.utils_kube_labels import label

a100_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[8, 16, 24, 32],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.OCI_G4_8},
    cpus=64,
    cpus_per_gpu=8,
    memory=2048,
    memory_per_gpu=256,
    storage=1600,
    storage_per_gpu=200,
)

R6Z3_INSTANCES = LocalPlatformInstances(gpu_configurations=[a100_config])


class R6Z3Platform(GenericK8sPlatform):
    """ R6Z3 Platform Overrides """

    allowed_instances: PlatformInstances = R6Z3_INSTANCES

    pod_group_scheduler: Optional[str] = 'scheduler-plugins-scheduler'
