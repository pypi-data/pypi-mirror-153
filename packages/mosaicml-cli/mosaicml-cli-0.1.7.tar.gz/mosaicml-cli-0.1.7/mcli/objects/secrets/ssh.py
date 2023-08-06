""" SSH Secret Type """
from dataclasses import dataclass

from kubernetes import client

from mcli.objects.secrets import MCLIMountedSecret
from mcli.serverside.job.mcli_k8s_job import MCLIK8sJob


@dataclass
class MCLISSHSecret(MCLIMountedSecret):
    """Secret class for ssh private keys that will be mounted to run pods as a file
    """

    def add_to_job(self, kubernetes_job: MCLIK8sJob, permissions: int = 256) -> bool:
        return super().add_to_job(kubernetes_job=kubernetes_job, permissions=permissions)


@dataclass
class MCLIGitSSHSecret(MCLISSHSecret):
    """Secret class for git-related ssh private keys

    The ssh key will be mounted to a file and the environment variable GIT_SSH_COMMAND
    will be pointed toward it
    """

    def add_to_job(self, kubernetes_job: MCLIK8sJob, permissions: int = 256) -> bool:
        super().add_to_job(kubernetes_job=kubernetes_job, permissions=permissions)
        git_ssh_command_var = client.V1EnvVar(
            name='GIT_SSH_COMMAND',
            value=f'ssh -o StrictHostKeyChecking=no -i {self.mount_path}',
        )
        kubernetes_job.add_env_var(git_ssh_command_var)
        return True
