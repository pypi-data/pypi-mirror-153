"""Experimental platform features"""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from mcli.serverside.job.mcli_job import MCLIK8sJob
    from mcli.serverside.platforms.instance_type import InstanceType
    from mcli.serverside.platforms.platform_instances import PlatformInstances


class ExperimentalFlag(Enum):
    """ Enum class for experimental Flags """
    RDMA = 'rdma'

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def permitted() -> List[ExperimentalFlag]:
        """Get all experimental flags available to a user

        Returns:
            List[ExperimentalFlag]: List of available experimental flags
        """
        return list(ExperimentalFlag)


class PlatformExperimental():
    """Handles applying platform-specific experimental flags to a job"""

    def apply_experimental_flags(
        self,
        kubernetes_job: MCLIK8sJob,
        platform_instance: PlatformInstances,
        instance_type: InstanceType,
        experimental_flags: Optional[List[ExperimentalFlag]] = None,
    ) -> None:
        """Apply experimental flags requested by the user

        Args:
            job_spec (MCLIK8sJob): Job to apply flags to
            platform_instances (InstanceType): Instance to check for flag support
            instance_type (InstanceType): Instance to check for flag support
            experimental_flags (Optional[List[ExperimentalFlag]]):
                List of flags requested by the user. Defaults to None.
        """
        del kubernetes_job
        if not experimental_flags:
            return

        for flag in experimental_flags:
            if flag not in ExperimentalFlag.permitted():
                raise PermissionError(f'User not permitted to use experimental flag {flag}')

            flag_allowed = platform_instance.allowed_experimental_flags(
                instance_type=instance_type,
                experimental_flag=flag,
            )
            if flag_allowed:
                pass
                # So far no flags do anything
            else:
                if not flag_allowed:
                    raise ValueError(f'Experimental flag {str(flag)} not allowed for instance {instance_type}. ')
                else:
                    raise ValueError(
                        f'Unsupported experimental flag: {str(flag)}. Valid options '
                        f'are {ExperimentalFlag.permitted()}, though not all are supported on all platforms.')
