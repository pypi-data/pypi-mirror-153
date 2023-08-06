# type: ignore

""" Sweep helper objects """
# pylint: skip-file
# type
from __future__ import annotations

import itertools
import logging
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from mcli.serverside.job.mcli_job import MCLIJob
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.serverside.runners.runner import Runner
from mcli.sweeps.config_backend import ConfigBackend, get_default_backend
from mcli.sweeps.inheritance import extract_only_item_from_dict, merge
from mcli.sweeps.local_sweep_config import LocalRunConfig, LocalSweepConfig, RunType
from mcli.sweeps.search import grid_search
from mcli.sweeps.template import TemplateConfigFactory
from mcli.utils.utils_config import format_jinja, get_unique_name
from mcli.utils.utils_types import convert_dict_to_single_item_lists

logger = logging.getLogger(__name__)


def submit_run(
    local_run_config: LocalRunConfig,
    priority_class: Optional[str] = None,
    experimental_flags: Optional[List[ExperimentalFlag]] = None,
    environment_variables: Optional[Dict[str, str]] = None,
    ports: Optional[List[int]] = None,
):
    """Submit a run through the k8s submission pipeline.

    Args:
        config: The ``RunConfig`` for the run to be submitted.
        attach_ebs: True if the run should attempt to attach EBS. Defaults to False.
        priority_class: The priority at which the run should be scheduled. Not all platforms
            support priority values. If you attempt to set a priority value that is not supported, a ``ValueError``
            will be thrown. Defaults to None.
        experimental_flags: A list of experimental flags to enable,
            if the instance allows them. Defaults to None.
        environment_variables: Environment variables to add. Defaults to None.
        ports: Ports to open on the container. Defaults to None.
    """
    logger.debug('Submitting run group...')

    parameters = local_run_config.parameters or {}
    environment_variables = environment_variables or {}
    ports = ports or []

    assert local_run_config.name is not None
    assert local_run_config.image is not None
    assert local_run_config.command is not None

    mcli_job = MCLIJob(
        name=local_run_config.name,
        command=[local_run_config.command],
        container_image=local_run_config.image,
        parameters=parameters,
        environment_variables=environment_variables,
        ports=ports,
    )
    runner = Runner()
    assert local_run_config.instance is not None

    #TODO: Re-attach


def _ensure_list(x: Any) -> List[Any]:
    if not isinstance(x, list):
        x = [x]
    return x


class Collection(object):
    """ A Collection to help prepopulate yamls """

    def __init__(
        self,
        local_config: LocalSweepConfig,
        fork_config: Optional[LocalRunConfig] = None,
        backend: Optional[ConfigBackend] = None,
    ) -> None:
        self.name = local_config.name or (fork_config and fork_config.name)
        if self.name is None:
            raise ValueError('Sweep config must be given a name. Got None.')
        self.config = local_config
        if fork_config is None:
            fork_config = LocalRunConfig()
        self.fork_config = fork_config
        if backend is None:
            backend = get_default_backend()
        self.backend = backend

    @staticmethod
    def _zip_longest(*args):
        args = tuple(_ensure_list(a) for a in args)
        max_len = max([len(a) for a in args])
        its = [list(itertools.islice(itertools.cycle(a), max_len)) for a in args]
        for t in zip(*its):
            yield t

    def _create_user_configs(self) -> List[LocalRunConfig]:
        assert isinstance(self.config, LocalSweepConfig)
        user_configs: List[LocalRunConfig] = []
        models = self.config.models or [None]
        algorithms = self.config.algorithms or [None]
        grid_configs = list(itertools.product(models, algorithms))
        grid = self.config.grid or {}
        parameters = self.config.parameters or {}

        assert isinstance(self.name, str)

        for model, algo_set in grid_configs:
            for search_params in grid_search(grid):
                search_params = convert_dict_to_single_item_lists(
                    search_params,
                    ['algorithms', 'callbacks', 'loggers', 'schedulers'],
                )
                search_params = merge(search_params, parameters)
                user_configs.append(
                    LocalRunConfig(
                        name=get_unique_name(self.name),
                        model=model,
                        algorithm=algo_set,
                        instance=self.config.instance,
                        run_type=self.config.run_type,
                        git_repo=self.config.git_repo,
                        git_branch=self.config.git_branch,
                        image=self.config.image,
                        command=self.config.command,
                        parameters=search_params,
                        sweep=self.name,
                        project=self.config.project,
                    ))

        return user_configs

    def get_run_configs(self):
        run_configs = []
        user_configs = self._create_user_configs()
        for user_config in user_configs:
            run_config = resolve_full_run_config(
                user_config,
                self.fork_config.copy(),
                self.backend,
            )
            run_configs.append(run_config)
        return run_configs


def resolve_full_run_config(
    user_config: LocalRunConfig,
    fork_config: Optional[LocalRunConfig] = None,
    backend: Optional[ConfigBackend] = None,
) -> LocalRunConfig:
    """Fully resolves a ``RunConfig`` from a user-provided config and a forked config, with all details filled in.

    Creates a fully-resolved ``RunConfig`` by:
        1. Filling in all user-provided details with values from the default templates (e.g. algorithm or model configs)
        2. Merging this detailed config with values from the fork, with user-provided values taking priority
        3. Adding remaining WandB logging data
        4. Formatting the final 'command' using jinja
        5. Removing all jinja-only variables (ie those starting with '_') from the parameters dictionary
        6. Converting necessary keys in parameters dictionary to lists of single-item dictionaries

    Args:
        user_config (RunConfig): Partially-resolved ``RunConfig`` from user-provided data
        fork_config (Optional[RunConfig], optional): Partially-resolved ``RunConfig`` from a forked run.
            Defaults to None.
        backend (Optional[ConfigBackend], optional): Controller for accessing template values from
            configuration storage. Defaults to the backend returned by ``get_default_backend()``.

    Returns:
        RunConfig: A fully-resolved ``RunConfig``
    """
    if fork_config is None:
        fork_config = LocalRunConfig()

    # Fill in run_type with CONVERGENCE if not specified
    # TODO (TL): Remove in when run_type is guaranteed (HEK-80)
    if user_config.run_type is None and fork_config.run_type is None:
        user_config.run_type = RunType.CONVERGENCE

    # Fill in config values and merge
    local_config = merge_config_with_fork_config(user_config, fork_config, backend)

    # Format command with Jinja
    command = local_config.command or ''
    command = format_jinja(command, asdict(local_config))
    local_config.command = command

    # Remove '_' prefixed keys from 'parameters'
    if local_config.parameters:
        local_config.parameters = {k: v for k, v in local_config.parameters.items() if not k.startswith('_')}

    # Convert final config to list of single-item dicts
    # TODO (TL): This assert can be removed with move to a fully-required RunConfig (HEK-80)
    assert isinstance(local_config.parameters, dict)
    local_config.parameters = convert_dict_to_single_item_lists(
        local_config.parameters,
        ['algorithms', 'callbacks', 'loggers', 'schedulers'],
    )

    return local_config


def merge_config_with_fork_config(
    user_config: LocalRunConfig,
    fork_config: LocalRunConfig,
    backend: Optional[ConfigBackend] = None,
) -> LocalRunConfig:
    """Merges a user config and forked config, filling in missing details

    Args:
        user_config (RunConfig): Partially filled ``RunConfig`` provided by the user
        fork_config (RunConfig): Partially filled ``RunConfig`` forked from a pre-existing run
        backend (Optional[ConfigBackend]): Config backend. Defaults to the backend returned by
                                           ``get_default_backend()``.

    Returns:
        RunConfig: Merged ``RunConfig``
    """

    tcf = TemplateConfigFactory(model=user_config.model,
                                algorithms=user_config.algorithm,
                                instance=user_config.instance,
                                run_type=user_config.run_type,
                                loggers=None,
                                backend=backend)
    template_configs = []
    user_specified = user_config.model is not None
    is_different = user_config.model != fork_config.model
    if user_specified and is_different:
        partial_config = tcf.build_model_config()
        template_configs.append(partial_config)

    user_specified = user_config.algorithm is not None
    is_different = user_config.algorithm != fork_config.algorithm
    if user_specified and is_different:
        partial_config = tcf.build_algorithms_config()

        # Merge with existing hyperparameters from fork_config
        if fork_config.parameters is not None:
            # TODO (TL): Provide better guarantees earlier in the pipeline that forked runs are valid
            # https://github.com/mosaicml/mosaicml-cli/issues/53
            assert 'algorithms' in fork_config.parameters, 'Forked run configuration is not valid'

            # TODO (TL): Convert configs to nested dicts first and back to single-item lists just before submission
            # https://github.com/mosaicml/mosaicml-cli/issues/54

            # List-based algorithms
            if isinstance(fork_config.parameters['algorithms'], list):
                keep = []
                for item in fork_config.parameters['algorithms']:
                    k, _ = extract_only_item_from_dict(item)
                    if k in user_config.algorithm:
                        keep.append(item)
            # Dict-based algorithms
            else:
                keep = {}
                for k in fork_config.parameters['algorithms']:
                    if k in user_config.algorithm:
                        keep[k] = fork_config.parameters['algorithms'][k]
            del fork_config.parameters['algorithms']

            partial_config.parameters = merge({'algorithms': keep}, partial_config.parameters)  #type: ignore
        template_configs.append(partial_config)

    # Add instance config data
    user_specified = user_config.instance is not None
    is_different = user_config.instance != fork_config.instance
    if user_specified and is_different:
        template_configs.append(tcf.build_instance_config())

    # Add callback config data for the run type
    user_specified = user_config.run_type is not None
    is_different = user_config.run_type != fork_config.run_type
    if user_specified and is_different:
        partial_config = tcf.build_run_type_config()
        if fork_config.parameters is not None and 'callbacks' in fork_config.parameters:
            del fork_config.parameters['callbacks']
        template_configs.append(partial_config)

    # Add logging config data
    template_configs.append(tcf.build_loggers_config())

    merged = user_config
    merged.resolve()
    for override in reversed(template_configs):
        merged = LocalRunConfig.merge(merged, override, 'overlay')
    if fork_config is not None:
        merged = LocalRunConfig.merge(merged, fork_config, 'overlay')
    merged = LocalRunConfig(**LocalRunConfig.validate(asdict(merged)))

    return merged
