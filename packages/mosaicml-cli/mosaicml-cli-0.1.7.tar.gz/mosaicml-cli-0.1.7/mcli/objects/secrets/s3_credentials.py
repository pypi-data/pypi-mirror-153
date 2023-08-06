""" S3 Credentials Secret Type """
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Set

from kubernetes import client

from mcli.models import MCLISecret
from mcli.models.mcli_secret import SECRET_MOUNT_PATH_PARENT
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob, MCLIVolume


@dataclass
class MCLIS3Secret(MCLISecret):
    """Secret class for AWS credentials
    """
    mount_directory: Optional[str] = None
    credentials: Optional[str] = None
    config: Optional[str] = None

    def __post_init__(self):
        if self.mount_directory is None:
            self.mount_directory = str(SECRET_MOUNT_PATH_PARENT / self.name)

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['credentials', 'config']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields + ['mount_directory'])

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        assert self.mount_directory is not None
        path = Path(self.mount_directory)
        secret_volume = client.V1Volume(
            name=self.name,
            secret=client.V1SecretVolumeSource(
                secret_name=self.name,
                items=[
                    client.V1KeyToPath(key='credentials', path='credentials'),
                    client.V1KeyToPath(key='config', path='config'),
                ],
            ),
        )
        secret_mount = client.V1VolumeMount(
            name=self.name,
            mount_path=str(path),
            read_only=True,
        )
        mcli_volume = MCLIVolume(volume=secret_volume, volume_mount=secret_mount)
        kubernetes_job.add_volume(mcli_volume)

        # Add config and credential env vars
        config_var = client.V1EnvVar(
            name='AWS_CONFIG_FILE',
            value=f'{self.mount_directory}/config',
        )
        kubernetes_job.add_env_var(config_var)
        cred_var = client.V1EnvVar(
            name='AWS_SHARED_CREDENTIALS_FILE',
            value=f'{self.mount_directory}/credentials',
        )
        kubernetes_job.add_env_var(cred_var)
        return True
