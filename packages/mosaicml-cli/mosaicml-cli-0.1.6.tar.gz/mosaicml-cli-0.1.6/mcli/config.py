"""Global Singleton Config Store"""
from __future__ import annotations

import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List

import ruamel.yaml
import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

from mcli.models import MCLIEnvVar, MCLIPlatform, MCLISecret
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_modules import check_if_module_exists
from mcli.utils.utils_serializable_dataclass import SerializableDataclass
from mcli.utils.utils_yaml import StringDumpYAML


def env_path_override_config(config_value: str):
    if config_value in os.environ:
        globals()[config_value] = Path(os.environ[config_value])


def env_str_override_config(config_value: str):
    if config_value in os.environ:
        globals()[config_value] = os.environ[config_value]


MCLI_CONFIG_DIR: Path = Path(os.path.expanduser('~/.mosaic'))
env_path_override_config('MCLI_CONFIG_DIR')

MCLI_BACKUP_CONFIG_DIR: Path = Path(os.path.expanduser('~/.mosaic.bak'))
env_path_override_config('MCLI_BACKUP_CONFIG_DIR')

MCLI_PROJECTS_DIR: Path = MCLI_CONFIG_DIR / 'projects'
env_path_override_config('MCLI_PROJECTS_DIR')

CURRENT_PROJECT_SYMLINK_PATH: Path = MCLI_CONFIG_DIR / 'current_project'
env_path_override_config('CURRENT_PROJECTS_SYMLINK_PATH')

MCTL_CONFIG_PATH: Path = MCLI_CONFIG_DIR / 'config'
env_path_override_config('MCTL_CONFIG_PATH')

MOSAICML_API_ENDPOINT: str = 'https://dat.int.mosaicml.com/api/graphql'
env_str_override_config('MOSAICML_API_ENDPOINT')

MCLI_CONFIG_PATH: Path = MCLI_CONFIG_DIR / 'mcli_config'
env_path_override_config('MCLI_CONFIG_PATH')

MCLI_KUBECONFIG: Path = MCLI_CONFIG_DIR / 'kube_config'
env_path_override_config('MCLI_KUBECONFIG')

COMPOSER_INSTALLED: bool = check_if_module_exists('composer')

UPDATE_CHECK_FREQUENCY_DAYS: float = 2

PAGER_LIMIT: int = 50  # When `mcli get` returns more than PAGER_LIMIT entries, a pager should be used

JOB_TTL: int = int(timedelta(days=14).total_seconds())
MCLI_MODE_ENV: str = 'MCLI_MODE'
env_path_override_config('MCLI_MODE_ENV')

# Used for local dev and testing
MOSAICML_API_KEY_ENV: str = 'MOSAICML_API_KEY'

logging.getLogger('urllib3.connectionpool').disabled = True


class FeatureFlag(Enum):
    ALPHA_TESTER = 'ALPHA_TESTER'
    USE_FEATUREDB = 'USE_FEATUREDB'
    USE_MLPERF_NODES = 'USE_MLPERF_NODES'


class MCLIMode(Enum):
    PROD = 'PROD'
    DEV = 'DEV'
    INTERNAL = 'INTERNAL'


class MCLIConfigError(Exception):
    pass


@dataclass
class MCLIConfig(SerializableDataclass):
    """Global Config Store persisted on local disk"""

    # set to default for now to not break existing users' configs
    MOSAICML_API_KEY: str = ''  # pylint: disable=invalid-name Global Stored within Singleton

    feature_flags: Dict[str, bool] = field(default_factory=dict)
    last_update_check: datetime = field(default_factory=datetime.now)

    # Global Environment Variables
    environment_variables: List[MCLIEnvVar] = field(default_factory=list)

    # Deprecated
    secrets: List[MCLISecret] = field(default_factory=list)

    # Registered Platforms
    platforms: List[MCLIPlatform] = field(default_factory=list)

    @classmethod
    def empty(cls) -> MCLIConfig:
        conf = MCLIConfig()
        conf.apply_environment_overrides()
        return conf

    @property
    def dev_mode(self) -> bool:
        return self.mcli_mode == MCLIMode.DEV

    @property
    def internal(self) -> bool:
        return self.mcli_mode in (
            MCLIMode.INTERNAL,
            MCLIMode.DEV,
        )

    @property
    def mcli_mode(self) -> MCLIMode:
        if os.environ.get(MCLI_MODE_ENV, None):
            found_mode = os.environ.get(MCLI_MODE_ENV)
            if found_mode == 'DEV':
                return MCLIMode.DEV
            elif found_mode == 'INTERNAL':
                return MCLIMode.INTERNAL
        return MCLIMode.PROD

    def apply_environment_overrides(self):
        api_key_env = os.environ.get(MOSAICML_API_KEY_ENV, None)
        if api_key_env is not None:
            self.MOSAICML_API_KEY = api_key_env

    @classmethod
    def load_config(cls, safe: bool = False) -> MCLIConfig:
        """Loads the MCLIConfig from local disk


        Args:
            safe (bool): If safe is true, if the config fails to load it will return
                an empty generated config

        Return:
            Returns the MCLIConfig if successful, otherwise raises Exception
        """
        try:
            with open(MCLI_CONFIG_PATH, 'r', encoding='utf8') as f:
                data = yaml.full_load(f)

                # TODO: Remove after full deprecation transition
                if 'dev_mode' in data:
                    del data['dev_mode']
                if 'internal' in data:
                    del data['internal']
                for platform in data.get('platforms', []):
                    if 'environment_overrides' in platform:
                        del platform['environment_overrides']
                # TODO(END): Remove after full deprecation transition
            conf: MCLIConfig = MCLIConfig.from_dict(data)
        except FileNotFoundError as e:
            if safe:
                return MCLIConfig.empty()
            raise MCLIConfigError(
                f'No mcli config file found at: {MCLI_CONFIG_PATH}. Please run `mcli init` to create it.') from e

        # Optional values can get filled in over time. If a new optional value is not
        # present in the config, let it be filled in by the default, if one was set.
        if set(asdict(conf)) != set(data):
            # TODO: Bug on over-saving HEK-452
            conf.save_config()

        conf.apply_environment_overrides()

        # Deprecating old secrets
        conf.secrets = []

        return conf

    def save_config(self) -> bool:
        """Saves the MCLIConfig to local disk

        Return:
            Returns true if successful
        """
        if self.dev_mode:
            print('saving config...')

        data = self._get_formatted_dump()
        y = YAML()
        y.explicit_start = True  # type: ignore
        with open(MCLI_CONFIG_PATH, 'w', encoding='utf8') as f:
            y.dump(data, f)
        return True

    def _get_formatted_dump(self) -> CommentedMap:
        """Gets the ruamel yaml formatted dump of the config
        """
        raw_data = self.to_disk()

        # Moves platforms to last item
        platforms = raw_data['platforms']
        del raw_data['platforms']
        raw_data['platforms'] = platforms

        # Delete deprecated secrets if possible
        if 'secrets' in raw_data:
            del raw_data['secrets']

        data: CommentedMap = ruamel.yaml.load(
            yaml.dump(raw_data),
            ruamel.yaml.RoundTripLoader,
        )
        data.yaml_set_start_comment('MCLI Config Data\n')
        data.yaml_set_comment_before_after_key(
            key='environment_variables',
            before='\nAll Global Environment variables go here',
        )
        data.yaml_set_comment_before_after_key(
            key='platforms',
            before='\nAll Platforms configured for MCLI',
        )
        return data

    def feature_enabled(self, feature: FeatureFlag) -> bool:
        """Checks if the feature flag is enabled

        Args:
            feature (FeatureFlag): The feature to check
        """
        if not self.internal:
            return False

        if feature.value in self.feature_flags:
            enabled = self.feature_flags[feature.value]
            return bool(enabled)
        return False

    def __str__(self) -> str:
        data = self._get_formatted_dump()
        y = StringDumpYAML()
        return y.dump(data)


def feature_enabled(feature: FeatureFlag) -> bool:
    conf = MCLIConfig.load_config(safe=True)
    return conf.feature_enabled(feature=feature)


class Messages():
    MCLI_NOT_INITIALIZED = f'{FAIL} MCLI not yet initialized. Please run `mcli init` first.'


MESSAGE = Messages()
