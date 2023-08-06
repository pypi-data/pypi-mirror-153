""" Reexporting All Secrets """
# pylint: disable=useless-import-alias

from typing import Dict, Type

from mcli.models import MCLISecret, SecretType
from mcli.models.mcli_secret import MCLIGenericSecret
from mcli.objects.secrets.docker_registry import MCLIDockerRegistrySecret
from mcli.objects.secrets.env_var import MCLIEnvVarSecret
from mcli.objects.secrets.mounted import MCLIMountedSecret
from mcli.objects.secrets.s3_credentials import MCLIS3Secret
from mcli.objects.secrets.ssh import MCLIGitSSHSecret, MCLISSHSecret

SECRET_CLASS_MAP: Dict[SecretType, Type[MCLISecret]] = {
    SecretType.docker_registry: MCLIDockerRegistrySecret,
    SecretType.generic: MCLIGenericSecret,
    SecretType.environment: MCLIEnvVarSecret,
    SecretType.mounted: MCLIMountedSecret,
    SecretType.ssh: MCLISSHSecret,
    SecretType.git: MCLIGitSSHSecret,
    SecretType.s3_credentials: MCLIS3Secret,
}
