""" Generic Config Backend """
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from mcli.sweeps.inheritance import merge as json_merge
from mcli.sweeps.local_sweep_config import RunType
from mcli.utils.utils_composer import get_composer_directory, is_composer_installed
from mcli.utils.utils_file import list_yamls
from mcli.utils.utils_types import PathLike

logger = logging.getLogger(__name__)


class ConfigBackend(ABC):
    """ Generic Config Backend """

    @abstractmethod
    def list_models(self) -> List[str]:
        """List all models with known configurations

        Returns:
            List[str]: List of model names
        """
        pass

    @abstractmethod
    def get_model_config(self, model: str) -> Dict[str, Any]:
        """Get the configuration for a specific model

        Args:
            model (str): The name of the model. If it is not valid, an empty dict will be returned.

        Returns:
            Dict[str, Any]: Known configuration for the requested model
        """
        pass

    @abstractmethod
    def list_instances(self, model: Optional[str] = None) -> List[str]:
        """List all instances with known configurations

        Args:
            model (Optional[str]): List only instances with known configurations for the specified model.
                                   Defaults to None.

        Returns:
            List[str]: List of instance names
        """
        pass

    @abstractmethod
    def get_instance_config(self, instance: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Get the configuration for a specific instance

        Args:
            instance (str): The name of the instance. If it is not valid, an empty dict will be returns
            model (Optional[str]): Include model-specific configuration for the instance, if it exists.
                                   Defaults to None.

        Returns:
            Dict[str, Any]: Known configuration for the requested instance
        """
        pass

    @abstractmethod
    def list_algorithms(self) -> List[str]:
        """List all algorithms with known configurations

        Returns:
            List[str]: List of algorithm names
        """
        pass

    @abstractmethod
    def get_algorithm_config(self, algorithm: str) -> Dict[str, Any]:
        """Get the configuration for a specific algorithm

        Args:
            algorithm (str): The name of the algorithm. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested algorithm
        """
        pass

    @abstractmethod
    def list_loggers(self) -> List[str]:
        """List all supported loggers with known configurations

        Returns:
            List[str]: List of logger names
        """
        pass

    @abstractmethod
    def get_logger_config(self, config_logger: str) -> Dict[str, Any]:
        """Get the configuration for a specific logger

        Args:
            logger (str): The name of the logger. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested logger
        """
        pass

    @abstractmethod
    def list_run_types(self) -> List[RunType]:
        """List all supported run types with known configurations

        Returns:
            List[RunType]: List of run types
        """
        pass

    @abstractmethod
    def get_run_type_config(self, run_type: RunType) -> Dict[str, Any]:
        """Get the configuration for a specific run type

        Args:
            run_type (RunType): The type of run. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested run type
        """
        pass


class MCLIConfigBackend(ConfigBackend):
    """ MCLI Config Backend """

    def __init__(self, root: Optional[PathLike] = None):
        """Backend for known configurations stored in mcli

        Args:
            root (Optional[PathLike]): Path to a folder with YAML files in "defaults" and "model-specific"
                                       subdirectories. Defaults to "GIT_ROOT/mcli-yamls" for the mcli repo.
        """
        if root is None:
            root = Path(__file__).resolve().parents[2].joinpath('mcli-yamls')
        self._root = Path(root)
        self._defaults_dir = self._root.joinpath('defaults')
        self._overrides_dir = self._root.joinpath('model-specific')

    @staticmethod
    def _load_yaml_if_exists(path: PathLike) -> Dict[str, Any]:
        """Load the provided YAML. If it doesn't exist or is empty, returns an empty dict.
        """
        data = {}
        if Path(path).exists():
            with open(path, 'r', encoding='utf8') as fh:
                data = yaml.safe_load(fh)
                if data is None:
                    data = {}
        return data

    def list_models(self) -> List[str]:
        """List all models with known configurations

        Returns:
            List[str]: List of model names
        """
        path = self._defaults_dir.joinpath('models')
        return sorted([m.stem for m in list_yamls(path)])

    def get_model_config(self, model: str) -> Dict[str, Any]:
        """Get the configuration for a specific model

        Args:
            model (str): The name of the model. If it is not valid, an empty dict will be returned.

        Returns:
            Dict[str, Any]: Known configuration for the requested model
        """

        overrides = self._overrides_dir.joinpath(model, 'model.yaml')
        base = self._load_yaml_if_exists(overrides)

        default = self._defaults_dir.joinpath('models', f'{model}.yaml')
        if not default.exists():
            logger.warning(
                f"No model configuration found for model {model}. In order to run it, you'll need to provide its "
                'parameters manually, including additional details like datasets, optimizers, schedulers, etc.')
        head = self._load_yaml_if_exists(default)

        return json_merge(base, head)

    def list_instances(self, model: Optional[str] = None) -> List[str]:
        """List all instances with known configurations

        Args:
            model (Optional[str]): List only instances with known configurations for the specified model.
                                   Defaults to None.

        Returns:
            List[str]: List of instance names
        """
        instances: List[str] = []
        path = self._defaults_dir.joinpath('instances')
        if model is not None:
            model_specific_path = self._overrides_dir.joinpath(model, 'instances')
            if model_specific_path.exists() and model_specific_path.is_dir():
                instances = sorted([p.stem for p in list_yamls(model_specific_path)])
            if len(instances) == 0:
                logger.warning(f"No instance configuration found for model {model}. In order to run this model, you'll "
                               'need to provide instance specific parameters manually, e.g. dataset paths.')
        if len(instances) == 0:
            instances = sorted([p.stem for p in list_yamls(path)])
        return instances

    def get_instance_config(self, instance: str, model: Optional[str] = None) -> Dict[str, Any]:
        """Get the configuration for a specific instance

        Args:
            instance (str): The name of the instance. If it is not valid, an empty dict will be returns
            model (Optional[str]): Include model-specific configuration for the instance, if it exists.
                                   Defaults to None.

        Returns:
            Dict[str, Any]: Known configuration for the requested instance
        """
        yaml_file = self._defaults_dir.joinpath('instances', f'{instance}.yaml')
        config = self._load_yaml_if_exists(yaml_file)
        if model is not None:
            overrides_yaml = self._overrides_dir.joinpath(model, 'instances', f'{instance}.yaml')
            base = self._load_yaml_if_exists(overrides_yaml)
            config = json_merge(base, config)
        return config

    def list_algorithms(self) -> List[str]:
        """List all algorithms with known configurations

        Returns:
            List[str]: List of algorithm names
        """
        path = self._defaults_dir.joinpath('algorithms')
        return sorted([a.stem for a in list_yamls(path)])

    def get_algorithm_config(self, algorithm: str) -> Dict[str, Any]:
        """Get the configuration for a specific algorithm

        Args:
            algorithm (str): The name of the algorithm. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested algorithm
        """
        yaml_file = self._defaults_dir.joinpath('algorithms', f'{algorithm}.yaml')
        return self._load_yaml_if_exists(yaml_file)

    def list_loggers(self) -> List[str]:
        """List all supported loggers with known configurations

        Returns:
            List[str]: List of logger names
        """
        path = self._defaults_dir.joinpath('loggers')
        return sorted([logger_file.stem for logger_file in list_yamls(path)])

    def get_logger_config(self, config_logger: str) -> Dict[str, Any]:
        """Get the configuration for a specific logger

        Args:
            logger (str): The name of the logger. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested logger
        """
        yaml_file = self._defaults_dir.joinpath('loggers', f'{config_logger}.yaml')
        return self._load_yaml_if_exists(yaml_file)

    def list_run_types(self) -> List[RunType]:
        """List all supported run types with known configurations

        Returns:
            List[RunType]: List of run types
        """
        yaml_dir = self._defaults_dir.joinpath('run_types')
        run_type_names = [t.stem for t in list_yamls(yaml_dir)]
        return [RunType[name.upper()] for name in sorted(run_type_names)]

    def get_run_type_config(self, run_type: RunType) -> Dict[str, Any]:
        """Get the configuration for a specific run type

        Args:
            run_type (RunType): The type of run. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested run type
        """
        yaml_file = self._defaults_dir.joinpath('run_types', f'{run_type.value}.yaml')
        return self._load_yaml_if_exists(yaml_file)


class ComposerConfigBackend(MCLIConfigBackend):
    """ Composer Config Backend """

    def __init__(self):
        """Backend for known configurations stored in composer

        Args:
            root (Optional[PathLike]): Path to a folder with YAML files in "defaults" and "model-specific"
                                       subdirectories. Defaults to "GIT_ROOT/mcli-yamls" for the mcli repo.

        Note:
            The `composer` library must be installed locally in order to find the appropriate configuration files.
            If it is not installed, an error will be raised. "model" and "algorithm" configurations are sourced from
            the local composer, while any remaining configurations are sourced from `mcli`.
        """

        if not is_composer_installed():
            raise ImportError('Cannot get configurations from composer because it could not be found. Please run '
                              '`pip install mosaicml` to install it.')
        self._composer_dir = get_composer_directory().joinpath('yamls')
        super().__init__()

    def list_models(self) -> List[str]:
        """List all models with known configurations

        Returns:
            List[str]: List of model names
        """
        path = self._composer_dir.joinpath('models')
        return sorted([m.stem for m in list_yamls(path)])

    def get_model_config(self, model: str) -> Dict[str, Any]:
        """Get the configuration for a specific model

        Args:
            model (str): The name of the model. If it is not valid, an empty dict will be returned.

        Returns:
            Dict[str, Any]: Known configuration for the requested model
        """

        yaml_file = self._composer_dir.joinpath('models', f'{model}.yaml')
        if not yaml_file.exists():
            logger.warning(
                f"No model configuration found for model {model}. In order to run it, you'll need to provide its "
                'parameters manually, including additional details like datasets, optimizers, schedulers, etc.')
        return self._load_yaml_if_exists(yaml_file)

    def list_algorithms(self) -> List[str]:
        """List all algorithms with known configurations

        Returns:
            List[str]: List of algorithm names
        """
        path = self._composer_dir.joinpath('algorithms')
        return sorted([a.stem for a in list_yamls(path)])

    def get_algorithm_config(self, algorithm: str) -> Dict[str, Any]:
        """Get the configuration for a specific algorithm

        Args:
            algorithm (str): The name of the algorithm. If it is not valid, an empty dict will be returns

        Returns:
            Dict[str, Any]: Known configuration for the requested algorithm
        """
        yaml_file = self._composer_dir.joinpath('algorithms', f'{algorithm}.yaml')
        return self._load_yaml_if_exists(yaml_file)


def get_default_backend() -> ConfigBackend:
    """Gets the default backend based on whether `composer` is installed.

    Returns:
        ConfigBackend: an instance of either ComposerConfigBackend or MCLIConfigBackend
    """
    if is_composer_installed():
        return ComposerConfigBackend()
    else:
        return MCLIConfigBackend()
