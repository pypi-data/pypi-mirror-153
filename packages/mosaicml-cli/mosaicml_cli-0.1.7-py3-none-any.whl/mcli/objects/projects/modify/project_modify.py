""" Helper Functions to Modify a Project and Validate Modifications """
from typing import Any, List, Optional

from mcli import config
from mcli.api.projects.get_project import check_if_project_exists
from mcli.objects.projects.info.project_info import get_all_used_images, get_projects_list
from mcli.utils.utils_git import get_git_branch_current, get_git_repo_name, get_git_tags
from mcli.utils.utils_interactive import list_options
from mcli.utils.utils_string_validation import validate_alphanumeric_dash_characters


def configure_project_name(
    name: Optional[str],
    accept_if_valid: bool = False,
) -> str:
    """Helper function to safely interactively configure a Project name

    Args:
        name (Optional[str]): The default project name to pick from
        accept_if_valid (bool): Skip interactive mode if valid default provided

    Returns:
        Returns the valid Project Name
    """
    if name and accept_if_valid and check_if_project_exists(project_name=name):
        return name

    options = [name] if name else []
    existing_project_names = {x.project for x in get_projects_list()}
    while True:
        project = list_options(
            input_text='What do you want to name the project?',
            options=options,
            default_response=name if name else None,
            allow_custom_response=True,
            validate=validate_alphanumeric_dash_characters,
            pre_helptext=None,
        )
        assert isinstance(project, str)
        if project not in existing_project_names:
            if config.feature_enabled(config.FeatureFlag.USE_FEATUREDB):
                # Check FeatureDB if project is already there
                if check_if_project_exists(project):
                    print('Project already exists in FeatureDB')
                    continue
            return project
        print(f'The project name: {project} already exists.  Please choose a unique name')


def configure_docker_image(
    image: Optional[str],
    accept_if_valid: bool = False,
) -> str:
    """Helper function to safely interactively configure a docker image

    Args:
        image (Optional[str]): The default docker image
        accept_if_valid (bool): Skip interactive mode if valid default provided

    Returns:
        Returns the docker image
    """
    if image and accept_if_valid:
        return image

    default_image = 'mosaicml/pytorch'
    possible_images = set([default_image])
    possible_images.update(get_all_used_images())
    if image is None:
        image = default_image
    if image not in possible_images:
        possible_images.add(image)
    possible_images = sorted(list(possible_images))
    image_response = list_options(
        input_text='What docker image do you want?',
        options=possible_images,
        default_response=image,
        allow_custom_response=True,
        validate=validate_alphanumeric_dash_characters,
        pre_helptext='Select your docker image...',
        helptext=f'default ({image})',
    )
    assert isinstance(image_response, str)
    return image_response


def configure_repo(
    repo: Optional[str],
    accept_if_valid: bool = False,
) -> str:
    """Helper function to safely interactively configure which repo to use

    Args:
        repo (Optional[str]): The default repo to use
        accept_if_valid (bool): Skip interactive mode if valid default provided

    Returns:
        Returns the repo string
    """
    if repo and accept_if_valid:
        return repo

    default_repo = 'mosaicml/composer'
    cwd_repo = get_git_repo_name()
    repo_options = set()
    repo_options.add(default_repo)
    default_repo = repo if repo else default_repo
    if repo:
        repo_options.add(repo)
    if cwd_repo:
        repo_options.add(cwd_repo)

    chosen_repo = list_options(
        input_text='What repo?',
        options=list(repo_options),
        default_response=default_repo,
        allow_custom_response=True,
        validate=validate_alphanumeric_dash_characters,
        helptext=f'default ({ default_repo })',
    )
    assert isinstance(chosen_repo, str)
    return chosen_repo


def configure_branch(
    branch: Optional[str],
    current_repo: Optional[str] = None,
    accept_if_valid: bool = False,
) -> str:
    """Helper function to safely interactively configure which branch

    Args:
        branch (Optional[str]): The default branch to use.  If left
              blank, it will use the current working branch
        current_repo ( Optional[str] ): Used to check if the working directory repo matches
           in order to provide smart defaults for branches (if it does match, then use the cwd branch)
        accept_if_valid (bool): Skip interactive mode if valid default provided

    Returns:
        Returns the branch string
    """
    if branch and accept_if_valid:
        return branch

    cwd_branch_tag = get_git_branch_current()
    cwd_repo = get_git_repo_name()
    if cwd_repo != current_repo:
        cwd_branch_tag = None
    branch_options = []
    default_branch = cwd_branch_tag if cwd_branch_tag else 'dev'

    def add_if_not_exists(item: Any, item_list: List[Any]):
        if item not in item_list:
            item_list.append(item)

    add_if_not_exists(cwd_branch_tag, branch_options)
    add_if_not_exists('dev', branch_options)
    add_if_not_exists('main', branch_options)

    if cwd_repo == current_repo:
        all_tags = get_git_tags()
        for tag in all_tags:
            add_if_not_exists(tag, branch_options)

    chosen_branch = list_options(
        input_text='What branch?',
        options=branch_options,
        default_response=default_branch,
        allow_custom_response=True,
        validate=validate_alphanumeric_dash_characters,
        helptext=f'default ({ default_branch })',
    )
    assert isinstance(chosen_branch, str)
    return chosen_branch
