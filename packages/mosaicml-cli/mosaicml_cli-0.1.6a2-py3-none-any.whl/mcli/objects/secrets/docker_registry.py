""" Docker Registry Secret Type """
import json
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Set

from kubernetes import client

from mcli.models import MCLISecret
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.utils.utils_kube import base64_decode, base64_encode


@dataclass
class MCLIDockerRegistrySecret(MCLISecret):
    """Secret class for docker image pull secrets
    """
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    server: Optional[str] = None

    @property
    def disk_skipped_fields(self) -> List[str]:
        return ['username', 'password', 'email', 'server']

    @property
    def required_packing_fields(self) -> Set[str]:
        return set(self.disk_skipped_fields) - {'email'}

    @property
    def kubernetes_type(self) -> str:
        """The corresponding Kubernetes secret type for this class of secrets
        """
        return 'kubernetes.io/dockerconfigjson'

    def unpack(self, data: Dict[str, str]):
        """Unpack the Kubernetes secret `data` field to fill in required secret values

        Args:
            data: _description_
        """
        if '.dockerconfigjson' in data:
            values: Dict[str, Any] = json.loads(base64_decode(data['.dockerconfigjson']))
            values = values['auths']
            missing = set()

            docker_servers = values.keys()
            if len(docker_servers) != 1:
                raise KeyError(f'{len(docker_servers)} Docker Servers detected.'
                               ' Must have only one specified')
            self.server = list(docker_servers)[0]
            values = values[self.server]

            for required in ('username', 'password'):
                if required not in values:
                    missing.add(required)
            if missing:
                raise KeyError(f'Incompatible secret: Docker secret is missing the following keys: {missing}')

            self.username = values['username']
            self.password = values['password']
            self.email = values.get('email', None)
        else:
            raise KeyError('Docker secret must have the key ".dockerconfigjson"')

    def pack(self) -> Dict[str, str]:
        filled_fields = asdict(self)
        missing_fields = self.required_packing_fields - filled_fields.keys()
        if missing_fields:
            raise ValueError('Missing required field(s) to unpack Secret: '
                             f'{",".join(missing_fields)}')

        registry_data = {
            'username': self.username,
            'password': self.password,
            'auth': base64_encode(f'{self.username}:{self.password}'),
        }
        if self.email:
            registry_data['email'] = self.email

        data = {'auths': {self.server: registry_data}}
        json_str = json.dumps(data)
        return {'.dockerconfigjson': base64_encode(json_str)}

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        if kubernetes_job.pod_spec.image_pull_secrets and isinstance(kubernetes_job.pod_spec.image_pull_secrets, list):
            kubernetes_job.pod_spec.image_pull_secrets.append(client.V1LocalObjectReference(name=self.name))
        else:
            kubernetes_job.pod_spec.image_pull_secrets = [client.V1LocalObjectReference(name=self.name)]
        return True
