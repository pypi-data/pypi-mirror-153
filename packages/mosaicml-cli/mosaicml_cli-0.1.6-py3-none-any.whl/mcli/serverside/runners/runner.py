""" Generic Runner for MCLI K8s Jobs """
from typing import Any, Dict, List, Optional, cast

from kubernetes import client
from kubernetes.client.api_client import ApiClient

from mcli.config import MCLIConfig
from mcli.serverside.job.mcli_job import MCLIJob, MCLIJobType, MCLIK8sJob
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.utils.utils_kube import get_cluster_version, merge_V1ObjectMeta, use_context
from mcli.utils.utils_kube_labels import label
from mcli.version import Version


def title_to_snake(s):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')


class Runner:
    """ Generic Runner for MCLI K8s Jobs """

    def configure_job_global_environment(self, job_spec: MCLIK8sJob):
        conf = MCLIConfig.load_config(safe=True)
        for env_item in conf.environment_variables:
            job_spec.add_env_var(client.V1EnvVar(name=env_item.key, value=env_item.value))

    def configure_job_client_metadata(self, job_type: MCLIJobType) -> client.V1ObjectMeta:
        """Add mcli client-sided metadata
        """
        labels = {label.mosaic.JOB_TYPE: job_type.value}
        return client.V1ObjectMeta(labels=labels)

    def get_specs(
        self,
        job: MCLIJob,
        priority_class: Optional[str] = None,
        experimental_flags: Optional[List[ExperimentalFlag]] = None,
        job_type: MCLIJobType = MCLIJobType.RUN,
    ) -> List[Dict[str, Any]]:
        """Get Kubernetes object specs to create

        Args:
            job: MCLI job to run
            instance: Instance on which to run
            priority_class: Priority at which the run should be submitted. Defaults to None,
                which does not set the run's priority.
            experimental_flags: A list of experimental flags to enable,
                if the instance allows them. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of Kubernetes specs to create
        """
        k8s_platform = job.platform

        kubernetes_job = job.get_kubernetes_job(k8s_platform)
        shared_metadata = job.get_shared_metadata()

        config_map, cm_volume = job.get_config_map()
        kubernetes_job.add_volume(cm_volume)

        k8s_platform.prepare_kubernetes_job_for_platform(
            kubernetes_job=kubernetes_job,
            instance_type=job.instance_type,
            priority_class=priority_class,
            experimental_flags=experimental_flags,
        )
        shared_metadata = merge_V1ObjectMeta(shared_metadata, self.configure_job_client_metadata(job_type))
        kubernetes_job.metadata = merge_V1ObjectMeta(shared_metadata, kubernetes_job.metadata)
        pod_template_spec = kubernetes_job.pod_template_spec
        pod_template_spec.metadata = merge_V1ObjectMeta(shared_metadata, pod_template_spec.metadata)

        config_map.metadata = merge_V1ObjectMeta(shared_metadata, config_map.metadata)

        service = job.get_service()
        if service is not None:
            service.metadata = merge_V1ObjectMeta(shared_metadata, service.metadata)

        # TODO: Typing for PodGroups
        pod_group = job.get_pod_group(k8s_platform)
        if pod_group is not None:
            if pod_group['metadata']:
                pod_group['metadata'] = merge_V1ObjectMeta(shared_metadata, pod_group['metadata'])
            else:
                pod_group['metadata'] = shared_metadata

        k8s_objects = [x for x in [pod_group, config_map, kubernetes_job, service] if x is not None]
        api = ApiClient()
        return cast(List[Dict[str, Any]], [api.sanitize_for_serialization(x) for x in k8s_objects])

    def submit(
        self,
        job: MCLIJob,
        priority_class: Optional[str] = None,
        experimental_flags: Optional[List[ExperimentalFlag]] = None,
        job_type: MCLIJobType = MCLIJobType.RUN,
    ):
        """Submit a job to run

        Args:
            job: MCLI job to run
            priority_class: Priority at which the run should be submitted. Defaults to None,
                which does not set the run's priority.
            experimental_flags: A list of experimental flags to enable,
                if the instance allows them. Defaults to None.

        Returns:
            List[Dict[str, Any]]: List of Kubernetes specs to create
        """
        specs = self.get_specs(
            job=job,
            priority_class=priority_class,
            experimental_flags=experimental_flags,
            job_type=job_type,
        )

        with use_context(context=job.platform.kubernetes_context):

            # Verify multi-node job is only running on Kubernetes version >= 1.22
            if job.instance_type.num_nodes > 1:
                required_version = Version(1, 22, 0)
                server_version = get_cluster_version()
                if server_version < required_version:
                    raise RuntimeError(
                        f'Platform {job.platform.mcli_platform.name} is not configured for multi-node runs.')

            for spec in specs:
                # Get API client from the object api version string.
                # E.g. "batch/v1" => client.BatchV1Api()

                api_version_str = spec['apiVersion']
                api_version_fragments = api_version_str.split('/')
                if len(api_version_fragments) > 1:
                    api_name, api_version = api_version_fragments[:2]
                else:
                    api_name, api_version = ('Core', api_version_fragments[0])
                client_api_name = api_name.capitalize() + api_version.upper() + 'Api'

                if hasattr(client, client_api_name):
                    api = getattr(client, client_api_name)()
                    # Find corresponding create method from Kind string.
                    # e.g. "Job" => api.create_namespaced_job(...)
                    kind_str = spec['kind']
                    create = getattr(api, f'create_namespaced_{title_to_snake(kind_str)}')
                    create(job.platform.namespace, body=spec)
                else:
                    api = client.CustomObjectsApi()
                    api.create_namespaced_custom_object(group=api_name,
                                                        version=api_version,
                                                        namespace=job.platform.namespace,
                                                        plural='podgroups',
                                                        body=spec)
