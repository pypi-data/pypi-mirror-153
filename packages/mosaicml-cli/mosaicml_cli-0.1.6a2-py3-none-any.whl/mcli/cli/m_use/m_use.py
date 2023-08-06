""" mcli use Entrypoint """
import argparse
from typing import Optional

import yaml

from mcli import config
from mcli.models import ProjectConfig
from mcli.objects.projects.info.project_info import get_projects_list
from mcli.utils.utils_interactive import list_options


def use(
    project: Optional[str] = None,
    branch: Optional[str] = None,
    repo: Optional[str] = None,
    docker: Optional[str] = None,
    **kwargs,
) -> int:
    """The default use command that can modify any parameter of the current
    project

    Each of the passed args are evaluated in sequence and multiple changes to a
    project can be made with one command

    Args:
        project: The string project to switch to
        branch: The branch to switch to
        repo: The repo to use
        docker: The docker image to use
        **kwargs: Catchall

    Returns:
        Returns a cli status code
    """
    del kwargs
    passed_args = {
        'project': project,
        'branch': branch,
        'repo': repo,
        'docker': docker,
    }
    function_map = {
        'project': use_project,
    }

    item_store = list(passed_args.items())
    for key, val in item_store:
        if val is None:
            del passed_args[key]

    if len(passed_args) == 0:
        mock_parser = configure_argparser(parser=argparse.ArgumentParser())
        mock_parser.print_help()
        return 0

    print(f'Passed: \n{yaml.dump(passed_args)}')
    for item, value in passed_args.items():
        function_map[item](value)

    return 0


def use_project(project: Optional[str], **kwargs) -> int:
    del kwargs
    current_project = ProjectConfig.get_current_project()
    all_projects = sorted(get_projects_list(), reverse=True)

    if project:
        match_projects = [x for x in all_projects if x.project.startswith(project)]
        if len(match_projects) == 1:
            matched_project = match_projects[0]
            print(f'Using matching project {matched_project.project} for {project}')
            matched_project.set_current_project()
            return 0

    if current_project in all_projects:
        all_projects.remove(current_project)
    all_projects.insert(0, current_project)

    def print_project(project: ProjectConfig) -> str:
        return f'{project.project} (last used {project.get_last_accessed_string()})'

    new_project = list_options(
        input_text='Which Project would you like to switch to?',
        options=all_projects,
        default_response=all_projects[0],
        pre_helptext='Select the project to switch to',
        helptext=f'default ({all_projects[0].project})',
        print_option=print_project,
    )

    new_project.set_current_project()
    return 0


def use_feature_flag(feature: Optional[str], activate: bool = True, **kwargs) -> int:
    del kwargs
    conf = config.MCLIConfig.load_config()
    available_features = list(config.FeatureFlag)
    available_features_str = [x.value for x in available_features]
    feature_flag: Optional[config.FeatureFlag] = None
    if feature:
        if feature not in available_features_str:
            print(f'Unable to find feature flag: {feature}')
        else:
            feature_flag = config.FeatureFlag[feature]
    if feature_flag is None:
        feature_flag = list_options(
            input_text='What feature would you like to enable?',
            options=available_features,
            print_option=lambda x: x.value,
            helptext='',
        )

    assert feature_flag is not None
    if activate:
        print(f'Activating Feature: {feature_flag.value}')
    else:
        print(f'Deactivating Feature: {feature_flag.value}')
    conf.feature_flags[feature_flag.value] = activate
    conf.save_config()

    return 0


def configure_argparser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=use)

    # TODO (HEK-473): Add back when projects are updated to new spec
    # parser.add_argument(
    #     '-p',
    #     '--project',
    #     help='Switch to a different project',
    #     dest='project',
    #     required=False,
    #     default=None,
    # )

    # project_parser = subparsers.add_parser('project', aliases=['p'], help='Use project')
    # project_parser.add_argument('project', nargs='?', help='The name of the project')
    # project_parser.set_defaults(func=use_project)

    feature_parser = subparsers.add_parser('feature', help='Activate or Deactivate feature flag')
    feature_parser.add_argument('feature', nargs='?', help='The name of the Feature Flag')
    feature_parser.add_argument('--deactivate', action='store_false', dest='activate', help='Deactivate a feature flag')
    feature_parser.add_argument('--activate',
                                action='store_true',
                                default=True,
                                dest='activate',
                                help='Activate a feature flag')
    feature_parser.set_defaults(func=use_feature_flag)
    return parser


def add_use_argparser(subparser: argparse._SubParsersAction,) -> argparse.ArgumentParser:
    """Adds the use parser to a subparser

    Args:
        subparser: the Subparser to add the Use parser to
    """
    use_parser: argparse.ArgumentParser = subparser.add_parser(
        'use',
        aliases=['u'],
        help='Configure your local project',
    )
    use_parser = configure_argparser(parser=use_parser)
    return use_parser
