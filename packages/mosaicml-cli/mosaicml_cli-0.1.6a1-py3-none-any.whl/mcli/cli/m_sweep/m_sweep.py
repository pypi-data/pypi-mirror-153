# type: ignore

""" mcli sweep Entrypoint """
# pylint: skip-file

from __future__ import annotations

import argparse
import functools
import json
import logging
import sys
import textwrap
from argparse import ArgumentParser
from contextlib import contextmanager
from dataclasses import asdict
from pathlib import Path
from signal import SIGINT
from typing import Any, List, Optional, Union

import yaml
from rich import print as rprint
from rich.progress import track
from yaspin import yaspin
from yaspin.core import Yaspin

from mcli.models import ProjectConfig
from mcli.serverside.platforms.experimental import ExperimentalFlag
from mcli.sweeps.config_backend import MCLIConfigBackend, get_default_backend
from mcli.sweeps.local_sweep_config import LocalRunConfig, LocalSweepConfig, RunType
from mcli.sweeps.objects import Collection, submit_run
from mcli.sweeps.run_names import (ALL_RUN_TEMPLATES, SIMPLE_RUN_TEMPLATES, RunTemplate, format_run_name,
                                   format_run_name_helper, get_run_format_options)
from mcli.sweeps.wandb import get_wandb_run_config
from mcli.utils.utils_composer import check_valid_hparams
from mcli.utils.utils_interactive import list_options, prompt, query_yes_no
from mcli.utils.utils_logging import OK
from mcli.utils.utils_rich import dict_to_tree, diff_dict_to_tree
from mcli.utils.utils_types import get_hours_type

logger = logging.getLogger(__name__)

ok_prefix = '✅ '
fail_prefix = '💥 '

_MAX_DEBUG_DURATION: float = 8


class NullYaspin:
    """ Context management for yaspin """

    text: str

    def ok(self, *args, **kwargs):
        del args
        del kwargs
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        return False

    @contextmanager
    def hidden(self):
        yield

    def start(self):
        pass

    def stop(self):
        pass

    def write(self, *args, **kwargs):
        del args
        del kwargs
        pass


def int_handler(signum, frame, spinner: Yaspin):
    """SIGINT handler function for yaspin

    Args:
        signum (_type_): Unused
        frame (_type_): Unused.
        spinner (Yaspin): The spinner that needs SIGINT handling

    Raises:
        KeyboardInterrupt: Re-raised after handling
    """
    del signum
    del frame

    spinner.text = 'Canceled!'
    spinner.fail(fail_prefix)
    spinner.stop()
    raise KeyboardInterrupt


def _validate_hours(value: Union[str, float], max_value: float = _MAX_DEBUG_DURATION) -> float:
    """Validate that the provided value is an float between 1 and `max_value`
    """
    float_value: float = float(value)
    if float_value <= 0 or float_value > max_value:
        raise ValueError(
            f'The value for `--hours` must be a float between 0 and {max_value}, but {float_value} was specified. '
            'Please specify a value within this range.')
    return float_value


def run_sweep(**kwargs) -> int:
    main(**kwargs)

    return 0


def add_sweep_argparser(subparser: argparse._SubParsersAction) -> None:
    sweep_parser: argparse.ArgumentParser = subparser.add_parser(
        'sweep',
        aliases=['s'],
        help='Sweep stuff',
    )
    sweep_parser.set_defaults(func=run_sweep)
    _configure_parser(sweep_parser)


def _configure_parser(parser=None):
    if parser is None:
        parser = ArgumentParser()

    config_ = parser.add_argument_group('Run configuration')
    config_.add_argument('--name', help='Name of the sweep to run. Each individual run name will be based off of this.')
    config_.add_argument('-f',
                         '--file',
                         help='File from which to load arguments.'
                         'Arguments present in the file can be overridden by the command line.')
    config_.add_argument('-m', '--model', '--models', dest='models', nargs='*', default=None, help='Model(s) to run')
    config_.add_argument('--algorithms',
                         dest='algorithms',
                         default=None,
                         nargs='+',
                         help='Algorithm or list of algorithms to run')
    config_.add_argument('--instance', dest='instance', help='Compute instance to use for all runs')
    config_.add_argument('--run-type',
                         dest='run_type',
                         type=lambda x: RunType[x.upper()],
                         choices=list(RunType),
                         metavar=f"{{{','.join([rt.value for rt in RunType])}}}",
                         help='The class of run you want to perform')
    config_.add_argument('--grid', default=None, type=json.loads, help='Parameters to grid search, in JSON format')
    config_.add_argument('--parameters',
                         default=None,
                         type=json.loads,
                         help='Default parameters to include in every run in JSON format')
    config_.add_argument('--git-branch', help='Commit/branch/tag to use in the clone')
    config_.add_argument('--git-repo', help='Which repo to clone')
    config_.add_argument('--image', dest='image', help='Docker image to use')
    config_.add_argument('--command',
                         help='Command to use for each run group. The command can be provided as a string or a path to '
                         'a shell script. Additionally, it can contain placeholder values that will be formatted using '
                         'Jinja')
    config_.add_argument('--wandb-project', help='Name of the W&B project in which to store results')
    config_.add_argument('--named-like',
                         help='Run name template. This can be provided as a string or as a path to a '
                         'file. It should contain placeholders that will be filled in with values from the run '
                         'configuration using Jinja. Run names will be trimmed to <= 58 characters and a unique ID '
                         'will be appended.')

    fork_ = parser.add_argument_group('Run forking')
    fork_.add_argument('--from-run', help='Initialize hyperparameters to those from the specified run')
    fork_.add_argument('--include-env',
                       action='store_true',
                       help='Include environment details from forked run (e.g. docker image, git repo and commit)')
    fork_.add_argument('--upgrade',
                       action='store_true',
                       help='Upgrade the composer configuration to the latest dev before submission')

    output_ = parser.add_argument_group('Output configuration')

    output_.add_argument('--output-directory', help='Directory in which individual mcli run configs will be written')
    output_.add_argument('-o',
                         '--output',
                         choices=('yaml', 'json', 'tree'),
                         help='Format in which to print each generated run configuration on stdout')
    output_.add_argument('--plain', action='store_true')

    interactive_ = parser.add_argument_group('Interactive')
    interactive_.add_argument(
        '--no-input',
        action='store_true',
        help='Disables all interactivity. If required inputs are not provided, an error will be thrown.')
    interactive_.add_argument('--query-defaults',
                              action='store_true',
                              help='Ask to use defaults from project configuration before using them')
    interactive_.add_argument('-y',
                              '--no-confirm',
                              dest='confirm',
                              action='store_false',
                              help='Do not request confirmation. True by default if --no-input is passed.')

    # Submission checks
    parser.add_argument('--debug',
                        action='store_true',
                        help='Run a debug pod. Instead of running its regular command the pod will simply sleep. This '
                        "lets you 'exec' into it to interact with the environment and run your code manually for "
                        'debugging purposes. The pod will live for a duration specified by the --hours argument, '
                        'default 1 hour.')
    parser.add_argument('--hours',
                        type=get_hours_type(_MAX_DEBUG_DURATION),
                        default=1,
                        help='If `--debug` is specified, this sets the number of hours that the run pod will be '
                        f'kept alive. The maximum value is {_MAX_DEBUG_DURATION}. Default %(default)s.')
    parser.add_argument('--dry-run', action='store_true', help='Do not submit any runs, just generate run configs')
    parser.add_argument('--validate-composer',
                        action='store_true',
                        help='Validate the final hparams with the local install of composer before submitting')
    parser.add_argument('--no-composer',
                        action='store_true',
                        help='Do not attempt to use local composer for inferring configuration details')

    # Scheduling
    parser.add_argument('--priority',
                        choices=('low', 'standard', 'high'),
                        help='Priority level at which runs should be submitted. '
                        'This is currently only valid for the R1Z1 cluster. (default None)')
    parser.add_argument('--num-nodes',
                        type=int,
                        default=None,
                        help='Number of parallel runs to submit for multinode runs. Default is None, '
                        'which indicates a single-node run.')

    # Platform flags
    parser.add_argument(
        '--experimental',
        choices=ExperimentalFlag.permitted(),
        type=ExperimentalFlag,
        nargs='+',
        default=None,
        metavar='FLAG',
        help=
        'Enable one or more experimental flags. These flags are designed to take advantage of a specific feature that '
        'may still be too experimental for long-term inclusion in mcli.')

    return parser


def get_args(argv: Optional[List[str]] = None):

    parser = _configure_parser()
    args = parser.parse_args(argv)
    return args


def get_default_image():
    proj = ProjectConfig.get_current_project()
    return proj.image


def get_default_repo():
    proj = ProjectConfig.get_current_project()
    repo_name = proj.repo
    # TODO (TL): Validate this data properly
    if 'github.com' not in repo_name:
        repo_name = f'https://github.com/{repo_name}'
    return repo_name


def get_default_commit():
    proj = ProjectConfig.get_current_project()
    return proj.branch


def get_default_project():
    proj = ProjectConfig.get_current_project()
    return proj.project


def get_default_command():
    path = Path(__file__).parents[3].joinpath('mcli-yamls', 'defaults', 'command.sh')
    with open(path, 'r', encoding='utf-8') as fh:
        cmd = fh.read()
        if cmd != '':
            return cmd
    return None


DEFAULT_CMDS = {
    'name': lambda: None,
    'image': get_default_image,
    'git_repo': get_default_repo,
    'git_branch': get_default_commit,
    'command': get_default_command,
    'project': get_default_project,
}

# Map of R1Z1 priorities to more generic names.
# It might make sense to generalize this as more clusters come online with prioritization support.
_PRIORITY_MAP = {'low': 'scavenge', 'standard': 'standard', 'high': 'emergency'}


def choose_one_of_many(options: List[Any], title: str = 'Choose one', allow_none=False, **kwargs) -> str:
    if allow_none:
        options.insert(0, 'None')
    response = list_options(title, options, multiple_ok=False, **kwargs)
    if response == 'None':
        response = None
    return response  # type: ignore


def choose_many_of_many(options: List[Any], title: str = 'Choose several', allow_none=False, **kwargs) -> List[str]:
    if allow_none:
        options.insert(0, 'None')
    response = list_options(title, options, multiple_ok=True, **kwargs)
    if response == ['None']:
        response = None
    return response  # type: ignore


# TODO: Refactor and fix statement complexity
# pylint: disable-next=too-many-statements
def main(
    name: Optional[str] = None,
    image: Optional[str] = None,
    git_repo: Optional[str] = None,
    git_branch: Optional[str] = None,
    command: Optional[str] = None,
    models: Optional[List[str]] = None,
    algorithms: Optional[List[List[str]]] = None,
    instance: Optional[str] = None,
    run_type: Optional[RunType] = None,
    grid: Optional[List[str]] = None,
    parameters: Optional[List[str]] = None,
    project: Optional[str] = None,
    file: Optional[str] = None,
    plain: bool = False,
    dry_run: bool = False,
    confirm: bool = True,
    validate_composer: bool = False,
    output: Optional[str] = None,
    output_directory: Optional[str] = None,
    from_run: Optional[str] = None,
    query_defaults: bool = False,
    no_input: bool = False,
    include_env: bool = False,
    upgrade: bool = False,
    debug: bool = False,
    priority: Optional[str] = None,
    no_composer: bool = False,
    hours: float = 1,
    experimental: Optional[List[ExperimentalFlag]] = None,
    num_nodes: Optional[int] = None,
    named_like: Optional[str] = None,
    **kwargs,
):
    del kwargs

    def validate_response(attr, choice):
        return LocalSweepConfig.validate({attr: choice})[attr]

    # Validate arguments
    hours = get_hours_type(_MAX_DEBUG_DURATION)(hours)

    priority_class: Optional[str] = None
    if priority is not None:
        if priority not in _PRIORITY_MAP:
            raise ValueError(f'`priority` must be one of {list(_PRIORITY_MAP.keys())}, not {priority}.')
        priority_class = _PRIORITY_MAP[priority]

    logger.info(
        textwrap.dedent("""
    ------------------------------------------------------
    Let's run this sweep
    ------------------------------------------------------
    """))

    if not plain:
        sp = yaspin(sigmap={SIGINT: int_handler})
    else:
        sp = NullYaspin()

    # Import config from file
    file_config = None
    if file:
        sp.text = f'Loading configuration from file: {file}'
        with sp.hidden():
            file_config = LocalSweepConfig.load(file)
            logger.debug(dict_to_tree(asdict(file_config), title=str(Path(file).name)))
        sp.text = f'Loaded configuration from file: {file}'
        sp.ok(ok_prefix)

    # If command is provided as a path, read it into a string
    if command is not None:
        if Path(command).exists():
            with open(Path(command), 'r', encoding='utf8') as fh:
                command = fh.read()

    # If named_like is provided as a path, read it into a string
    if named_like and Path(named_like).exists():
        with open(Path(named_like), 'r', encoding='utf8') as fh:
            named_like = fh.read()

    # Import config from CLI args
    args_config = {
        'name': name,
        'image': image,
        'git_repo': git_repo,
        'git_branch': git_branch,
        'command': command,
        'models': models,
        'algorithms': algorithms,
        'instance': instance,
        'run_type': run_type,
        'grid': grid,
        'parameters': parameters,
        'project': project,
        'named_like': named_like,
    }
    args_config = LocalSweepConfig.validate(args_config)
    config = LocalSweepConfig(**args_config)
    with sp.hidden():
        logger.debug('Command-line arguments:')
        logger.debug(dict_to_tree(asdict(config), title='CLI'))

    # Overlay CLI config on file config
    if file_config is not None:
        config = LocalSweepConfig.merge(config, file_config)
        assert isinstance(config, LocalSweepConfig)  # Fix typing inference
        if asdict(config) != asdict(file_config):
            sp.text = 'Merged command-line and file configurations'
            sp.ok(ok_prefix)

    # If clone/forking previous run, do that here and merge configs
    if from_run:
        sp.text = f'Forking run {from_run}'
        with sp:
            sp.start()
            run_config = get_wandb_run_config(from_run, include_env=include_env, upgrade=upgrade)
        sp.text = f'Downloaded config from run: {from_run}'
        sp.ok(ok_prefix)
    else:
        run_config = LocalRunConfig()

    # Fill in remaining fields
    for attr in ('name', 'image', 'git_repo', 'git_branch', 'command', 'project'):
        config_val = getattr(config, attr)
        run_val = getattr(run_config, attr)
        if (config_val is None) and (run_val is None):
            default_val = DEFAULT_CMDS[attr]()
            with sp.hidden():
                if not no_input:
                    if query_defaults or default_val is None:
                        config_val = prompt(
                            f"Please provide {'an' if attr[0] in 'aeiou' else 'a'} {attr}:",
                            default=default_val,
                        )
                    else:
                        config_val = default_val
                    config_val = validate_response(attr, config_val)
                    logger.debug(f"Using {attr.replace('_', ' ')}(s): {config_val}")
                    setattr(config, attr, config_val)
                elif default_val is not None:
                    logger.debug(f"Using default value for {attr.replace('_', '-')}(s): {default_val}")
                    setattr(config, attr, default_val)
                else:
                    raise RuntimeError(f'No {attr} was provided. This is required. '
                                       f"Please re-submit with the --{attr.replace('-', '_')} argument.")

    backend = MCLIConfigBackend() if no_composer else get_default_backend()

    # Get values that may require additional configuration
    # Get the model(s) to run
    sp.text = 'Verifying that all required details are provided.'
    if (config.models is None) and (run_config.model is None):
        default_val = None  # Stub for possible project-specific defaults
        with sp.hidden():
            if not no_input:
                if query_defaults or default_val is None:
                    logger.debug('No models specified. Querying...')
                    model_options = backend.list_models()
                    choice = choose_many_of_many(model_options, 'Choose a set of models to run')
                else:
                    choice = default_val
                choice = validate_response('models', choice)
                logger.debug(f'Using model(s): {choice}')
                config.models = choice
            elif default_val is not None:
                default_val = validate_response('models', default_val)
                logger.debug(f'Using default value for model(s): {default_val}')
                config.models = default_val
            else:
                raise RuntimeError('No model was provided. Please re-submit with the --models argument')

    # Get algorithms to run for the model(s)
    if (config.algorithms is None) and (run_config.algorithm is None):
        with sp.hidden():
            logger.debug('No algorithms argument')
            if not no_input:
                logger.debug('No algorithms were specified. Querying...')
                # query algorithms
                algo_options = backend.list_algorithms()
                choice = choose_many_of_many(
                    algo_options,
                    'Choose a set of algorithms to use, if any',
                    allow_none=True,
                    default_response='None',
                    helptext=f'default ({ None })',
                )
                if choice is not None:
                    choice = validate_response('algorithms', choice)
                    logger.debug(f'Using algorithm(s): {choice}')
                    config.algorithms = choice

    # Finally, get instance values
    instance_options = None
    if config.instance is None and run_config.instance is None:
        if config.models is not None:
            models = config.models
        elif run_config.model is not None:
            models = [run_config.model]
        else:
            raise RuntimeError('No model was provided. Please re-submit with the --models argument')
        assert models is not None
        with sp.hidden():
            logger.debug('No instances specified. Querying...')
            no_instance = True
            if not no_input:
                instance_options = set(backend.list_instances(models[0]))
                for model in models[1:]:
                    instance_options = instance_options.intersection(backend.list_instances(model))
                instance_options = sorted(list(instance_options))
                choice = choose_one_of_many(
                    instance_options,
                    'Which instance would you like to run on?',
                    allow_none=False,
                )
                if choice is not None:
                    no_instance = False
                    choice = validate_response('instance', choice)
                    sp.write(f'instance: {choice}')
                    logger.debug(f'Using instance: {choice}')
                    config.instance = choice
            if no_instance:
                RuntimeError('No instances were requested. You must specify an instance with --instance')

    sp.text = 'All required details have been provided'
    sp.ok(ok_prefix)
    if asdict(config) != {}:
        with sp.hidden():
            logger.debug(dict_to_tree(asdict(config), title='Sweep configuration:'))

    if file_config is not None:
        assert file is not None  # Only way to get file_config not None is if this is True
        if asdict(config) != asdict(file_config):
            with sp.hidden():
                logger.debug(
                    diff_dict_to_tree(
                        asdict(config),
                        asdict(file_config),
                        title=f'Difference from file {Path(file).name}:',
                    ))

    if from_run:
        run_as_sweep = run_config.to_sweep_config()
        if asdict(config) != asdict(run_as_sweep):
            with sp.hidden():
                logger.debug(
                    diff_dict_to_tree(
                        asdict(LocalSweepConfig.merge(config, run_as_sweep, 'overlay')),
                        asdict(run_as_sweep),
                        title=f'Difference from run {from_run}:',
                    ))

    sp.text = 'Generating run configurations for the sweep'
    with sp:
        sp.start()
        collection = Collection(local_config=config, fork_config=run_config, backend=backend)
        run_configs = collection.get_run_configs()
    sp.text = f'Generated {len(run_configs)} run configurations.'
    sp.ok(ok_prefix)

    if validate_composer:
        sp.text = 'Attempting to validate configs with local composer install'
        for rconfig in track(run_configs):
            is_valid, e = check_valid_hparams(rconfig)
            if not is_valid:
                logger.error('Run was not a valid hparams for the currently install composer!')
                logger.error(yaml.safe_dump(rconfig.to_json()))
                assert isinstance(e, Exception)
                raise e
        sp.text = 'Validated all run configurations against local composer'
        sp.ok(ok_prefix)

    # Format run names
    grid_parameters = list(config.grid.keys()) if config.grid else []
    if not config.named_like and not no_input:
        format_options = get_run_format_options(run_configs[0], search_parameters=grid_parameters)
        templates = ALL_RUN_TEMPLATES if grid_parameters else SIMPLE_RUN_TEMPLATES
        print_option = functools.partial(
            format_run_name_helper,
            formatters=format_options,
        )
        _description = textwrap.dedent("""
            You can format your run names based on their configuration. Formatting is
            done through Jinja templating, which you can control using the `--named-like`
            argument or `named_like:` key in a supplied YAML file. Below are a few options
            you can choose from if you don't want to supply your own.

            Examples for your first run:
        """)
        run_template = list_options(
            'How would you like your run names formatted?',
            templates,
            allow_custom_response=True,
            default_response=templates[0],
            pre_helptext=_description,
            helptext='Enter a number or your own Jinja template',
            print_option=print_option,
        )
        config.named_like = run_template.template if isinstance(run_template, RunTemplate) else run_template

    if config.named_like:
        for rconfig in run_configs:
            rconfig.name = format_run_name(RunTemplate.from_string(config.named_like),
                                           get_run_format_options(rconfig, search_parameters=grid_parameters))

    if output_directory is not None:
        output_directory_path = Path(output_directory)
        output_directory_path.mkdir(parents=True, exist_ok=True)
        for ii, rconfig in enumerate(run_configs):
            fname = rconfig.name or f'{config.name}-{ii}'
            rconfig.dump(output_directory_path.joinpath(f'{fname}.yaml'))

    if output:
        for ii, rconfig in enumerate(run_configs):
            data = rconfig.to_json()
            print('')
            if output == 'yaml':
                print(yaml.safe_dump(data))
            elif output == 'json':
                print(json.dumps(data))
            elif output == 'tree':
                rprint(dict_to_tree(data))

    if debug:
        debug_command = f'sleep {int(3600 * hours)}'
        logger.info(f"A 'debug' run was requested - restricting to a single run with command {debug_command}")
        run_configs = run_configs[:1]
        logger.info('Original command was:')
        logger.info(run_configs[0].command)
        run_configs[0].command = debug_command

    environment_variables = {}
    ports = []
    if num_nodes:
        logger.info('Creating a multi-node run. Currently only a single multi-node run can be created at a time. '
                    'Restricting a single run.')
        _PORT = 5000  # pylint: disable=invalid-name
        environment_variables.update({
            'WORLD_SIZE': str(num_nodes),
            'RANK': '0',
            'MASTER_PORT': str(_PORT),
        })
        ports.append(_PORT)

    run_names = []
    if not dry_run:
        if confirm and not no_input:
            confirm = query_yes_no('Do you want to submit?')
            if not confirm:
                logger.error('Canceling!')
                sys.exit(1)
        for rconfig in track(run_configs):
            # TODO: Readd
            # wandb_envs = get_wandb_env_vars(rconfig)
            # environment_variables.update(wandb_envs)
            submit_run(rconfig,
                       priority_class=priority_class,
                       experimental_flags=experimental,
                       environment_variables=environment_variables,
                       ports=ports)
            # TODO: Run names
            # run_names.append(group_runs)
        logger.info(f'{OK} Submitted!')

    return run_configs, run_names
