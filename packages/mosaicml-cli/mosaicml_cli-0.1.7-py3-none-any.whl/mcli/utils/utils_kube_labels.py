""" Label Holders """
from __future__ import annotations

from typing import Any, Dict, List, Optional

from mcli import version
from mcli.utils.utils_string_validation import ensure_rfc_compatibility


def ensure_labelability(item: Any) -> str:
    return ensure_rfc_compatibility(str(item), length=63, special_characters=r'\-\._')


def extract_label_values(all_labels: Dict[str, Any], labels_to_get: List[str], default: str = '-') -> Dict[str, Any]:
    result = {}
    for l in labels_to_get:
        result[l] = all_labels.get(l, default)
    return result


class PrefixMetaclass(type):
    """ Modifies all attributes of a class to append a prefix keyed 'prefix'"""

    def __new__(cls, clsname, bases, attrs):
        assert 'prefix' in attrs
        prefix = attrs['prefix']
        del attrs['prefix']
        prefixed_items = {}
        for k, v in attrs.items():
            if isinstance(v, str):
                if prefix != '':
                    prefixed_items[k] = f'{prefix}/{v}'
                else:
                    prefixed_items[k] = v
            else:
                prefixed_items[k] = v
        return type.__new__(cls, clsname, bases, prefixed_items)


class CotaLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'mosaicml.com'

    PREFER_GPU_WORKLOADS = 'prefer-gpu-workloads'
    MULTIGPU_8 = 'multigpu_8'


class R1Z1LabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'mosaicml.com'

    MLPERF_NODE = 'mlperf'


class GCPLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = ''

    TPUv2 = 'cloud-tpus.google.com/v2'
    TPUv3 = 'cloud-tpus.google.com/v3'
    TPU_ANNOTATION = 'tf-version.cloud-tpus.google.com'
    TF_VERSION = 'pytorch-nightly'


class LegacyInstanceSizeHolder(object, metaclass=PrefixMetaclass):
    prefix = ''

    # gcp-research-01
    GCP_A100_4G = 'a2-highgpu-4g-a100-4'
    GCP_A100_8G = 'a2-highgpu-8g-a100-8'
    GCP_A100_16G = 'a2-megagpu-16g-a100-16'
    GCP_V100_8G = 'n1-highmem-64-v100-8'
    GCP_TPUV3_8G = 'n1-standard-32'
    GCP_TPUV2_8G = 'n1-standard-32'

    #aws-research-01
    AWS_A100_G8 = 'p4d.24xlarge'
    AWS_V100_G8 = 'p3.16xlarge'
    AWS_T4_G8 = 'g4dn.metal'


class MosaicCloudHolder(object, metaclass=PrefixMetaclass):
    prefix = 'mosaicml.cloud'

    INSTANCE_SIZE = 'instance-size'


class MosaicInstanceSizeHolder(object, metaclass=PrefixMetaclass):
    """ Special mosaicml.com/instance-size Label holder

    Stores our cloud defined instance-size labels with no prefix
    to use within our codebase
    """

    prefix = ''

    A100_80G_1 = 'mosaic.a100-80sxm.1'
    A100_80G_2 = 'mosaic.a100-80sxm.2'  # unused for now
    A100_40G_1 = 'mosaic.a100-40sxm.1'
    OCI_G4_8 = 'oci.bm.gpu4.8'
    MML_NV3080 = 'mml-nv3080'
    MML_NV3090 = 'mml-nv3090'

    AWS_A100_G8 = 'aws.p4d.24xlarge'
    AWS_V100_32G_G8 = 'aws.p3dn.24xlarge'
    AWS_V100_16G_G8 = 'aws.p3.16xlarge'
    AWS_T4_G8 = 'aws.g4dn.metal'

    GCP_A100_4G = 'gcp.a2-highgpu-4g'
    GCP_A100_8G = 'gcp.a2-highgpu-8g'
    GCP_A100_16G = 'gcp.a2-megagpu-16g'
    GCP_V100_8G = 'gcp.n1-highmem-64-v100-8'
    GCP_TPUV3_8G = 'gcp.n1-standard-32-tpuv3'


class MosaicBillingHolder(object, metaclass=PrefixMetaclass):
    """
    All mosaicml.com Billing labels required for billback
    """
    prefix = 'mosaicml.com'

    NUM_NODES = 'total-nodes'
    WORKLOAD_UUID = 'workload-uuid'
    CUSTOMER_UUID = 'customer-uuid'
    INSTANCE_SIZE = 'instance-size'
    CLUSTER = 'cluster'

    @classmethod
    def get_billing_labels(
        cls,
        num_nodes: int,
        uuid: str,
        customer: str,
        instance_size: str,
        cluster: str,
    ) -> Dict[str, str]:
        return_items = {
            label.mosaic.billing.NUM_NODES: num_nodes,
            label.mosaic.billing.WORKLOAD_UUID: uuid,
            # TODO: needs to be added when MAPI is live
            label.mosaic.billing.CUSTOMER_UUID: customer,
            label.mosaic.billing.INSTANCE_SIZE: instance_size,
            label.mosaic.billing.CLUSTER: cluster,
        }
        return {k: ensure_labelability(v) for k, v in return_items.items()}


class MCLIVersionHolder(object, metaclass=PrefixMetaclass):
    """
    All MCLI Version Labels to apply
    """
    prefix = 'mosaicml.com'

    # MCLI Version
    MCLI_VERSION = 'mcli_version'
    MCLI_VERSION_MAJOR = 'mcli_version_major'
    MCLI_VERSION_MINOR = 'mcli_version_minor'
    MCLI_VERSION_PATCH = 'mcli_version_patch'
    MCLI_VERSION_EXTRAS = 'mcli_version_extras'

    @classmethod
    def get_version_labels(cls) -> Dict[str, str]:
        return_items = {
            cls.MCLI_VERSION: str(version.__version__),
            cls.MCLI_VERSION_MAJOR: str(version.__version_major__),
            cls.MCLI_VERSION_MINOR: str(version.__version_minor__),
            cls.MCLI_VERSION_PATCH: str(version.__version_patch__),
            cls.MCLI_VERSION_EXTRAS: str(version.__version_extras__),
        }
        return {k: ensure_labelability(v) for k, v in return_items.items()}


class MosaicComputeSelectionLabels(object, metaclass=PrefixMetaclass):
    """ Compute Selectors """
    prefix = 'mosaicml.com'

    LABEL_MCLI_PLATFORM = 'mcli-platform'
    LABEL_GPU_TYPE = 'gpu-type'
    LABEL_GPU_NUM = 'gpu-num'
    LABEL_CPUS = 'cpus'

    @classmethod
    def get_compute_selection_labels(
        cls,
        platform: str,
        gpu_type: str,
        gpu_num: int,
        cpus: Optional[float],
    ) -> Dict[str, str]:
        return_items = {
            cls.LABEL_MCLI_PLATFORM: platform,
            cls.LABEL_GPU_TYPE: gpu_type,
            cls.LABEL_GPU_NUM: str(gpu_num),
            cls.LABEL_CPUS: str(int(cpus) if cpus else 0),
        }
        return {k: ensure_labelability(v) for k, v in return_items.items()}


class MosaicLabelHolder(object, metaclass=PrefixMetaclass):
    """ Base Mosaic Labels """
    prefix = 'mosaicml.com'

    JOB = 'job'
    JOB_TYPE = 'job-type'

    NODE_CLASS = 'node-class'

    LABEL_INSTANCE = 'instance'
    LABEL_INSTANCE_SIZE = 'instance-size'
    LABEL_CLUSTER = 'cluster'

    LABEL_SWEEP = 'sweep'

    # Cloud Labels
    cloud = MosaicCloudHolder

    # Cloud Instance-Size Labels
    instance_size_types = MosaicInstanceSizeHolder

    # Compute Selector Labels
    compute_selectors = MosaicComputeSelectionLabels

    # Cota Labels
    cota = CotaLabelHolder

    # R1Z1 Labels
    r1z1 = R1Z1LabelHolder

    # MCLI Version holder
    version = MCLIVersionHolder

    LAUNCHER_TYPE = 'launcher_type'

    # Secrets
    SECRET_TYPE = 'secret-type'

    # Billing
    billing = MosaicBillingHolder


class KubernetesNodeLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'node.kubernetes.io'

    INSTANCE_TYPE = 'instance-type'


class KubeBatchLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'batch.kubernetes.io'

    POD_RANK = 'job-completion-index'


class NvidiaLabelHolder(object, metaclass=PrefixMetaclass):
    prefix = 'nvidia.com'

    GPU = 'gpu'


class LabelHolder():
    mosaic = MosaicLabelHolder
    nvidia = NvidiaLabelHolder
    gcp = GCPLabelHolder
    kubernetes_node = KubernetesNodeLabelHolder
    kube_batch = KubeBatchLabelHolder
    compute = MosaicComputeSelectionLabels
    legacy = LegacyInstanceSizeHolder


label = LabelHolder
