""" R1Z1 Platform Definition """
from typing import Dict, List

from mcli import config
from mcli.serverside.platforms.gpu_type import GPUType
from mcli.serverside.platforms.instance_type import InstanceType
from mcli.serverside.platforms.platform import GenericK8sPlatform
from mcli.serverside.platforms.platform_instances import (LocalPlatformInstances, PlatformInstanceGPUConfiguration,
                                                          PlatformInstances)
from mcli.utils.utils_kube_labels import label

MAX_CPUS = 60

R1Z1_PRIORITY_CLASS_LABELS: Dict[str, str] = {
    'scavenge': 'mosaicml-internal-research-scavenge-priority',
    'standard': 'mosaicml-internal-research-standard-priority',
    'emergency': 'mosaicml-internal-research-emergency-priority'
}


def _get_selectors() -> Dict[str, str]:
    selectors: Dict[str, str] = {label.mosaic.cloud.INSTANCE_SIZE: label.mosaic.instance_size_types.A100_80G_1}
    mcli_config = config.MCLIConfig.load_config(safe=True)
    if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_MLPERF_NODES):
        selectors[label.mosaic.r1z1.MLPERF_NODE] = 'true'
    return selectors


a100_config = PlatformInstanceGPUConfiguration(
    gpu_type=GPUType.A100_80GB,
    gpu_nums=[1, 2, 4, 8],
    gpu_selectors=_get_selectors(),
    cpus=64,
    cpus_per_gpu=8,
    memory=512,
    memory_per_gpu=64,
    storage=1600,
    storage_per_gpu=200,
)

R1Z1_INSTANCES = LocalPlatformInstances(gpu_configurations=[a100_config])


class R1Z1Platform(GenericK8sPlatform):
    """ R1Z1 Platform Overrides """

    allowed_instances: PlatformInstances = R1Z1_INSTANCES
    priority_class_labels = R1Z1_PRIORITY_CLASS_LABELS  # type: Dict[str, str]
    default_priority_class: str = 'standard'

    def get_tolerations(self, instance_type: InstanceType) -> List[Dict[str, str]]:
        del instance_type
        tolerations = []
        mcli_config = config.MCLIConfig.load_config()
        if mcli_config.feature_enabled(feature=config.FeatureFlag.USE_MLPERF_NODES):
            tolerations.append({
                'effect': 'NoSchedule',
                'key': label.mosaic.r1z1.MLPERF_NODE,
                'operator': 'Equal',
                'value': 'true'
            })

        return tolerations
