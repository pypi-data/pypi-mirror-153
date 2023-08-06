"""Implementation of secrets for a Kubernetes backend"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Union

from kubernetes import client

from mcli.models import MCLIPlatform, MCLISecret, SecretType
from mcli.objects.secrets import SECRET_CLASS_MAP
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.utils import utils_kube
from mcli.utils.utils_kube_labels import label

logger = logging.getLogger(__name__)


class PlatformSecretError(Exception):
    """Error in handling platform secrets"""


@dataclass
class PlatformSecret:
    """Platform-dependent secret backed by Kubernetes
    Attributes:
        secret: The secret whose data was imported from Kubernetes
    """

    secret: MCLISecret

    def create(self, namespace: str) -> bool:
        """Create the secret in the current platform
        Args:
            namespace: Namespace in which the secret should be created
        Returns:
            True if secret was created successfully
        """
        return utils_kube.create_secret(self.to_kube_spec(), namespace)

    def delete(self, namespace: str):
        """Delete the secret from the current platform
        Args:
            namespace: Namespace in which the secret exists
        Returns:
            True if secret was deleted successfully
        """
        return utils_kube.delete_secret(self.secret.name, namespace)

    def to_kube_spec(self) -> Dict[str, Any]:
        """Convert the secret to a Kubernetes spec
        Returns:
            Kubernetes spec dictionary
        """
        labels = self.secret.kubernetes_labels or {}
        annotations = self.secret.kubernetes_annotations or {}

        secret = client.V1Secret(type=self.secret.kubernetes_type, data=self.secret.pack())
        secret.metadata = client.V1ObjectMeta(name=self.secret.name, labels=labels, annotations=annotations)
        return client.ApiClient().sanitize_for_serialization(secret)

    @classmethod
    def from_kube_spec(cls: Type[PlatformSecret], spec: Dict[str, Any]) -> PlatformSecret:
        """Import a secret from a Kubernetes spec
        Args:
            spec: Kubernetes spec for an MCLI generated secret
        Raises:
            PlatformSecretError: Raised if the provided secret is not a valid MCLI secret
        Returns:
            A PlatformSecret
        """
        name = spec['metadata']['name']
        logger.debug(f'Attempting to create secret from Kubernetes secret {name}')

        # Get the secret type label
        labels = spec['metadata'].get('labels', {})
        if label.mosaic.SECRET_TYPE not in labels:
            raise PlatformSecretError(f'Secret named {name} is not a valid MCLI secret.')

        try:
            secret_type = SecretType[labels[label.mosaic.SECRET_TYPE].replace('-', '_')]
        except KeyError as e:
            raise PlatformSecretError(
                f'Secret named {name} has an unknown type: {labels[label.mosaic.SECRET_TYPE]}') from e
        logger.debug(f'Secret {name} is of type: {secret_type.value}')

        secret_class = SECRET_CLASS_MAP[secret_type]
        secret = secret_class(name=name, secret_type=secret_type)
        secret.unpack(spec['data'])

        return PlatformSecret(secret=secret)


class SecretManager:
    """Secrets manager for Kubernetes-backed secrets
    Arguments:
        platform: The platform where secrets are stored
    """

    def __init__(self, mcli_platform: MCLIPlatform):
        self.platform = mcli_platform

    def get_secrets(self) -> List[PlatformSecret]:
        """Get a list of secrets on the platform
        Returns:
            List of secrets
        """
        labels: Dict[str, Optional[Union[str, List[str]]]] = {label.mosaic.SECRET_TYPE: None}
        with MCLIPlatform.use(self.platform):
            secrets = utils_kube.list_secrets(self.platform.namespace, labels=labels)
            logger.debug(f'Found {len(secrets["items"])} secrets in platform {self.platform.name}')
        return [PlatformSecret.from_kube_spec(spec) for spec in secrets['items']]

    def add_secrets_to_job(self, kubernetes_job: MCLIK8sJob) -> None:
        """Add all of the platform's secrets to the provided job
        Args:
            job_spec: MCLIK8sJob spec that should be modified by each managed secret
        """
        platform_secrets = self.get_secrets()
        for platform_secret in platform_secrets:
            logger.debug(f'Adding secret {platform_secret.secret.name} from {self.platform.name} to job')
            platform_secret.secret.add_to_job(kubernetes_job)
