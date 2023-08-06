""" Creates an EnvVar Secret """
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set, Type

from kubernetes import client

from mcli.models import MCLIGenericSecret, SecretType
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLIEnvVarSecret(MCLIGenericSecret):
    """Secret class for generic secrets that will be added as environment variables
    """
    key: Optional[str] = None

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields + ['key'])

    @classmethod
    def from_generic_secret(
        cls: Type[MCLIEnvVarSecret],
        generic_secret: MCLIGenericSecret,
        key: str,
    ) -> MCLIEnvVarSecret:
        return cls(
            name=generic_secret.name,
            value=generic_secret.value,
            secret_type=SecretType.environment,
            key=key,
        )

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        secret_env = client.V1EnvVar(
            name=self.key,
            value_from=client.V1EnvVarSource(secret_key_ref=client.V1SecretKeySelector(
                name=self.name,
                key='value',
                optional=False,
            ),),
        )

        kubernetes_job.add_env_var(secret_env)
        return True
