""" The AWS Platform """

from typing import List

from kubernetes import client

from mcli.serverside.job.mcli_k8s_job import MCLIVolume
from mcli.serverside.platforms import PlatformInstances
from mcli.serverside.platforms.overrides.aws_instances import AWS_ALLOWED_INSTANCES
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_pv_setup import CSIVolume, PVDetails, PVSetupMixin

USER_WORKDISK_STORAGE_CAPACITY: str = '5Gi'
CSI_DRIVER: str = 'efs.csi.aws.com'
CSI_VOLUME_HANDLE: str = 'fs-5cb37458'


class AWSPlatform(PVSetupMixin, GenericK8sPlatform):
    """ The AWS Platform """

    allowed_instances: PlatformInstances = AWS_ALLOWED_INSTANCES
    storage_capacity: str = USER_WORKDISK_STORAGE_CAPACITY

    def get_volumes(self) -> List[MCLIVolume]:
        volumes = super().get_volumes()
        volumes.append(
            MCLIVolume(
                volume=client.V1Volume(
                    name='workdisk',
                    persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                        claim_name=f'pvc-aws-{self.mcli_platform.namespace}'),
                ),
                volume_mount=client.V1VolumeMount(
                    name='workdisk',
                    mount_path='/mnt/aws',
                ),
            ))
        return volumes

    @property
    def pv_name(self) -> str:
        return f'pv-aws-{self.mcli_platform.namespace}'

    @property
    def pvc_name(self) -> str:
        return f'pvc-aws-{self.mcli_platform.namespace}'

    def get_volume_details(self) -> PVDetails:
        """Returns the details of the PV spec
        """
        csi_details = CSIVolume(CSI_DRIVER, CSI_VOLUME_HANDLE)
        return PVDetails(csi=csi_details)

    def setup(self) -> bool:
        """Setup the platform for future use.

        Raises:
            PlatformSetupError: Raised if setup failure prevents use of the platform
        """
        if not self.setup_pv(self.mcli_platform):
            return False
        return True
