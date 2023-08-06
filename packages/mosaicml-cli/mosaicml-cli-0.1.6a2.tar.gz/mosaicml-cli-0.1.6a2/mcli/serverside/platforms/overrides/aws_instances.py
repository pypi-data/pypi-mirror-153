""" AWS Available Instances """

from mcli.serverside.job.mcli_k8s_job_typing import MCLIK8sResourceRequirements
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform_instances import CloudPlatformInstances, InstanceTypeLookupData
from mcli.utils.utils_kube_labels import label

a100_g8_instance = InstanceType(
    gpu_type=GPUType.A100_40GB,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=96,
        memory=int(0.9 * 1152),
        storage=80,
    ),
    selectors={
        label.kubernetes_node.INSTANCE_TYPE: label.legacy.AWS_A100_G8,
    },
)

v100_g8_instance = InstanceType(
    gpu_type=GPUType.V100_16GB,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=64,
        memory=int(0.9 * 488),
        storage=80,
    ),
    selectors={
        label.kubernetes_node.INSTANCE_TYPE: label.legacy.AWS_V100_G8,
    },
)

t4_g8_instance = InstanceType(
    gpu_type=GPUType.T4,
    gpu_num=8,
    resource_requirements=MCLIK8sResourceRequirements.from_simple_resources(
        cpus=96,
        memory=int(0.9 * 384),
        storage=80,
    ),
    selectors={
        label.kubernetes_node.INSTANCE_TYPE: label.legacy.AWS_T4_G8,
    },
)

AWS_ALLOWED_INSTANCES = CloudPlatformInstances(instance_type_map={
    InstanceTypeLookupData(GPUType.A100_40GB, 8): a100_g8_instance,
    InstanceTypeLookupData(GPUType.V100_16GB, 8): v100_g8_instance,
    InstanceTypeLookupData(GPUType.T4, 8): t4_g8_instance,
},)
