""" mcli create secret Entrypoint """
import argparse
import logging
from typing import Callable, Optional

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform, MCLISecret, SecretType
from mcli.objects.secrets.create.docker_registry import DockerSecretCreator
from mcli.objects.secrets.create.generic import EnvVarSecretCreator, FileSecretCreator
from mcli.objects.secrets.create.s3 import S3SecretCreator
from mcli.objects.secrets.create.ssh import SSHSecretCreator
from mcli.objects.secrets.platform_secret import PlatformSecret, SecretManager
from mcli.utils.utils_interactive import InputDisabledError, ValidationError, input_disabled
from mcli.utils.utils_logging import FAIL, OK, console

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete secret. Please provide a name, key and value if running with '
                          '`--no-input`. Check `mcli create env --help` for more information.')

CREATORS = {
    SecretType.docker_registry: DockerSecretCreator,
    SecretType.environment: EnvVarSecretCreator,
    SecretType.mounted: FileSecretCreator,
    SecretType.ssh: SSHSecretCreator,
    SecretType.git: SSHSecretCreator,
    SecretType.s3_credentials: S3SecretCreator,
}


def create_new_secret(
    secret_type: SecretType,
    secret_name: Optional[str] = None,
    no_input: bool = False,
    **kwargs,
) -> int:
    kwargs.pop('func', None)

    with input_disabled(no_input):
        try:
            creator = CREATORS[secret_type]()
            secret = creator.create(name=secret_name, **kwargs)
            logger.info(f'{OK} Created secret: {secret.name}')
            sync_secret(secret)
            logger.info(f'{OK} Synced to all platforms')
        except MCLIConfigError:
            logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
            return 1
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1
        except ValidationError as e:
            logger.error(e)
            return 1

    return 0


def copy_existing_secret(
    secret_name: str,
    platform_name: str,
    namespace: str,
    **kwargs,
):
    """Copy an existing secret to the user's platforms

    Args:
        secret_name: Name of secret in a shared namespace
        platform_name: Name of the platform in which the secret is stored
        namespace: Namespace in which the shared secret lives
    """
    del kwargs

    try:

        conf = MCLIConfig.load_config()

        # Check that the platform exists
        mcli_platform: Optional[MCLIPlatform] = None
        for pl in conf.platforms:
            if pl.name == platform_name:
                mcli_platform = pl
                break

        if mcli_platform is None:
            platform_names = {pl.name for pl in conf.platforms}
            raise ValueError(
                f'Invalid platform: Platform must be one of {sorted(list(platform_names))}. Got: {platform_name}')

        # Get available secrets from new platform
        manager = SecretManager(
            MCLIPlatform(name=platform_name, kubernetes_context=mcli_platform.kubernetes_context, namespace=namespace))
        available_secrets = manager.get_secrets()
        logger.debug(f'Found {len(available_secrets)} secrets in platform {platform_name}')

        # Check if secret exists
        new_secret: Optional[MCLISecret] = None
        for platform_secret in available_secrets:
            if platform_secret.secret.name == secret_name:
                new_secret = platform_secret.secret
                break

        if new_secret is None:
            raise ValueError(
                f'Secret not found: Could not find secret {secret_name} in {namespace} namespace of platform '
                f'{platform_name}. Please double-check these values.')

        # Sync secret to user's platforms
        logger.info(f'{OK} Copying existing secret: {secret_name}')
        sync_secret(new_secret)
        logger.info(f'{OK} Synced to all platforms')
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1
    except ValueError as e:
        logger.error(f'{FAIL} {e}')
        return 1
    return 0


def sync_secret(secret: MCLISecret):
    conf = MCLIConfig.load_config()

    # Sync to all known platforms
    platform_secret = PlatformSecret(secret)
    with console.status('Creating secret in all platforms...') as status:
        for platform in conf.platforms:
            with MCLIPlatform.use(platform):
                status.update(f'Creating secret in platform: {platform.name}...')
                platform_secret.create(platform.namespace)


def _add_common_arguments(parser: argparse.ArgumentParser):
    parser.add_argument(
        '--name',
        dest='secret_name',
        metavar='NAME',
        help='What you would like to call the secret. Must be unique',
    )
    parser.add_argument('--no-input', action='store_true', help='Do not query for user input')


def _add_docker_registry_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    DOCKER_EXAMPLES = """

    Examples:

    # Add docker credentials interactively
    mcli create secret docker
    """
    docker_registry_parser = subparser.add_parser(
        'docker',
        help='Create a secret to let you pull images from a private Docker registry.',
        description='Create a secret to let you pull images from a private Docker registry.',
        epilog=DOCKER_EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _add_common_arguments(docker_registry_parser)
    docker_registry_parser.add_argument(
        '--username',
        dest='username',
        help='Your username for the Docker registry',
    )
    docker_registry_parser.add_argument(
        '--password',
        dest='password',
        help='Your password for the Docker registry. If possible, use an API key here.',
    )
    docker_registry_parser.add_argument(
        '--email',
        dest='email',
        help='The email you use for the Docker registry',
    )
    docker_registry_parser.add_argument('--server',
                                        dest='server',
                                        help='The URL for the Docker registry. '
                                        'For DockerHub, this should be https://index.docker.io/v1/.')
    docker_registry_parser.set_defaults(func=secret_handler, secret_type=SecretType.docker_registry)
    return docker_registry_parser


def _add_ssh_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add an SSH key
    mcli create secret ssh ~/.ssh/my_id_rsa

    # Give the secret a special name and special mount point
    mcli create secret ssh ~/.ssh/my_id_rsa --name my-ssh-key --mount-path /secrets/foo

    # Add an SSH secret interactively
    mcli create secret ssh
    """
    ssh_parser = subparser.add_parser(
        'ssh',
        help='Create an SSH secret for your SSH private key',
        description='Add your SSH private key to your workloads to enable SSH from within your workloads. '
        'This allows you to get data into your workloads via SSH, for example from an SFTP server.',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ssh_parser.add_argument('ssh_private_key',
                            metavar='</path/to/private-key>',
                            nargs='?',
                            help='Path the private key of an SSH key-pair')
    ssh_parser.add_argument('--mount-path',
                            metavar='</path/inside/workload>',
                            help='Location in your workload at which the SSH key should be mounted')
    _add_common_arguments(ssh_parser)
    ssh_parser.set_defaults(func=secret_handler, secret_type=SecretType.ssh, git=False)


def _add_git_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add a Git SSH key
    mcli create secret git-ssh ~/.ssh/github_id_rsa

    # Give the secret a special name and special mount point
    mcli create secret git-ssh ~/.ssh/github_id_rsa --name my-git-key --mount-path /secrets/foo

    # Add a Git SSH secret interactively
    mcli create secret git-ssh
    """
    git_parser = subparser.add_parser(
        'git-ssh',
        help='Create an SSH secret for use with Git commands',
        description='Add an SSH private key to your workloads to access private Git repos over SSH. '
        'To use this, you\'ll also need to register the associated public SSH key to your account '
        'at github.com (or your repository host of choice).',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    git_parser.add_argument('ssh_private_key',
                            metavar='</path/to/private-key>',
                            nargs='?',
                            help='Path to the private key of an SSH key-pair')
    git_parser.add_argument('--mount-path',
                            metavar='</path/inside/workload>',
                            help='Location in your workload at which the SSH key should be mounted')
    _add_common_arguments(git_parser)
    git_parser.set_defaults(func=secret_handler, secret_type=SecretType.git, git=True)


def _add_mounted_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    generic_mounted_parser = subparser.add_parser('mounted', help='Create a secret that will be mounted as a text file')
    _add_common_arguments(generic_mounted_parser)
    generic_mounted_parser.add_argument('--mount-path',
                                        help='Location in your workload at which the secret should be mounted')
    generic_mounted_parser.add_argument('--value', help='Secret data you\'d like to store at the chosen path')
    generic_mounted_parser.set_defaults(func=secret_handler, secret_type=SecretType.mounted)


def _add_env_var_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    # pylint: disable-next=invalid-name
    EXAMPLES = """

    Examples:

    # Add a secret API key as an environment variable named FOO
    mcli create secret env FOO=super-secret-api-key-1234

    # Give the secret a special name
    mcli create secret env FOO=super-secret-api-key-1234 --name my-env-var

    # Add an environment variable secret interactively
    mcli create secret env
    """
    generic_env_parser = subparser.add_parser(
        'env',
        help='Create a secret that will be exposed as an environment variable',
        description='Create a secret that will be exposed as an environment variable. This lets you easily use '
        'arbitrary confidential information within your workloads.',
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    generic_env_parser.add_argument(
        'env_pair',
        nargs='?',
        help='A KEY=VALUE pair',
    )
    _add_common_arguments(generic_env_parser)
    generic_env_parser.set_defaults(func=secret_handler, secret_type=SecretType.environment)


def _add_s3_subparser(
    subparser: argparse._SubParsersAction,
    secret_handler: Callable,
):
    s3_cred_parser = subparser.add_parser('s3', help='Create an S3 Credentials Secret')
    _add_common_arguments(s3_cred_parser)
    s3_cred_parser.add_argument('--config-file', help='Path to your S3 config file. Usually `~/.aws/config`')
    s3_cred_parser.add_argument('--credentials-file',
                                help='Path to your S3 credentials file. Usually `~/.aws/credentials`')
    s3_cred_parser.add_argument(
        '--mount-directory',
        help='Location in your workload at which your credentials and config files will be mounted')
    s3_cred_parser.set_defaults(func=secret_handler, secret_type=SecretType.s3_credentials)


def _add_shared_subparser(subparser: argparse._SubParsersAction,):
    shared_parser = subparser.add_parser('shared', help='Copy an existing secret from a shared store')
    shared_parser.add_argument('--name',
                               dest='secret_name',
                               required=True,
                               help='Name of an existing secret',
                               metavar='NAME')

    conf = MCLIConfig.load_config(safe=True)
    platform_names = sorted([pl.name for pl in conf.platforms])
    shared_parser.add_argument(
        '--platform',
        dest='platform_name',
        required=True,
        choices=platform_names,
        metavar='PLATFORM',
        help=f'Name of the platform that contains the secret. Choices: {", ".join(platform_names)}')

    shared_parser.add_argument('--namespace', required=True, help='Namespace that contains the secret')
    shared_parser.set_defaults(func=copy_existing_secret)


def configure_secret_argparser(
    parser: argparse.ArgumentParser,
    secret_handler: Callable,
) -> None:

    subparser = parser.add_subparsers(title='MCLI Secrets',
                                      description='The table below shows the types of secrets that you can create',
                                      help='DESCRIPTION',
                                      metavar='SECRET_TYPE')

    # Environment variables
    _add_env_var_subparser(subparser, secret_handler)

    # Mounted secrets
    _add_mounted_subparser(subparser, secret_handler)

    # Docker registry
    _add_docker_registry_subparser(subparser, secret_handler)

    # SSH credentials
    _add_ssh_subparser(subparser, secret_handler)

    # Git credentials
    _add_git_subparser(subparser, secret_handler)

    # S3 credentials
    _add_s3_subparser(subparser, secret_handler)

    # Shared secret
    _add_shared_subparser(subparser)
