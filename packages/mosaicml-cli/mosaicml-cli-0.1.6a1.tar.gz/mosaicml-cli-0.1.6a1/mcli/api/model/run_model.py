""" GraphQL representation of MCLIJob"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

from mcli.api.engine.utils import dedent_indent
from mcli.api.schema.generic_model import DeserializableModel
from mcli.models.run_input import RunInput
from mcli.serverside.job.mcli_job import MCLIJob


class RunStatus(Enum):
    """Status of an individual run
    """
    FAILED = 'failed'
    QUEUED = 'queued'
    STOPPED = 'stopped'
    RUNNING = 'running'
    SUCCEEDED = 'succeeded'
    UNKNOWN = 'unknown'


@dataclass
class RunModel(DeserializableModel):
    """ The GraphQL Serializable and Desrializable representation of a MCLIJob

    The intermediate form includes the MCLIJob as a bjson value
    """

    run_uid: str
    run_name: str
    run_status: RunStatus
    created_by_id: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    tags: List[str] = field(default_factory=list)

    # TODO: make this a dataclass type that is serializable
    run_config: Dict[str, Any] = field(default_factory=dict)

    property_translations = {
        'runUid': 'run_uid',
        'runName': 'run_name',
        'runConfig': 'run_config',
        'runStatus': 'run_status',
        'createdById': 'created_by_id',
        'createdAt': 'created_at',
        'updatedAt': 'updated_at',
        'isDeleted': 'is_deleted',
    }

    @classmethod
    def from_mcli_job(cls, mcli_job: MCLIJob) -> RunModel:
        data = {
            'run_uid': mcli_job.unique_name,
            'run_name': mcli_job.run_name,
            'run_status': RunStatus.UNKNOWN,
        }
        return cls(**data, run_config=asdict(mcli_job))

    @classmethod
    def from_run_input(cls, run_input: RunInput) -> RunModel:
        mcli_job = MCLIJob.from_run_input(run_input=run_input)
        return cls.from_mcli_job(mcli_job=mcli_job)

    def to_create_run_input(self):
        return {
            'runName': self.run_name,
            'runConfig': asdict(self),
        }


def get_run_schema(indentation: int = 2,):
    """ Get the GraphQL schema for a :type RunModel:
    Args:
        indentation (int): Optional[int] for the indentation of the block
    Returns:
        Returns a GraphQL string with all the fields needed to initialize a
        :type RunModel:
    """
    return dedent_indent(
        """
runUid
runName
runConfig
runStatus
tags
createdById
createdAt
updatedAt
isDeleted
        """, indentation)
