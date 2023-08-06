""" Local Sweep Config """
from __future__ import annotations

import copy
import os
import tempfile
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, fields
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from mcli.sweeps.inheritance import (_recursively_update_leaf_data_items, _unwrap_overridden_value_dict,
                                     load_yaml_with_inheritance)
from mcli.utils.utils_string_validation import validate_rfc1123_name


class RunType(Enum):
    CONVERGENCE = 'convergence'
    TIMING = 'timing'
    NONE = 'none'

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class LocalConfig(ABC):
    """Abstract base class for other Mcli Config classes"""
    inherits: Optional[List[Union[str, Path]]] = None
    name: Optional[str] = None

    @classmethod
    def load(cls, path: Union[str, Path]) -> LocalConfig:
        """Load the config from the provided YAML file

        Args:
            path (Union[str, Path]): Path to YAML file

        Returns:
            Config: The config object specified in the YAML file
        """
        with open(path, 'r', encoding='utf8') as fh:
            config = yaml.safe_load(fh)
            if config is None:
                config = {}
        assert isinstance(config, dict)
        config = cls.validate(config)
        return cls(**config)

    @staticmethod
    @abstractmethod
    def validate(fields_to_validate: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError('Config subclasses must implement the ``validate`` staticmethod.')

    @classmethod
    def merge(cls, base: LocalConfig, head: LocalConfig, strategy: str = 'simple') -> LocalConfig:
        """Merge two ``Config`` instances

        Args:
            base (Config): Base ``Config`` object
            head (Config): ``Config`` object to be overlayed on ``base``
            strategy (str, optional): strategy for merging configs. Can be either ``"simple"`` or ``"overlay"``.
                                      ``"simple"`` updates any value not in ``base`` with the value in ``head``.
                                      ``"overlay"`` does a nested merge using YAHP inheritance. Defaults to "simple".

        Raises:
            ValueError: raised for unrecognized ``strategy`` values

        Returns:
            Config: The merged ``Config`` instance
        """
        new = asdict(base)
        if strategy == 'simple':
            for k, v in asdict(head).items():
                if (k not in new) or (new[k] is None):
                    new[k] = v
        elif strategy == 'overlay':
            _recursively_update_leaf_data_items(new, asdict(head), [])
            _unwrap_overridden_value_dict(new)
        else:
            raise ValueError(
                f"Invalid Config merge strategy. Must be one of {['simple', 'overlay']}, but got {strategy}")
        return cls(**new)

    def to_json(self) -> Dict[str, Any]:
        """Converts the config to a JSON dictionary that can be written to a file or stdout

        Returns:
            Dict[str, Any]: The config as a JSON dictionary
        """
        data = asdict(self)
        for k, v in data.items():
            if isinstance(v, Enum):
                data[k] = v.value
        return data

    def dump(self, path: Union[str, Path]):
        """Write the config out as a YAML file

        Args:
            path (Union[str, Path]): Path to output YAML file
        """

        data = self.to_json()
        with open(path, 'w', encoding='utf8') as fh:
            yaml.safe_dump(data, fh)

    def resolve(self):
        """Resolve any ``"inherits"`` sections within the config.

        ``"inherits"`` sections enable external linking to additional YAML files on the filesystem.
        """
        fname = tempfile.mktemp()
        self.dump(fname)
        new_data = load_yaml_with_inheritance(fname)
        new_data = self.validate(new_data)
        self.__dict__.update(**new_data)
        os.remove(fname)

    def copy(self):
        return self.__class__(**copy.deepcopy(asdict(self)))


@dataclass
class LocalSweepConfig(LocalConfig):
    """Configuration for a sweep of runs"""
    image: Optional[str] = None
    git_repo: Optional[str] = None
    git_branch: Optional[str] = None
    command: Optional[str] = None
    named_like: Optional[str] = None
    instance: Optional[str] = None
    run_type: Optional[RunType] = None
    models: Optional[List[str]] = None
    algorithms: Optional[List[List[str]]] = None
    grid: Optional[Dict[str, List[Any]]] = None
    parameters: Optional[Dict[str, Any]] = None
    project: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.run_type, str):
            self.run_type = RunType[self.run_type.upper()]

        if self.name is not None:
            name_is_valid = validate_rfc1123_name(self.name)
            if not name_is_valid:
                raise ValueError(f'Invalid name: {name_is_valid.message}, got {self.name}')

    @staticmethod
    def validate(fields_to_validate: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures that all fields are of the right type

        Args:
            fields (Dict[str, Any]): Dictionary of arguments to be passed to the ``SweepConfig`` constructor

        Returns:
            Dict[str, Any]: Dictionary of arguments, with types corrected, to be passed to
                            the ``SweepConfig`` constructor
        """
        # Convert to list of strings
        for key in ('models', 'algorithms'):
            if isinstance(fields_to_validate.get(key), str):
                fields_to_validate[key] = [fields_to_validate[key]]

        # Ensure run_type is Enum
        if isinstance(fields_to_validate.get('run_type'), str):
            fields_to_validate['run_type'] = RunType[fields_to_validate['run_type'].upper()]

        # Convert to list of lists
        if isinstance(fields_to_validate.get('algorithms'), list):
            if len(fields_to_validate['algorithms']) and isinstance(fields_to_validate['algorithms'][0], str):
                fields_to_validate['algorithms'] = [fields_to_validate['algorithms']]

        return fields_to_validate


RUN_CONFIG_VERSION = 'v0.4.0'


@dataclass
class LocalRunConfig(LocalConfig):
    """ Local Run Config """
    model: Optional[str] = None
    instance: Optional[str] = None
    run_type: Optional[RunType] = None
    git_repo: Optional[str] = None
    git_branch: Optional[str] = None
    image: Optional[str] = None
    command: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    algorithm: Optional[List[str]] = None
    sweep: Optional[str] = None
    project: Optional[str] = None
    version: Optional[str] = field(default=RUN_CONFIG_VERSION)

    def __post_init__(self):
        if isinstance(self.run_type, str):
            self.run_type = RunType[self.run_type.upper()]

        if self.name is not None:
            name_is_valid = validate_rfc1123_name(self.name)
            if not name_is_valid:
                raise ValueError(f'Invalid name: {name_is_valid.message}, got {self.name}')

    @staticmethod
    def validate(fields_to_validate: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures that all fields are of the right type.

        Args:
            fields_to_validate (Dict[str, Any]): Dictionary of arguments to be passed to the ``RunConfig`` constructor

        Returns:
            Dict[str, Any]: Dictionary of arguments, with types corrected, to be passed to
                            the ``RunConfig`` constructor
        """
        # Ensure that parameters exists
        if not fields_to_validate.get('parameters'):
            fields_to_validate['parameters'] = {}

        # Ensure run_type is Enum
        if isinstance(fields_to_validate.get('run_type'), str):
            fields_to_validate['run_type'] = RunType[fields_to_validate['run_type'].upper()]

        return fields_to_validate

    def to_sweep_config(self):

        config = {}
        sweep_fields = {f.name for f in fields(LocalSweepConfig)}
        config = {k: v for k, v in asdict(self).items() if (k in sweep_fields) and (v is not None)}

        # TODO(TL): Consider renaming these. We may go to one model per sweep as well...
        if self.model is not None:
            config['models'] = self.model
        if self.algorithm is not None:
            config['algorithms'] = self.algorithm

        config = LocalSweepConfig.validate(config)
        return LocalSweepConfig(**config)
