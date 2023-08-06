""" The InstanceType Abstraction for different instance configs """

from __future__ import annotations

from dataclasses import dataclass, field
from math import ceil
from typing import TYPE_CHECKING, Dict, List, Optional

from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sResourceRequirements
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.utils.utils_kube_labels import label

if TYPE_CHECKING:
    from mcli.serverside.platforms.experimental import ExperimentalFlag


@dataclass
class InstanceType():
    """ The InstanceType Abstraction that has all necessary information to update MCLIK8sJobs"""

    gpu_type: GPUType
    gpu_num: int

    resource_requirements: MCLIK8sResourceRequirements = MCLIK8sResourceRequirements()

    description: Optional[str] = None

    selectors: Dict[str, str] = field(default_factory=dict)

    priority_class: Optional[str] = ''
    experimental: List[ExperimentalFlag] = field(default_factory=list)

    _local_world_size: Optional[int] = None

    def __post_init__(self):

        if self.gpu_type == GPUType.TPUv3:
            self.resource_requirements.tpu_v3s = self.local_world_size
        elif self.gpu_type == GPUType.TPUv2:
            self.resource_requirements.tpu_v2s = self.local_world_size
        elif self.gpu_type != GPUType.NONE:
            self.resource_requirements.gpus = self.local_world_size

    @property
    def local_world_size(self) -> int:
        if self._local_world_size is not None:
            return self._local_world_size
        return min(self.gpu_num, 8)

    @local_world_size.setter
    def local_world_size(self, local_world_size: int):
        """ Usually local_world_size will be gpu_num or 8

        This setter exists for instances with rare different gpu numbers eg. 16/node
        """
        self._local_world_size = local_world_size

    @property
    def num_nodes(self) -> int:
        if self.gpu_num == 0:
            return 1
        return max(1, ceil(self.gpu_num / self.local_world_size))

    @property
    def cpus(self) -> float:
        return self.resource_requirements.cpus

    @property
    def memory(self) -> float:
        return self.resource_requirements.memory

    @property
    def storage(self) -> float:
        return self.resource_requirements.ephemeral_storage

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        # Update Selectors
        kubernetes_job.pod_spec.node_selector.update(self.selectors)

        # Update Resource Requirements
        kubernetes_job.pod_spec.container.resources = self.resource_requirements

        return True

    @property
    def instance_size(self) -> str:
        """Pulls the instance_size label from the InstanceType selector
        """
        # TODO: Eventually when INSTANCE_SIZE is required for all instances
        #      it should be a first class field that is required in the InstanceType object
        return self.selectors.get(label.mosaic.cloud.INSTANCE_SIZE, 'unknown')

    def __str__(self) -> str:
        return f'InstanceType: gpus: {self.gpu_type.value}{"x" + str( self.gpu_num ) if self.gpu_num else ""}'
