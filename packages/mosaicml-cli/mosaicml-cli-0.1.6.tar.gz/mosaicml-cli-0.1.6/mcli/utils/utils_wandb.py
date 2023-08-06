"""Utils for accessing and modifying WanDB"""
import copy
import json
import logging
import tempfile
import warnings
from abc import ABC
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from mcli.sweeps.config_backend import MCLIConfigBackend
from mcli.sweeps.inheritance import ListOfSingleItemDict
from mcli.utils.utils_types import convert_dict_to_single_item_lists, delete_nested_key

logger = logging.getLogger(__name__)


# Create yaml from wandb run config
def wandb_config_to_yaml(config):
    yaml_config = {}
    for dot_key, v in config.items():
        keys = dot_key.split('.')
        inner = yaml_config
        for key in keys[:-1]:
            inner = inner.setdefault(key, {})
        inner[keys[-1]] = v
    return yaml_config


def model_name_from_config(config):
    model_hparam_key_fragments = [key for key in config.keys() if key.startswith('model.')]
    if len(model_hparam_key_fragments) == 0:
        if isinstance(config['model'], str):
            model = config['model']
        else:
            model = list(config['model'].keys())[0]
    else:
        model_hparam_key = model_hparam_key_fragments[0]
        model = model_hparam_key.split('.')[1]

    return model


def _remove_wandb_parameter_metadata(parameters: Dict[str, Any], upgrade: bool) -> Dict[str, Any]:
    # Remove wandb metadata
    parameters = delete_nested_key(parameters, ['metadata'])
    for k in ('name', 'project', 'tags', 'extra_init_params'):
        parameters = delete_nested_key(parameters, ['loggers', 'wandb', k])
    parameters = delete_nested_key(parameters, ['algo_str'])
    parameters = delete_nested_key(parameters, ['algorithms_str'])
    parameters = delete_nested_key(parameters, ['algo'])
    parameters = delete_nested_key(parameters, ['instance'])
    if upgrade:
        parameters = upgrade_version(parameters, 'latest')

    return parameters


def get_run_details(run, include_env=False, upgrade=True):
    if hasattr(run.config, 'as_dict'):
        yaml_config = run.config.as_dict()
    else:
        yaml_config = run.config
    if any('.' in k for k in yaml_config):  # contains dot-syntax keys
        yaml_config = wandb_config_to_yaml(yaml_config)
        yaml_config = convert_dict_to_single_item_lists(yaml_config,
                                                        ['algorithms', 'schedulers', 'loggers', 'callbacks'])

    metadata = yaml_config.get('metadata')
    if run.job_type == 'timing':
        run_type_key = 'timing_instance'
    elif run.job_type == 'convergence':
        run_type_key = 'convergence_instance'
    else:
        run_type_key = None
    details = {}
    if metadata is not None:
        details = {'models': metadata.get('model')}
        if include_env:
            details.update({
                'image': metadata.get('image'),
                'git_repo': metadata.get('repo'),
                'git_branch': metadata.get('commit'),
            })

        if run_type_key is not None:
            details[run_type_key] = metadata.get('instance')
    else:
        details = {'models': model_name_from_config(yaml_config)}
        if include_env:
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    meta_json = json.load(run.file('wandb-metadata.json').download(root=tmpdir))
                git_details = meta_json.get('git', {})
                details['git_repo'] = git_details.get('remote')
                details['git_branch'] = git_details.get('commit')
            except Exception as _:  # pylint: disable=broad-except
                run_path = '/'.join(run.path)
                logger.info(f'WandBDataWarning: Could not get environment details from run: {run_path}',)
                pass
        if run_type_key is None:
            if 'timing' in run.project:
                run_type_key = 'timing_instance'
            else:
                run_type_key = 'accuracy_instance'
            instance = yaml_config.get('instance', None)
            if instance is not None:
                details[run_type_key] = instance

    parameters = copy.deepcopy(yaml_config)
    parameters = _remove_wandb_parameter_metadata(parameters, upgrade=upgrade)

    details['parameters'] = parameters
    if 'algorithms' in parameters:
        if isinstance(parameters['algorithms'], dict):
            details['algorithms'] = list(parameters['algorithms'].keys())
        elif isinstance(parameters['algorithms'], list):
            if len(parameters['algorithms']) and isinstance(parameters['algorithms'][0], dict):
                details['algorithms'] = [list(a.keys())[0] for a in parameters['algorithms']]
            else:
                details['algorithms'] = parameters['algorithms']
    return details


def get_diff(d1: Dict, d2: Dict) -> Dict:
    """Get the difference between two nested config dictionaries.

    Determines a nested dictionary where each leaf node is an element where ``d1`` and ``d2`` differ.
    For each element, the key is taken from either dictionary and the value is a tuple of the values from
    the two dictionaries. If one of the dictionaries does not contain that key, its value will be provided
    as "UNSPECIFIED".

    Args:
        d1, d2 (Dict): Two nested config dictionaries

    Returns:
        Dict: dictionary of the differences between ``d1`` and ``d2``
    """
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersection = d1_keys & d2_keys
    d1_only = d1_keys - d2_keys
    d2_only = d2_keys - d1_keys
    diff = {}
    for k in sorted(list(intersection)):
        if isinstance(d1[k], dict) and isinstance(d2[k], dict):
            inner_diff = get_diff(d1[k], d2[k])
            if len(inner_diff):
                diff[k] = inner_diff
        else:
            if d1[k] != d2[k]:
                diff[k] = (d1[k], d2[k])
    diff.update({k: (d1[k], 'UNSPECIFIED') for k in d1_only})
    diff.update({k: ('UNSPECIFIED', d2[k]) for k in d2_only})

    return diff


# # Find all runs of a bundle in a list of projects
# def find_bundles(projects, exclude_keys):
#     unique_configs = []
def get_archetypal_runs(runs, bundles=None):
    if bundles is None:
        bundles = [InstanceBundle, SSRBundle, RunTypeBundle, SeedBundle]
    configs = {}
    for run in runs:
        config = get_run_details(run)
        for b in bundles:
            config = b.remove_modified_keys(config)
        config = json.dumps(config, sort_keys=True)
        if config not in configs:
            configs[config] = run
    return list(configs.values())


def get_flattened_dict(data: Dict[str, Any], _prefix: List[str], separator: str = '.') -> Dict[str, Any]:
    """
    Flattens a dictionary with list or sub dicts to have dot syntax
    i.e. {
        "sub_dict":{
        "sub_list":[
            "sub_sub_dict":{
            "field1": 12,
            "field2": "tomatoes"
            }
        ]
        },
        "field3": "potatoes"
    }
    returns:
    {
        "sub_dict.sub_list.sub_sub_dict.field1": 12,
        "sub_dict.sub_list.sub_sub_dict.field2": "tomatoes,
        "field3": "potatoes",
    }
    """
    all_items = {}
    for key, val in data.items():
        key_items = _prefix + [key]
        key_name = separator.join(key_items)
        if isinstance(val, dict):
            all_items.update(get_flattened_dict(val, key_items, separator))
        elif isinstance(val, list):
            found_sub_dicts = False
            for item in val:
                if isinstance(item, dict):
                    found_sub_dicts = True
                    for sub_key, sub_val in item.items():
                        all_items.update(get_flattened_dict(sub_val, key_items + [sub_key], separator))
            if not found_sub_dicts:
                all_items[key_name] = val
        else:
            all_items[key_name] = val
    return all_items


class InstanceBundle(object):
    """ A bundle of instance types to group runs under """
    modified_keys: List[str] = ['timing_instance', 'accuracy_instance']

    def __init__(self, model: Optional[str] = None):
        if model is not None:
            backend = MCLIConfigBackend(Path(__file__).parents[2].joinpath('mcli-yamls'))
            instances = backend.list_instances(model)
            stable = {}
            diff_keys = set()
            for ii, instance in enumerate(instances):
                conf = backend.get_instance_config(instance, model)
                conf = get_flattened_dict(conf, _prefix=[])
                if ii == 0:
                    stable = conf
                else:
                    diff = get_diff(stable, conf)
                    for k in get_flattened_dict(diff, _prefix=[]):
                        stable.pop(k, None)
                        diff_keys.add(k)
            self.modified_keys = list(self.modified_keys) + list(diff_keys)

    @classmethod
    def remove_modified_keys(cls, config):
        if 'models' not in config:
            warnings.warn('config does not have a model key. This could lead to duplicate instance bundles since all '
                          'modified instance-specific keys cannot be determined')
        bundle = cls(config.get('models', None))
        config = copy.deepcopy(config)
        for k in bundle.modified_keys:
            config = delete_nested_key(config, k.split('.'))
        return config


class SSRBundle(object):
    """ A bundle of keys to simplify SSR run creation """

    modified_keys: List[str] = ['parameters.algorithms.scale_schedule.ratio']

    @classmethod
    def remove_modified_keys(cls, config):
        config = copy.deepcopy(config)
        for k in cls.modified_keys:
            config = delete_nested_key(config, k.split('.'))
        return config


class RunTypeBundle(object):
    """ A bundle of runtype to simplify run creation """

    modified_keys: List[str] = ['parameters.callbacks', 'parameters.validate_every_n_epochs']

    @classmethod
    def remove_modified_keys(cls, config):
        config = copy.deepcopy(config)
        for k in cls.modified_keys:
            config = delete_nested_key(config, k.split('.'))
        return config


class SeedBundle(object):
    """ A bundle of keys to simplify multi-seed run creation """

    modified_keys: List[str] = ['parameters.seed']

    @classmethod
    def remove_modified_keys(cls, config):
        config = copy.deepcopy(config)
        for k in cls.modified_keys:
            config = delete_nested_key(config, k.split('.'))
        return config


# Modify config


def nested_key_in(config: Dict, keys: Union[List, Tuple, str]) -> bool:
    """Check if the nested key exists in the dictionary.

    Args:
        config (Dict): Nested dictionary
        keys (Union[List, str]): Either a list of nested keys or a '.'-separated string of nested keys

    Returns:
        bool: True if the key is present
    """
    if isinstance(keys, str):
        keys = list(keys.split('.'))
    inner = config
    for key in keys[:-1]:
        if isinstance(inner, list):
            inner = ListOfSingleItemDict(inner)
        if key not in inner:
            return False
        inner = inner[key]
        if not isinstance(inner, (dict, list)):
            return False
    return keys[-1] in inner


def copy_nested_key(config: Dict,
                    source_keys: Union[List, Tuple, str],
                    dest_keys: Union[List, Tuple, str],
                    keep: bool = False,
                    method: Optional[Callable] = None) -> Dict:
    if isinstance(source_keys, str):
        source_keys = list(source_keys.split('.'))
    if isinstance(dest_keys, str):
        dest_keys = list(dest_keys.split('.'))

    if nested_key_in(config, source_keys):
        inner = config
        for key in source_keys[:-1]:
            if isinstance(inner, list):
                inner = ListOfSingleItemDict(inner)
            inner = inner[key]
        if not keep:
            value = inner.pop(source_keys[-1])
        else:
            value = inner[source_keys[-1]]
        inner = config
        for key in dest_keys[:-1]:
            if isinstance(inner, list):
                inner = ListOfSingleItemDict(inner)
            if key not in inner:
                inner[key] = {}
        if method is not None:
            value = method(value)
        inner[dest_keys[-1]] = value
    return config


# TODO (TL): Remove `in_place` as an argument.
class Versioning(ABC):
    """ Base class for all versions
    """
    name: str = ''
    additions: Optional[Tuple[str]] = None
    translations: Optional[Tuple[Tuple[str, str, Optional[Callable]]]] = None
    deletions: Optional[Tuple[str]] = None

    @classmethod
    def validate(cls, config: Dict) -> Union[bool, None]:
        """Validates if the given config dictionary could have come from this version.

        Args:
            config (Dict): Trainer Hparams configuration dictionary

        Returns:
            Union[bool, NoneType]: ``True`` if it COULD have, ``False`` if it COULD NOT have
                 and ``None`` if it's UNKNOWN.
        """
        if cls.deletions:
            for key in cls.deletions:
                # TODO: Fix typing here
                if nested_key_in(config, key):
                    return False
        if cls.translations:
            for key, _, _ in cls.translations:
                if nested_key_in(config, key):
                    return False
        if cls.additions:
            for key in cls.additions:
                if nested_key_in(config, key):
                    return True
        if cls.translations:
            for _, key, _ in cls.translations:
                if nested_key_in(config, key):
                    return True
        return

    @classmethod
    def upgrade(cls, config: Dict, in_place: bool = False, alert_missing: bool = True) -> Dict:
        """Upgrade the given config dictionary to this version from the previous one.

        Args:
            config (Dict): Trainer Hparams configuration dictionary
            in_place (bool): Whether ``config`` should be modified in-place
            alert_missing (bool): Whether to alert if ``config`` may be missing necessary keys

        Returns:
            Dict: The upgraded configuration dictionary
        """
        if not in_place:
            config = copy.deepcopy(config)
        if cls.translations:
            for (source, dest, method) in cls.translations:
                config = copy_nested_key(config, source, dest, method=method)
        if cls.deletions:
            for source in cls.deletions:
                config = delete_nested_key(config, source.split('.'))
        if cls.translations:
            for (source, _, _) in cls.translations:
                config = delete_nested_key(config, source.split('.'))
        if alert_missing and cls.additions and len(cls.additions):
            keys = ['.'.join(k) if isinstance(k, (tuple, list)) else k for k in cls.additions]
            warnings.warn(
                f'PossibleMissingKey: Upgraded to version {cls.name}.'
                f" You may be missing the following keys in your configuration: {','.join(keys)}.",)
        return cls.upgrade_additional(config)

    @classmethod
    def upgrade_additional(cls, config: Dict) -> Dict:
        return config

    @classmethod
    def downgrade_additional(cls, config: Dict) -> Dict:
        return config

    @classmethod
    def downgrade(cls, config, in_place: bool = False, alert_missing: bool = True) -> Dict:
        """Downgrade the given config dictionary from this version to the previous one.

        Args:
            config (Dict): Trainer Hparams configuration dictionary.
            in_place (bool): Whether ``config`` should be modified in-place. Defaults to ``False``.
            alert_missing (bool): Whether to alert if ``config`` may be missing necessary keys. Defaults to ``True``.

        Returns:
            Dict: The downgraded configuration dictionary
        """
        if not in_place:
            config = copy.deepcopy(config)
        if cls.translations:
            for (dest, source, method) in cls.translations:
                config = copy_nested_key(config, source, dest, method=method)
        if cls.additions:
            for source in cls.additions:
                config = delete_nested_key(config, source.split('.'))
        if cls.translations:
            for (_, dest, _) in cls.translations:
                config = delete_nested_key(config, dest.split('.'))
        if alert_missing and cls.deletions and len(cls.deletions):
            keys = ['.'.join(k) if isinstance(k, (tuple, list)) else k for k in cls.deletions]
            warnings.warn(
                f'PossibleMissingKey: Downgraded from version {cls.name}. '
                f"You may be missing the following keys in your configuration: {','.join(keys)}.",)
        return cls.downgrade_additional(config)


def to_str(non_str: Any, prefix: str = '', suffix: str = ''):
    if not isinstance(non_str, str):
        return f'{prefix}{str(non_str)}{suffix}'
    else:
        return non_str


class PreLaunch(Versioning):
    name: str = 'prelaunch'
    # additions: Tuple[Union[str, Tuple]] = (("optimizer", "mosaicml_sgdw"), ("optimizer", "mosaicml_adamw"),
    #                                        ("callbacks", "timing_monitor"))


class ComposerV0_3_2(Versioning):  # pylint: disable=invalid-name
    """ V0.3.2 Run Conifg """
    name: str = 'v0.3.2'
    # TODO: Move to '.' notation from nested tuples -> Tuple[Tuple[str, str]]
    translations: Tuple[Tuple[str, str, Optional[Callable]]] = (
        ('ddp.sync_strategy', 'ddp_sync_strategy', None), ('ddp.timeout', 'dist_timeout', None),
        ('ddp_timeout', 'dist_timeout', None), ('total_batch_size', 'train_batch_size',
                                                None), ('max_epochs', 'max_duration', lambda x: to_str(x, suffix='ep')),
        ('checkpoint_interval_unit', 'save_checkpoint.interval_unit',
         None), ('checkpoint_folder', 'save_checkpoint.folder',
                 None), ('checkpoint_interval', 'save_checkpoint.interval',
                         None), ('checkpoint_filepath', 'load_checkpoint.checkpoint',
                                 None), ('checkpoint_load_weights_only', 'load_checkpoint.load_weights_only', None),
        ('checkpoint_strict_model_weights', 'load_checkpoint.strict_model_weights',
         None), ('loggers.file.flush_every_n_batches', 'loggers.file.flush_interval', None))  # type: ignore
    deletions: Tuple[str] = ('ddp',)

    @classmethod
    def upgrade_additional(cls, config: Dict) -> Dict:
        if nested_key_in(config, 'load_checkpoint.checkpoint'):
            chk = config['load_checkpoint']['checkpoint']
            if chk is None:
                del config['load_checkpoint']
        else:
            if 'load_checkpoint' in config:
                del config['load_checkpoint']
        if nested_key_in(config, 'save_checkpoint.interval_unit'):
            iu = config['save_checkpoint']['interval_unit']
            if iu is None:
                del config['save_checkpoint']
        else:
            if 'save_checkpoint' in config:
                del config['save_checkpoint']
        if nested_key_in(config, 'loggers.file.log_level'):
            if isinstance(config['loggers'], list):
                file_config = ListOfSingleItemDict(config['loggers'])['file']
            else:
                file_config = config['loggers']['file']
            file_level = file_config['log_level']
            if nested_key_in(config, 'loggers.file.every_n_epochs'):  # Old version, move carefully
                k = 'every_n_epochs' if file_level.lower() == 'epoch' else 'every_n_batches'
                file_config['log_interval'] = file_config[k]
                del file_config['every_n_epochs']
                del file_config['every_n_batches']
        if nested_key_in(config, 'model.resnet50'):
            model_config = config['model'].pop('resnet50')
            model_config['model_name'] = 'resnet50'
            config['model']['resnet'] = model_config

        return config


class ComposerV0_3_0(Versioning):  # pylint: disable=invalid-name
    """ V0.3.0 Run Conifg """

    name: str = 'v0.3.0'
    deletions: Tuple[str] = ('device.gpu.n_gpus',)


class ComposerV0_2_4(Versioning):  # pylint: disable=invalid-name
    """ V0.2.4 Run Conifg """

    name: str = 'v0.2.4'
    translations: Tuple[Tuple[str, str, Optional[Callable]]] = (
        ('optimizer.mosaicml_sgdw', 'optimizer.decoupled_sgdw',
         None), ('optimizer.mosaicml_adamw', 'optimizer.decoupled_adamw',
                 None), ('callbacks.timing_monitor', 'callbacks.benchmarker',
                         None), ('schedulers.cosine_cooldown', 'schedulers.cosine_decay',
                                 None), ('accelerator', 'device', None))  # type: ignore


def check_version(config: Dict) -> str:
    """Find the earliest composer version compatible with the given configuration dictionary.

    Args:
        config (Dict): TrainerHparams configuration dictionary

    Returns:
        str: Version string for the earlier composer version compatible with the given config

    NOTE: This is not an exact 1-1 mapping. This will always break if a key is re-introduced.
    TODO: Add a version string to the config so we don't have to guess.
    """
    if not isinstance(config, dict):
        raise TypeError(f'config must be a dictionary, not {type(config)}')

    version = ''
    value = None
    for name, version_class in VERSIONS.items():
        gt = version_class.validate(config)
        if gt is None:
            if value is None and version == '':
                # We want the first None
                version = name
            value = None
        elif gt:
            # First True takes priority over first None
            # True after False wins out
            if value is None or value is False:
                version = name
            value = True
        else:
            value = False

    if version == '':
        raise ValueError('Somehow this configuration dictionary did not match any of the known versions.')
    return version


def migrate_version(config: Dict, version: str, in_place: bool = False, alert_missing: bool = True) -> Dict:
    """Migrate the configuration dictionary to the desired version.

    Args:
        config (Dict): Trainer Hparams configuration dictionary.
        version (str): Desired version.
        in_place (bool): Whether ``config`` should be modified in-place. Defaults to ``False``.
        alert_missing (bool): Whether to alert if ``config`` may be missing necessary keys. Defaults to ``True``.

    Raises:
        ValueError: Raised if the desired ``version`` is not valid

    Returns:
        Dict: The modified configuration dictionary
    """

    version_names = list(VERSIONS.keys())
    if version not in VERSIONS:
        raise ValueError(f'Provided version {version} is not valid. Choose one of {version_names}.')
    current_version = check_version(config)

    current_idx = version_names.index(current_version)
    new_idx = version_names.index(version)
    if new_idx == current_idx:
        return config
    elif new_idx > current_idx:
        return upgrade_version(config, version, in_place, alert_missing)
    else:
        return downgrade_version(config, version, in_place, alert_missing)


def upgrade_version(config: Dict, version: str, in_place: bool = False, alert_missing: bool = True) -> Dict:
    """Upgrade the configuration dictionary to the desired version.

    Args:
        config (Dict): Trainer Hparams configuration dictionary.
        version (str): Desired version.
        in_place (bool): Whether ``config`` should be modified in-place. Defaults to ``False``.
        alert_missing (bool): Whether to alert if ``config`` may be missing necessary keys. Defaults to ``True``.

    Raises:
        ValueError: Raised if the desired ``version`` is not valid

    Returns:
        Dict: The upgraded configuration dictionary
    """

    version_names = list(VERSIONS.keys())
    if version not in VERSIONS:
        raise ValueError(f'Provided version {version} is not valid. Choose one of {version_names}.')
    current_version = check_version(config)
    # current_version = "prelaunch"

    current_idx = version_names.index(current_version)
    new_idx = version_names.index(version)
    if new_idx <= current_idx:
        return config

    if not in_place:
        config = copy.deepcopy(config)

    for ii in range(current_idx, new_idx + 1):
        version_class = VERSIONS[version_names[ii]]
        config = version_class.upgrade(
            config,
            in_place=True,
            alert_missing=alert_missing,
        )  # already handled in-place above
    return config


def downgrade_version(config: Dict, version: str, in_place: bool = False, alert_missing: bool = True) -> Dict:
    """Downgrade the configuration dictionary to the desired version.

    Args:
        config (Dict): Trainer Hparams configuration dictionary.
        version (str): Desired version.
        in_place (bool): Whether ``config`` should be modified in-place. Defaults to ``False``.
        alert_missing (bool): Whether to alert if ``config`` may be missing necessary keys. Defaults to ``True``.

    Raises:
        ValueError: Raised if the desired ``version`` is not valid

    Returns:
        Dict: The downgraded configuration dictionary
    """

    version_names = list(VERSIONS.keys())
    if version not in VERSIONS:
        raise ValueError(f'Provided version {version} is not valid. Choose one of {version_names}.')
    current_version = check_version(config)

    current_idx = version_names.index(current_version)
    new_idx = version_names.index(version)
    if new_idx >= current_idx:
        return config

    if not in_place:
        config = copy.deepcopy(config)

    for ii in range(current_idx, new_idx - 1, -1):
        version_class = VERSIONS[version_names[ii]]
        config = version_class.downgrade(
            config,
            in_place=True,
            alert_missing=alert_missing,
        )  # already handled in-place above
    return config


VERSION_LIST: List[Type] = [PreLaunch, ComposerV0_2_4, ComposerV0_3_0, ComposerV0_3_2]

VERSIONS = {V.name: V for V in VERSION_LIST}
VERSIONS['latest'] = VERSION_LIST[-1]
