"""Utilities for interpreting pod status"""
from __future__ import annotations

import functools
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Type, TypeVar

from kubernetes import client

from mcli.utils.utils_kube import deserialize


@functools.total_ordering
class PodState(Enum):
    """Enum for possible pod states
    """
    PENDING = 'PENDING'
    SCHEDULED = 'SCHEDULED'
    QUEUED = 'QUEUED'
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED_PULL = 'FAILED_PULL'
    FAILED = 'FAILED'
    UNKNOWN = 'UNKNOWN'

    @property
    def order(self) -> List[PodState]:
        """Order of pod states, from latest to earliest
        """
        return [
            PodState.FAILED,
            PodState.FAILED_PULL,
            PodState.COMPLETED,
            PodState.RUNNING,
            PodState.STARTING,
            PodState.SCHEDULED,
            PodState.QUEUED,
            PodState.PENDING,
            PodState.UNKNOWN,
        ]

    def __lt__(self, other: PodState):
        if not isinstance(other, PodState):
            raise TypeError(f'Cannot compare order of ``PodState`` and {type(other)}')
        return self.order.index(self) > self.order.index(other)

    def before(self, other: PodState, inclusive: bool = False) -> bool:
        """Returns True if this state usually comes "before" the other

        Args:
            other: Another PodState
            inclusive: If True, == evaluates to True. Default False.

        Returns:
            True of this state is "before" the other

        Examples:
        > PodState.RUNNING.before(PodState.COMPLETED)
        True

        > PodState.PENDING.before(PodState.RUNNING)
        True
        """
        return (self < other) or (inclusive and self == other)

    def after(self, other: PodState, inclusive: bool = False) -> bool:
        """Returns True if this state usually comes "after" the other

        Args:
            other: Another PodState
            inclusive: If True, == evaluates to True. Default False.

        Returns:
            True of this state is "after" the other

        Examples:
        > PodState.RUNNING.before(PodState.COMPLETED)
        True

        > PodState.PENDING.before(PodState.RUNNING)
        True
        """
        return (self > other) or (inclusive and self == other)


StatusType = TypeVar('StatusType')  # pylint: disable=invalid-name


@dataclass
class PodStatus():
    """Base pod status detector
    """
    state: PodState
    message: str = ''
    reason: str = ''

    @classmethod
    def from_pod_dict(cls: Type[PodStatus], pod_dict: Dict[str, Any]) -> PodStatus:
        """Get the status of a pod from its dictionary representation

        This is useful if the pod has already been converted to a JSON representation

        Args:
            pod_dict: Dictionary representation of a V1Pod object

        Returns:
            PodStatus instance
        """
        if 'status' not in pod_dict:
            raise KeyError('pod_dict must have a valid "status" key')
        status = deserialize(pod_dict['status'], 'V1PodStatus')
        return cls.from_pod_status(status)

    @classmethod
    def from_pod_status(cls: Type[PodStatus], status: client.V1PodStatus) -> PodStatus:
        """Get the appropriate PodStatus instance from a Kubernetes V1PodStatus object

        The resulting PodStatus instance contains parsed information about the current state of the pod

        Args:
            status: Valid V1PodStatus object

        Returns:
            PodStatus instance
        """
        if RunningStatus.match(status):
            return RunningStatus.from_matching_pod_status(status)
        elif CompletedStatus.match(status):
            return CompletedStatus.from_matching_pod_status(status)
        elif FailedStatus.match(status):
            return FailedStatus.from_matching_pod_status(status)
        elif ScheduledStatus.match(status):
            return ScheduledStatus.from_matching_pod_status(status)
        elif QueuedStatus.match(status):
            return QueuedStatus.from_matching_pod_status(status)
        elif StartingStatus.match(status):
            return StartingStatus.from_matching_pod_status(status)
        elif FailedPullStatus.match(status):
            return FailedPullStatus.from_matching_pod_status(status)
        elif PendingStatus.match(status):
            return PendingStatus.from_matching_pod_status(status)
        else:
            return PodStatus.from_matching_pod_status(status)

    @classmethod
    def from_matching_pod_status(cls: Type[PodStatus], status: client.V1PodStatus) -> PodStatus:
        """Get PodStatus object from a matching Kubernetes V1PodStatus object

        Args:
            status: Matching V1PodStatus object

        Returns:
            A PodStatus instance of the correct type
        """
        del status
        return cls(state=PodState.UNKNOWN)

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        """Determines if the provided status matches
        """
        raise NotImplementedError


@dataclass
class RunningStatus(PodStatus):
    """Status of running pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        return status.phase == 'Running'

    @classmethod
    def from_matching_pod_status(cls: Type[RunningStatus], status: client.V1PodStatus) -> RunningStatus:
        return RunningStatus(state=PodState.RUNNING, message='Running', reason='Running')


@dataclass
class ScheduledStatus(PodStatus):
    """Status of pending pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        if status.phase != 'Pending':
            return False
        if not status.conditions or len(status.conditions) > 1:
            return False
        return status.conditions[0] == client.V1PodCondition(status='True', type='PodScheduled')

    @classmethod
    def from_matching_pod_status(cls: Type[ScheduledStatus], status: client.V1PodStatus) -> ScheduledStatus:
        return ScheduledStatus(state=PodState.SCHEDULED, message='PodScheduled', reason='PodScheduled')


@dataclass
class PendingStatus(PodStatus):
    """Status of pending pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        return status.phase == 'Pending'

    @classmethod
    def from_matching_pod_status(cls: Type[PendingStatus], status: client.V1PodStatus) -> PendingStatus:
        return PendingStatus(state=PodState.PENDING)


@dataclass
class StartingStatus(PodStatus):
    """Status of starting pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        if status.phase != 'Pending':
            return False
        if status.container_statuses is None or status.container_statuses[0].state is None:
            return False
        if status.container_statuses[0].state.waiting is None:
            return False
        return 'ContainerCreating' in status.container_statuses[0].state.waiting.reason

    @classmethod
    def from_matching_pod_status(cls: Type[StartingStatus], status: client.V1PodStatus) -> StartingStatus:
        return StartingStatus(state=PodState.STARTING)


@dataclass
class QueuedStatus(PodStatus):
    """Status of queued pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        if status.phase != 'Pending':
            return False
        if not status.conditions or len(status.conditions) > 1:
            return False
        cond = status.conditions[0]
        return cond.type == 'PodScheduled' and cond.status == 'False' and cond.reason == 'Unschedulable'

    @classmethod
    def from_matching_pod_status(cls: Type[QueuedStatus], status: client.V1PodStatus) -> QueuedStatus:
        return QueuedStatus(state=PodState.QUEUED)


@dataclass
class CompletedStatus(PodStatus):
    """Status of completed pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        return status.phase == 'Succeeded'

    @classmethod
    def from_matching_pod_status(cls: Type[CompletedStatus], status: client.V1PodStatus) -> CompletedStatus:
        return CompletedStatus(state=PodState.COMPLETED)


@dataclass
class FailedStatus(PodStatus):
    """Status of failed pods
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        return status.phase == 'Failed'

    @classmethod
    def from_matching_pod_status(cls: Type[FailedStatus], status: client.V1PodStatus) -> FailedStatus:
        return FailedStatus(state=PodState.FAILED)


@dataclass
class FailedPullStatus(PodStatus):
    """Status of pods that failed image pulls
    """

    @staticmethod
    def match(status: client.V1PodStatus) -> bool:
        if status.phase != 'Pending':
            return False
        if status.container_statuses is None or status.container_statuses[0].state is None:
            return False
        if status.container_statuses[0].state.waiting is None:
            return False
        return status.container_statuses[0].state.waiting.reason in {'ErrImagePull', 'ImagePullBackOff'}

    @classmethod
    def from_matching_pod_status(cls: Type[FailedPullStatus], status: client.V1PodStatus) -> FailedPullStatus:
        return FailedPullStatus(state=PodState.FAILED_PULL)
