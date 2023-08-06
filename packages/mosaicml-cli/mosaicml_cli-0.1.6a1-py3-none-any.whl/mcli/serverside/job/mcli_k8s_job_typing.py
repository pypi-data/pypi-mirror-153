""" Provides typing for Lazy Loaded MCLIK8sJob Class """
from __future__ import annotations

from typing import Dict, List, Type, cast

from kubernetes import client

from mcli.serverside.job.mcli_k8s_resource_requirements_typing import MCLIK8sResourceRequirements


class MCLIK8sContainer(client.V1Container):
    """ Provides typing for Lazy Loaded V1Container

    Makes properties and nested properties lazy loaded for convenience
    """

    @classmethod
    def empty(cls: Type[MCLIK8sContainer], name: str) -> MCLIK8sContainer:
        container = cls(name=name)
        return container

    @property
    def command_string(self) -> str:
        assert len(self.args) == 1, 'MCLI Commands can have only a single arg'
        return self.args[0]

    @command_string.setter
    def command_string(self, command: str):
        self.args[0] = command

    @property
    def args(self) -> List[str]:
        if self._args is None:
            self._args = ['']
        return self._args

    @args.setter
    def args(self, args):
        self._args = args

    @property
    def resources(self) -> MCLIK8sResourceRequirements:
        if self._resources is None:
            self._resources = MCLIK8sResourceRequirements()
        return self._resources

    @resources.setter
    def resources(self, resources: MCLIK8sResourceRequirements):
        self._resources = resources


class MCLIK8sPodSpec(client.V1PodSpec):
    """ Provides typing for Lazy Loaded V1PodSpec

    Makes properties and nested properties lazy loaded for convenience
    """

    @classmethod
    def empty(cls: Type[MCLIK8sPodSpec], name: str) -> MCLIK8sPodSpec:
        container = MCLIK8sContainer.empty(name=name)
        pod_spec = cls(containers=[container])
        return pod_spec

    @property
    def container(self) -> MCLIK8sContainer:
        containers = cast(List[MCLIK8sContainer], self.containers)
        if len(containers) != 1:
            raise ValueError('MCLIK8sJobs can only have 1 container')
        return containers[0]

    @property
    def node_selector(self) -> Dict[str, str]:
        if self._node_selector is None:
            self._node_selector = {}
        return self._node_selector

    @node_selector.setter
    def node_selector(self, node_selector: Dict[str, str]):
        self._node_selector = node_selector


class MCLIK8sPodTemplateSpec(client.V1PodTemplateSpec):
    """ Provides typing for Lazy Loaded V1PodTemplateSpec

    Makes properties and nested properties lazy loaded for convenience
    """

    @classmethod
    def empty(cls: Type[MCLIK8sPodTemplateSpec], name: str) -> MCLIK8sPodTemplateSpec:
        pod_spec = MCLIK8sPodSpec.empty(name=name)
        pod_template_spec = cls(spec=pod_spec)
        return pod_template_spec

    @property
    def metadata(self) -> client.V1ObjectMeta:
        if self._metadata is None:
            self._metadata = client.V1ObjectMeta()
        return self._metadata

    @property
    def spec(self) -> MCLIK8sPodSpec:
        return cast(MCLIK8sPodSpec, self._spec)

    @spec.setter
    def spec(self, spec: MCLIK8sPodSpec):
        assert isinstance(spec, MCLIK8sPodSpec), 'Please use the MCLI Typed k8s object'
        self._spec = spec

    @metadata.setter
    def metadata(self, metadata: client.V1ObjectMeta) -> None:
        self._metadata = metadata


class MCLIK8sPod(client.V1Pod):
    """ Provides typing for Lazy Loaded V1Pod

    Makes properties and nested properties lazy loaded for convenience
    """

    @classmethod
    def empty(cls: Type[MCLIK8sPod], name: str) -> MCLIK8sPod:
        pod_spec = MCLIK8sPodSpec.empty(name=name)
        pod = cls(spec=pod_spec)
        return pod

    @property
    def metadata(self) -> client.V1ObjectMeta:
        if self._metadata is None:
            self._metadata = client.V1ObjectMeta()
        return self._metadata

    @property
    def spec(self) -> MCLIK8sPodSpec:
        return cast(MCLIK8sPodSpec, self._spec)

    @spec.setter
    def spec(self, spec: MCLIK8sPodSpec):
        assert isinstance(spec, MCLIK8sPodSpec), 'Please use the MCLI Typed k8s object'
        self._spec = spec

    @metadata.setter
    def metadata(self, metadata: client.V1ObjectMeta) -> None:
        self._metadata = metadata

    @property
    def status(self) -> client.V1PodStatus:
        if self._status is None:
            self._status = client.V1PodStatus()
        return self._status

    @status.setter
    def status(self, status: client.V1PodStatus) -> None:
        self._status = status


class MCLIK8sJobTyping(client.V1Job):
    """ Provides typing for Lazy Loaded V1Job

    Makes properties and nested properties lazy loaded for convenience
    """

    @classmethod
    def empty(cls: Type[MCLIK8sJobTyping], name: str) -> MCLIK8sJobTyping:
        job = cls()
        pod_template_spec = MCLIK8sPodTemplateSpec.empty(name=name)
        job.spec = client.V1JobSpec(template=pod_template_spec)
        job.spec.template = pod_template_spec
        return job

    @property
    def api_version(self) -> str:  # type: ignore
        if super().api_version:
            return cast(str, super().api_version)
        return 'batch/v1'

    @property
    def kind(self) -> str:  # type: ignore
        if super().kind:
            return cast(str, super().kind)
        return 'Job'

    @property
    def metadata(self) -> client.V1ObjectMeta:
        if self._metadata is None:
            self._metadata = client.V1ObjectMeta()
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: client.V1ObjectMeta) -> None:
        self._metadata = metadata

    @property
    def status(self) -> client.V1JobStatus:
        if self._status is None:
            self._status = client.V1JobStatus()
        return self._status

    @status.setter
    def status(self, status: client.V1JobStatus) -> None:
        self._status = status

    @property
    def container(self) -> MCLIK8sContainer:
        return self.pod_spec.container

    @property
    def resources(self) -> MCLIK8sResourceRequirements:
        return self.container.resources

    @property
    def spec(self) -> client.V1JobSpec:
        return self._spec

    @spec.setter
    def spec(self, spec: client.V1JobSpec) -> None:
        self._spec = spec

    @property
    def pod_template_spec(self) -> MCLIK8sPodTemplateSpec:
        return cast(MCLIK8sPodTemplateSpec, self.spec.template)

    @property
    def pod_spec(self) -> MCLIK8sPodSpec:
        return self.pod_template_spec.spec

    @pod_spec.setter
    def pod_spec(self, pod_spec) -> None:
        pod_template_spec = cast(client.V1PodTemplateSpec, self.spec.template)
        pod_template_spec.spec = pod_spec

    @property
    def pod_volumes(self) -> List[client.V1Volume]:
        if self.pod_spec.volumes is None:
            self.pod_spec.volumes = []
        return self.pod_spec.volumes

    @pod_volumes.setter
    def pod_volumes(self, pod_volume: List[client.V1Volume]):
        self.pod_spec.volumes = pod_volume

    @property
    def container_volume_mounts(self) -> List[client.V1VolumeMount]:
        if self.container.volume_mounts is None:
            self.container.volume_mounts = []
        return self.container.volume_mounts

    @container_volume_mounts.setter
    def container_volume_mounts(self, container_volume_mount: List[client.V1VolumeMount]):
        self.container.volume_mounts = container_volume_mount

    @property
    def environment_variables(self) -> List[client.V1EnvVar]:
        if self.container.env is None:
            self.container.env = []
        return self.container.env

    @environment_variables.setter
    def environment_variables(self, environment_variables: List[client.V1EnvVar]):
        self.container.env = environment_variables

    @property
    def ports(self) -> List[client.V1ContainerPort]:
        if self.container.ports is None:
            self.container.ports = []
        return self.container.ports

    @ports.setter
    def ports(self, ports: List[client.V1ContainerPort]):
        self.container.ports = ports
