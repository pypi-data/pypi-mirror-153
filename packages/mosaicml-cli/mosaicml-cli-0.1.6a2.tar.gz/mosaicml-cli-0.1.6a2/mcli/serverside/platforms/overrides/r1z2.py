# pylint: disable=duplicate-code

""" R1Z2 Platform Definition """

from typing import List

from kubernetes import client

from mcli.models import MCLIPlatform
from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.serverside.platforms.platform_pv_setup import NFSVolume, PVDetails, PVSetupMixin
from mcli.utils.utils_kube_labels import label

USER_WORKDISK_SERVER = '10.100.1.241'
USER_WORKDISK_PATH = '/mnt/tank0/r1z2'
USER_WORKDISK_STORAGE_CAPACITY = '10Gi'

a100_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.A100_40GB,
    gpu_nums=[1, 2, 4],
    gpu_selectors={label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.A100_40G_1},
    cpus=64,
    cpus_per_gpu=8,
    memory=512,
    memory_per_gpu=64,
    storage=1600,
    storage_per_gpu=200,
)
R1Z2_INSTANCES = LocalPlatformInstances(
    # Enable CPU Interactive
    available_instances={GPUType.NONE: [0]},
    gpu_configurations=[a100_config],
)


class R1Z2Platform(PVSetupMixin, GenericK8sPlatform):
    """ R1Z2 Platform Overrides """

    allowed_instances: PlatformInstances = R1Z2_INSTANCES
    storage_capacity: str = USER_WORKDISK_STORAGE_CAPACITY

    def __init__(self, mcli_platform: MCLIPlatform) -> None:
        super().__init__(mcli_platform)
        self.interactive = True

    @property
    def pv_name(self) -> str:
        return f'workdisk-{self.namespace}'

    @property
    def pvc_name(self) -> str:
        return f'workdisk-{self.namespace}'

    def get_volume_details(self) -> PVDetails:
        """Returns the details of the PV spec
        """
        nfs_details = NFSVolume(USER_WORKDISK_PATH, USER_WORKDISK_SERVER)
        return PVDetails(nfs=nfs_details)

    def get_volumes(self) -> List[MCLIVolume]:
        """Get the volumes for the R1Z2 platform, including the user's workdisk volume
        """
        volumes = super().get_volumes()

        # Get workdisk mount
        volume = client.V1Volume(
            name='workdisk',
            persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                claim_name=self.pvc_name,
                read_only=False,
            ),
        )
        mount = client.V1VolumeMount(name='workdisk', mount_path='/workdisk')
        volumes.append(MCLIVolume(volume=volume, volume_mount=mount))

        return volumes

    def setup(self) -> bool:
        """Setup the platform for future use.

        Raises:
            PlatformSetupError: Raised if setup failure prevents use of the platform
        """
        if not self.setup_pv(self.mcli_platform):
            return False
        return True
