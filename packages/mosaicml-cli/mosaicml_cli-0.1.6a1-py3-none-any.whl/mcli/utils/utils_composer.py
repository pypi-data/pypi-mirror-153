"""Composer Utils for validating composer configs"""
import copy
from pathlib import Path
from typing import Optional, Tuple

from mcli.config import COMPOSER_INSTALLED
from mcli.sweeps.local_sweep_config import LocalRunConfig


def is_composer_installed() -> bool:
    """Returns `True` if the `composer` library is installed.
    """
    return COMPOSER_INSTALLED


def assert_composer_installed():
    """Raises an `ImportError` if `composer` is not installed.
    """
    if not COMPOSER_INSTALLED:
        raise ImportError('Could not find composer library. Please install it using `pip install mosaicml`.')


def get_composer_directory() -> Path:
    """Returns the directory path for `composer`, if installed.

    Returns:
        Path: path to `composer` root directory
    """
    assert_composer_installed()

    # pylint: disable-next=import-outside-toplevel
    import composer  # type: ignore
    return Path(composer.__file__).parents[0]


def check_valid_hparams(run_config: LocalRunConfig) -> Tuple[bool, Optional[Exception]]:
    """Checks if the `RunConfig` produces a valid composer `Trainer`

    Args:
        run_config (RunConfig): `RunConfig` with composer `Trainer` hparams specfied in the `parameters` attribute

    Returns:
        Tuple[bool, Optional[Exception]]: If valid, returns True, None. Otherwise, False and the raised exception
    """
    assert_composer_installed()

    # pylint: disable-next=import-outside-toplevel
    from composer.trainer.trainer_hparams import TrainerHparams  # type: ignore

    config = copy.deepcopy(run_config.parameters)
    try:
        _ = TrainerHparams.create(data=config, cli_args=False)
        return True, None
    except Exception as e:  # TODO (TL): make this more specific (HEK-124) pylint: disable=broad-except
        return False, e
