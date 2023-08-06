""" MCLI Integration APT Packages """
from dataclasses import dataclass
from typing import List

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLIAptPackagesIntegration(MCLIIntegration):
    """APT Package Integration
    """
    packages: List[str]

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        package_list = ' '.join(self.packages)
        kubernetes_job.add_command(
            f'apt-get update -y && apt-get install -y {package_list}',
            error_message=f'Failed to apt install packages: {package_list}',
            required=True,
        )
        return True
