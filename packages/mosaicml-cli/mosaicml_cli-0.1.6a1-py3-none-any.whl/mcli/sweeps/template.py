""" Sweep template """
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from mcli.sweeps.config_backend import ConfigBackend, get_default_backend
from mcli.sweeps.inheritance import merge as json_merge
from mcli.sweeps.local_sweep_config import LocalRunConfig, RunType

logger = logging.getLogger(__name__)


def update_nested_dict(data, key, value):
    keys = key.split('.', 1)
    if len(keys) > 1:
        k, key = keys
        if isinstance(data, dict):
            if k not in data:
                data[k] = {}
            data = data[k]
        elif isinstance(data, list):
            for poss in data:
                if not isinstance(poss, dict):
                    raise RuntimeError('Nesting must be dicts or list of dicts')
                if k in poss:
                    data = poss[k]
        else:
            raise RuntimeError('Nesting must dicts or list of dicts')
        update_nested_dict(data, key, value)
    else:
        k = key
        if isinstance(data, dict):
            data[k] = value
        else:
            raise RuntimeError('Leaf nodes must be part of a dictionary')


class TemplateConfigFactory():
    """ Template Config Factory """

    def __init__(
        self,
        model: Optional[str] = None,
        algorithms: Optional[List[str]] = None,
        instance: Optional[str] = None,
        run_type: Optional[RunType] = None,
        loggers: Optional[List[str]] = None,
        backend: Optional[ConfigBackend] = None,
    ):
        """Factory for creating ``RunConfig`` objects from stored YAML files

        Args:
            model (Optional[str], optional): Model name. Defaults to None.
            algorithms (Optional[List[str]], optional): List of algorithms. Defaults to None.
            instance (Optional[str], optional): Compute instance name. Defaults to None.
            run_type (Optional[RunType], optional): The type of run (e.g. "CONVERGENCE"). Defaults to None.
            loggers (Optional[List[str]], optional): The loggers to use. Defaults to None.
            backend (Optional[ConfigBackend]): The configuration backend to use. Defaults to the backend returned by
                                               ``get_default_backend()``.
        """
        self.model = model
        if isinstance(algorithms, str):
            algorithms = [algorithms]
        self.algorithms = algorithms
        self.instance = instance
        self.run_type = run_type
        if isinstance(loggers, str):
            loggers = [loggers]
        self.loggers = loggers
        self._backend = backend or get_default_backend()

    def build_model_config(self) -> LocalRunConfig:
        """Build a ``RunConfig`` for just this object's model.

        Returns:
            RunConfig
        """
        if self.model is not None:
            parameters = self._backend.get_model_config(self.model)
            return LocalRunConfig(parameters=parameters)
        else:
            return LocalRunConfig()

    def build_instance_config(self):
        """Build a ``RunConfig`` for just this object's instance.

        Returns:
            RunConfig
        """
        if self.instance is not None:
            parameters = self._backend.get_instance_config(self.instance, model=self.model)
            return LocalRunConfig(parameters=parameters)
        else:
            return LocalRunConfig()

    def build_algorithms_config(self):
        """Build a ``RunConfig`` for just this object's algorithms.

        Returns:
            RunConfig
        """
        if self.algorithms is not None:
            # TODO (TL): Add support for model-specific algorithm overrides (HEK-78)
            parameters: Dict[str, Any] = {'algorithms': {}}
            for algorithm in self.algorithms:
                config = self._backend.get_algorithm_config(algorithm)
                parameters = json_merge(parameters, {'algorithms': {algorithm: config}})
            return LocalRunConfig(parameters=parameters)
        else:
            return LocalRunConfig()

    def build_run_type_config(self):
        """Build a ``RunConfig`` for this object's run type.

        Returns:
            RunConfig
        """
        if self.run_type is not None:
            parameters = self._backend.get_run_type_config(self.run_type)

            # TODO (TL): Remove this hack for algo-specific timing overrides (HEK-79)
            if self.algorithms is not None and self.run_type == RunType.TIMING:
                for a in self.algorithms:
                    if a in ('swa', 'progressive_resizing', 'selective_backprop', 'layer_freezing'):
                        update_nested_dict(parameters, 'callbacks.benchmarker.all_epochs', 'true')
                        break

            return LocalRunConfig(parameters=parameters)
        else:
            return LocalRunConfig()

    def build_loggers_config(self) -> LocalRunConfig:
        """Build a ``RunConfig`` from known logger configurations.

        Returns:
            RunConfig
        """
        if self.loggers is not None:
            # TODO (TL): Loggers are currently stored as lists of single-item dicts. Fix this with (HEK-55).
            parameters: Dict[str, Any] = {'loggers': []}
            for config_logger in self.loggers:
                config = self._backend.get_logger_config(config_logger)
                parameters = json_merge(parameters, config)
            return LocalRunConfig(parameters=parameters)
        else:
            return LocalRunConfig()
