""" Functions for deleting MCLI objects """
import logging
from typing import Dict, List, Optional, Union

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform
from mcli.objects.secrets.platform_secret import PlatformSecret, SecretManager
from mcli.utils.utils_interactive import query_yes_no
from mcli.utils.utils_kube import (delete_config_maps_across_contexts, delete_jobs_across_contexts,
                                   delete_services_across_contexts, get_run_status_from_pod, group_pods_by_job,
                                   list_pods_across_contexts)
from mcli.utils.utils_kube_labels import label
from mcli.utils.utils_logging import FAIL, OK, console
from mcli.utils.utils_string_validation import ensure_rfc1123_compatibility

logger = logging.getLogger(__name__)


def delete_environment_variable(variable_name: str, force: bool = False, **kwargs) -> int:
    del kwargs
    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    existing_env_variables = conf.environment_variables
    new_env_vars = [x for x in existing_env_variables if x.name != variable_name]
    if len(existing_env_variables) == len(new_env_vars):
        print(f'Unable to find env var with name: {variable_name}.'
              ' To see all env vars run `mcli get env`')
        return 1

    if not force:
        confirm = query_yes_no(f'Would you like to delete environment variable {variable_name}?')
        if not confirm:
            print('Canceling deletion.')
            return 1

    conf.environment_variables = new_env_vars
    conf.save_config()
    return 0


def delete_secret(secret_name: str, force: bool = False, **kwargs) -> int:
    """Delete the requested secret from the user's MCLI config and platforms

    Args:
        secret_name: Name of the secret to delete
        force: If True, do not request confirmation. Defaults to False.

    Returns:
        True if deletion was successful
    """
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.error(f'{FAIL} No platforms found. You must have at least 1 platform added before working with secrets.')
        return 1

    # Note, we could just attempt to delete and catch the error.
    # I think it's a bit cleaner to first check if the secret exists, but this will be a bit slower
    # This slowness should be OK for secrets since they are generally small in number

    ref_platform = conf.platforms[0]
    secret_manager = SecretManager(ref_platform)

    to_delete: Dict[str, PlatformSecret] = {}
    for platform_secret in secret_manager.get_secrets():
        if platform_secret.secret.name == secret_name:
            to_delete[platform_secret.secret.name] = platform_secret

    if not to_delete:
        logger.error(f'Unable to find secret with name: {secret_name}.'
                     ' To see all secrets run `mcli get secrets`')
        return 1

    if not force:
        confirm = query_yes_no(f'Would you like to delete secret {secret_name}?')
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion.')
            return 1

    success = []
    with console.status('Deleting secrets...') as status:
        for platform in conf.platforms:
            with MCLIPlatform.use(platform):
                status.update(f'Deleting secrets from {platform.name}...')
                success.extend([ps.delete(platform.namespace) for ps in to_delete.values()])

    if not all(success):
        logger.error(f'{FAIL} Could not delete secret: {secret_name}')
        return 1

    logger.info(f'{OK} Deleted secret: {secret_name}')
    return 0


def delete_platform(platform_name: str, force: bool = False, **kwargs) -> int:
    del kwargs

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    existing_platforms = conf.platforms
    new_platforms = [x for x in existing_platforms if x.name != platform_name]
    if len(existing_platforms) == len(new_platforms):
        print(f'Unable to find platform with name: {platform_name}.'
              ' To see all platforms run `mcli get platforms`')
        return 1
    if not force:
        confirm = query_yes_no(f'Would you like to delete platform {platform_name}?')
        if not confirm:
            print('Canceling deletion.')
            return 1
    conf.platforms = new_platforms
    conf.save_config()
    return 0


def delete_project(project_name: str, **kwargs) -> int:
    del kwargs

    # TODO: Fix projects implementation
    existing_projects = []
    found_projects = [x for x in existing_projects if x.project == project_name]
    if not found_projects:
        print(f'Unable to find project with name: {project_name}.'
              ' To see all projects run `mcli get projects`')
        return 1
    if len(existing_projects) == 1:
        print('Unable to delete the only existing project'
              ' To see all projects run `mcli get projects`')
        return 1
    if found_projects and len(found_projects) == 1:
        found_project = found_projects[0]
        return found_project.delete()

    return 1


def delete_run(name_filter: Optional[List[str]] = None,
               platform_filter: Optional[List[str]] = None,
               status_filter: Optional[List[str]] = None,
               delete_all: bool = False,
               force: bool = False,
               **kwargs):
    del kwargs

    if not (name_filter or platform_filter or status_filter or delete_all):
        logger.error(f'{FAIL} Must specify at least one of --name, --platform, --status, --all.')
        return 1

    if name_filter:
        name_filter = list(map(ensure_rfc1123_compatibility, name_filter))

    try:
        conf = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.error(f'{FAIL} No platforms found. You must have at least 1 platform added before working with runs.')
        return 1

    platforms_to_use = conf.platforms
    if platform_filter:
        platforms_to_use = list(filter(lambda x: x.name in platform_filter, conf.platforms))
        if len(platforms_to_use) == 0:
            logger.error(f'{FAIL} No platforms found matching filter', ','.join(platform_filter))
            return 1

    contexts = [p.to_kube_context() for p in platforms_to_use]

    all_pods, _ = list_pods_across_contexts(contexts=contexts, labels={label.mosaic.JOB: None})
    pod_grouping_by_job = group_pods_by_job(all_pods)

    job_names_to_delete: List[str] = []
    for job_name, pods in pod_grouping_by_job.items():
        if name_filter and job_name not in name_filter:
            continue
        if status_filter:
            run_status = get_run_status_from_pod(pods[0])
            if run_status.value not in status_filter:
                continue
        job_names_to_delete.append(job_name)

    if len(job_names_to_delete) == 0:
        logger.error(f'{FAIL} No jobs found matching the specified criteria.')
        return 1

    labels: Dict[str, Optional[Union[str, List[str]]]] = {label.mosaic.JOB: job_names_to_delete}

    if not force:
        name_string = '\n' + '\n'.join(job_names_to_delete) + '\n'
        run_string = f'{len(job_names_to_delete)} runs' if len(job_names_to_delete) > 1 else 'run'
        confirm_string = f'Would you like to delete the following {run_string}? {name_string}' if len(
            job_names_to_delete) <= 50 else f'Would you like to delete {len(job_names_to_delete)} runs?'
        confirm = query_yes_no(confirm_string)
        if not confirm:
            logger.error(f'{FAIL} Canceling deletion.')
            return 1

    plural = 's' if len(job_names_to_delete) > 1 else ''
    with console.status(f'Deleting run{plural}...') as console_status:
        if not delete_jobs_across_contexts(contexts=contexts, labels=labels):
            console_status.stop()
            logger.error('Job deletion failed')
            return 1

        if not delete_config_maps_across_contexts(contexts=contexts, labels=labels):
            console_status.stop()
            logger.error('Config map deletion failed')
            return 1

        if not delete_services_across_contexts(contexts=contexts, labels=labels):
            console_status.stop()
            logger.error('Service deletion failed')
            return 1

    logger.info(f'{OK} Deleted run{plural}')
    return 0
