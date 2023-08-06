"""Helpers for Weights and Biases integration"""
from dataclasses import dataclass
from typing import Dict, List, Optional

from kubernetes import client

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob
from mcli.sweeps.local_sweep_config import LocalRunConfig


class WandBLabels():
    PROJECT_KEY = 'WANDB_PROJECT'
    ENTITY_KEY = 'WANDB_ENTITY'
    TAGS_KEY = 'WANDB_TAGS'
    RUN_NAME_KEY = 'WANDB_NAME'
    RUN_ID_KEY = 'WANDB_RUN_ID'
    RUN_CONFIG_KEY = 'WANDB_CONFIG_PATHS'
    API_KEY = 'WANDB_API_KEY'
    GROUP_KEY = 'WANDB_RUN_GROUP'
    JOB_TYPE = 'WANDB_JOB_TYPE'


label = WandBLabels()


@dataclass
class MCLIWandBIntegration(MCLIIntegration):
    """WandB Integration
    """
    project: Optional[str] = None
    entity: Optional[str] = None

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        if self.project:
            kubernetes_job.add_env_var(env_var=client.V1EnvVar(
                name=label.PROJECT_KEY,
                value=self.project,
            ))
        if self.entity:
            kubernetes_job.add_env_var(env_var=client.V1EnvVar(
                name=label.ENTITY_KEY,
                value=self.entity,
            ))
        return True


def get_wandb_env_vars(run_config: LocalRunConfig) -> Dict[str, str]:
    """Get environment variables that wandb can use for logging

    Args:
        run_config: The complete run config to be run

    Returns:
        A dictionary of environment variables

    NOTE: This should ultimately modify the run config directly by adding env vars and other details
    TODO: Remove validation guards when LocalRunConfig is fully validated
    """

    envs: Dict[str, str] = {}
    if run_config.project:
        envs[label.PROJECT_KEY] = run_config.project
    if run_config.name:
        name_stem = '-'.join(run_config.name.split('-')[:-1])
        envs[label.RUN_NAME_KEY] = name_stem
    if run_config.algorithm:
        algos: List[str] = run_config.algorithm if isinstance(run_config.algorithm, list) else [run_config.algorithm]
        if algos:
            envs[label.TAGS_KEY] = ','.join(algos)
    return envs
