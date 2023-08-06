""" MCLI Integration APT Packages """
from dataclasses import dataclass
from typing import List

from mcli.models import MCLIIntegration
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLIPipPackagesIntegration(MCLIIntegration):
    """APT Package Integration
    """
    packages: List[str]
    upgrade: bool = False

    def add_to_job(self, kubernetes_job: MCLIK8sJob) -> bool:
        package_list = ' '.join(self.packages)
        arguments: List[str] = [package_list]
        if self.upgrade:
            arguments.insert(0, '--upgrade')
        cmd = f'pip install {" ".join(arguments)}'
        kubernetes_job.add_command(
            cmd,
            error_message=f'Failed to pip install packages: {package_list}',
            required=True,
        )
        return True
