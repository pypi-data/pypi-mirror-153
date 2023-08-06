""" The MCLI Kubernetes Job Abstraction """
from typing import TYPE_CHECKING, NamedTuple

from kubernetes import client
from kubernetes.client.api_client import ApiClient
from ruamel import yaml

from mcli.serverside.job.mcli_k8s_config_map_typing import MCLIK8sConfigMap
from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sJobTyping

if TYPE_CHECKING:
    from mcli.models.mcli_secret import MCLISecret


class MCLIVolume(NamedTuple):
    volume: client.V1Volume
    volume_mount: client.V1VolumeMount


class MCLIConfigMap(NamedTuple):
    config_map: MCLIK8sConfigMap
    config_volume: MCLIVolume


class MCLIK8sJob(MCLIK8sJobTyping):
    """ MCLI Job K8s Abstraction

    The collection of functions we use internally to modify and make
    changes to a K8s Job


    """

    def add_volume(self, volume: MCLIVolume):
        """Add an Volume to a k8s Job

        Args:
            volume: the MCLIVolume to add (includes volume and mount)
        """
        self.pod_volumes.append(volume.volume)
        self.container_volume_mounts.append(volume.volume_mount)

    def add_env_var(
        self,
        env_var: client.V1EnvVar,
    ):
        """Add an Environment Variable to a k8s Job

        Args:
            env_var: the Environment Variable to add
        """
        self.environment_variables.append(env_var)

    def add_port(
        self,
        port: client.V1ContainerPort,
    ):
        """Open an additional port in the primary container

        Args:
            port (client.V1ContainerPort): Port to open, specified as a V1ContainerPort
        """
        self.ports.append(port)

    def add_secret(self, secret: 'MCLISecret'):
        secret.add_to_job(self)

    def add_command(
        self,
        command: str,
        error_message: str,
        required: bool = True,
    ):
        existing_command = self.container.command_string
        # Temporarily remove set -e
        existing_command = existing_command.replace('set -e;', '')
        if required:
            error_case = f'( echo { error_message } && exit 1 )'
        else:
            error_case = f'( echo { error_message }) '
        new_command = f'set -e; {command} || {error_case};'
        self.container.command_string = new_command + existing_command

    def __str__(self) -> str:

        api = ApiClient()
        data = api.sanitize_for_serialization(self)
        return yaml.dump(data)
