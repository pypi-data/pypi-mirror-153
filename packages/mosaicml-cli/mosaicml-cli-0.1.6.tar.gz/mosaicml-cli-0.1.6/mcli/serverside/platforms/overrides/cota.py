# pylint: disable=duplicate-code

""" The COTA Platform """
from typing import Dict, List

from kubernetes import client

from mcli.serverside.job.mcli_job import MCLIVolume
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.utils.utils_kube_labels import label

rtx3080_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.RTX3080,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.NODE_CLASS: label.mosaic.instance_size_types.MML_NV3080},
    cpus=128,
    cpus_per_gpu=16,
    memory=512,
    memory_per_gpu=64,
    storage=400,
    storage_per_gpu=50,
)
rtx3090_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.RTX3090,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors={label.mosaic.NODE_CLASS: label.mosaic.instance_size_types.MML_NV3090},
    cpus=128,
    cpus_per_gpu=16,
    memory=512,
    memory_per_gpu=64,
    storage=400,
    storage_per_gpu=50,
)
COTA_INSTANCES = LocalPlatformInstances(gpu_configurations=[
    rtx3080_config,
    rtx3090_config,
])


class COTAPlatform(GenericK8sPlatform):
    """ The COTA Platform """

    allowed_instances: PlatformInstances = COTA_INSTANCES

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        volumes.append(
            MCLIVolume(
                volume=client.V1Volume(
                    name='local',
                    host_path=client.V1HostPathVolumeSource(path='/localdisk', type='Directory'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='local',
                    mount_path='/localdisk',
                ),
            ))

        return volumes

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        tolerations = []
        if instance_type.gpu_num > 0:
            tolerations.append({
                'effect': 'PreferNoSchedule',
                'key': label.mosaic.cota.PREFER_GPU_WORKLOADS,
                'operator': 'Equal',
                'value': 'true'
            })

        if instance_type.gpu_num == 8:
            tolerations.append({
                'effect': 'NoSchedule',
                'key': label.mosaic.cota.MULTIGPU_8,
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations
