""" Wandb Helpers """
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Optional

from mcli.sweeps.local_sweep_config import LocalRunConfig, RunType
from mcli.sweeps.template import TemplateConfigFactory
from mcli.utils.utils_wandb import get_run_details

if TYPE_CHECKING:
    from wandb.apis.public import Run as WandBRun


def get_wandb_run_config(
    path: Optional[str] = None,
    run: Optional['WandBRun'] = None,
    include_env: bool = False,
    upgrade: bool = False,
) -> LocalRunConfig:
    if path is None and run is None:
        raise ValueError('One of ``path`` or ``run`` must be provided')
    if path is not None and run is not None:
        raise ValueError('Only one of ``path`` or ``run`` can be provided. Got both.')
    if path is not None:
        # Lazy load wandb (0.8s load time)
        import wandb  # pylint: disable=import-outside-toplevel

        # pylint: disable-next=no-member
        api = wandb.Api()
        run = api.run(path)
    assert run is not None
    details = get_run_details(run, include_env=include_env, upgrade=upgrade)
    run_type = RunType.TIMING if details.get('timing_instance') else RunType.CONVERGENCE
    config = {
        'name': details.get('name'),
        'image': details.get('image'),
        'git_repo': details.get('git_repo'),
        'git_branch': details.get('git_branch'),
        'command': details.get('command'),
        'model': details.get('models'),
        'algorithm': details.get('algorithms'),
        'instance': details.get('convergence_instance') or details.get('timing_instance'),
        'run_type': run_type,
        'parameters': details.get('parameters'),
    }
    config = LocalRunConfig.validate(config)
    run_config = LocalRunConfig(**config)

    tcf = TemplateConfigFactory(run_config.model, instance=run_config.instance)
    if run_config.model:
        partial = tcf.build_model_config()
        # Just grab the model's section. can't do this until new merge setting is available
        # TODO (TL): Remove or refactor now that WandB data is uploaded faithfully
        # (https://github.com/mosaicml/mcli/issues/37)
        if not partial.parameters or not partial.parameters.get('model'):
            warnings.warn(
                f'Run {run.id} used an unknown model: {run_config.model}. '
                'Could not import extra model config details.',)
        else:
            assert run_config.parameters is not None
            run_config.parameters['model'] = partial.parameters['model']

    return run_config
