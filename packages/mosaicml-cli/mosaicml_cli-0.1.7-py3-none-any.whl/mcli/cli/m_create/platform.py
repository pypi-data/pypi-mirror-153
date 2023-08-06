"""CLI creator for platforms"""
import argparse
import logging
import textwrap
from typing import Callable, List, Optional, Set

from kubernetes.config.config_exception import ConfigException

from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLIPlatform
from mcli.objects.secrets.platform_secret import SecretManager
from mcli.utils.utils_interactive import (InputDisabledError, ValidationError, get_validation_callback, input_disabled,
                                          list_options)
from mcli.utils.utils_kube import KubeContext, get_kube_contexts
from mcli.utils.utils_logging import FAIL, OK, console
from mcli.utils.utils_string_validation import validate_rfc1123_name

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete platform. Please provide a name, context and namespace if running with '
                          '`--no-input`. Check `mcli create platform --help` for more information.')

PLATFORM_EXAMPLES = """

Examples:

# Choose a platform from a list of options
mcli create platform

# Add the rXzX platform
mcli create platform rXzX

# Add a platform with a custom name and namespace
mcli create platform rXzX --name my-platform --namespace my-user-namespace
"""


class PlatformValidationError(ValidationError):
    """Platform could not be configured with the provided values
    """


class PlatformFillError(ValidationError):
    """Platform could not have its details filled in
    """


class PlatformFiller():
    """Interactive filler for platform data
    """

    @staticmethod
    def fill_context(available_contexts: List[KubeContext], validate: Callable[[KubeContext], bool]) -> KubeContext:
        print_kube_context = lambda x: x.name
        default = available_contexts[0]
        new_context = list_options(
            input_text='Which platform would you like to set up?',
            options=available_contexts,
            default_response=default,
            pre_helptext='Select the platform to set up:',
            helptext=f'default: {print_kube_context(default)}',
            print_option=print_kube_context,
            validate=validate,
        )
        return new_context

    @staticmethod
    def fill_namespace(default: str, validate: Callable[[str], bool]) -> str:
        namespace = list_options(
            input_text='Which namespace will you be using?',
            options=[default],
            default_response=default,
            pre_helptext=' ',
            helptext=f'default: {default}',
            allow_custom_response=True,
            validate=validate,
        )
        return namespace


class PlatformValidator():
    """Validation methods for platform data

    Raises:
        PlatformValidationError: Raised for any validation error for platform data
    """

    @staticmethod
    def validate_contexts_available(contexts: List[KubeContext]) -> bool:
        if not contexts:
            raise PlatformValidationError(f'{FAIL} All platforms from your kubeconfig file have already been added.')
        return True

    @classmethod
    def validate_context_exists(cls, context: KubeContext, available_contexts: List[KubeContext]) -> bool:
        return cls.validate_context_name_exists(context.name, [kc.name for kc in available_contexts])

    @staticmethod
    def validate_context_name_exists(context_name: str, available_context_names: List[str]) -> bool:
        if context_name not in available_context_names:
            raise PlatformValidationError(f'{FAIL} No context named {context_name}. Available contexts are '
                                          f'{sorted(available_context_names)}')
        return True

    @staticmethod
    def validate_context_supported(context_name: str) -> bool:
        # pylint: disable-next=import-outside-toplevel
        from mcli.serverside.platforms.platform import GenericK8sPlatform
        if context_name not in GenericK8sPlatform.get_k8s_context_map():
            raise PlatformValidationError(f'{FAIL} Context named {context_name} currently unsupported.')
        return True

    @staticmethod
    def validate_platform_name_available(name: str, platform_names: Set[str]) -> bool:
        if name in platform_names:
            raise PlatformValidationError(f'{FAIL} Existing platform. Platform named {name} already exists. Please '
                                          f'choose something not in {sorted(list(platform_names))}')
        return True

    @staticmethod
    def validate_namespace_rfc1123(namespace: str) -> bool:
        is_valid = validate_rfc1123_name(namespace)
        if not is_valid:
            raise PlatformValidationError(f'{FAIL} Invalid Kubernetes namespace. {is_valid.message}')
        return True


class PlatformCreator(PlatformValidator, PlatformFiller):
    """Creates platforms for the CLI
    """

    @staticmethod
    def get_all_platforms() -> List[MCLIPlatform]:
        conf: MCLIConfig = MCLIConfig.load_config()
        return conf.platforms

    @staticmethod
    def get_available_contexts(platforms: List[MCLIPlatform]):
        platform_contexts = [x.kubernetes_context for x in platforms]
        kube_contexts = get_kube_contexts()
        return [x for x in kube_contexts if x.name not in platform_contexts]

    @staticmethod
    def shortened_cluster_name_default(name: str) -> str:
        if len(name.split('-')) > 1:
            return name.split('-')[0]
        return name

    def create_all(self,) -> List[MCLIPlatform]:
        created_platforms = []
        all_platforms = self.get_all_platforms()
        unregistered_contexts = self.get_available_contexts(all_platforms)
        self.validate_contexts_available(unregistered_contexts)
        for unregistered_context in unregistered_contexts:
            platform = self.create(
                name=None,
                kubernetes_context=unregistered_context.name,
                namespace=None,
            )
            created_platforms.append(platform)
        return created_platforms

    def create(
        self,
        name: Optional[str],
        kubernetes_context: Optional[str],
        namespace: Optional[str],
    ) -> MCLIPlatform:
        all_platforms = self.get_all_platforms()
        platform_names = {x.name for x in all_platforms}

        unregistered_contexts = self.get_available_contexts(all_platforms)
        self.validate_contexts_available(unregistered_contexts)
        available_context_map = {kc.name: kc for kc in unregistered_contexts}

        # Validate provided arguments
        new_context = None
        if kubernetes_context:
            self.validate_context_name_exists(kubernetes_context, list(available_context_map.keys()))
            new_context = available_context_map[kubernetes_context]

        if name:
            self.validate_platform_name_available(name, platform_names)

        if namespace:
            self.validate_namespace_rfc1123(namespace)

        # Fill remaining details
        if not new_context:
            new_context = self.fill_context(unregistered_contexts,
                                            validate=get_validation_callback(self.validate_context_exists,
                                                                             unregistered_contexts))
        name = name or self.shortened_cluster_name_default(new_context.name)

        if not namespace:
            namespace = new_context.namespace or self.fill_namespace(
                default='default',
                validate=get_validation_callback(self.validate_namespace_rfc1123),
            )

        self.validate_context_supported(new_context.name)
        return MCLIPlatform(name=name, kubernetes_context=new_context.name, namespace=namespace)


def create_new_platform(
    name: Optional[str] = None,
    kubernetes_context: Optional[str] = None,
    namespace: Optional[str] = None,
    all_platforms: bool = False,
    no_input: bool = False,
    **kwargs,
) -> int:
    """Create a new platform

    All required variables can be provided directly. If they are not provided, they will
    be requested interactively from the user unless `no_input` is `True`.

    Args:
        name: Name of the platform. Defaults to None.
        kubernetes_context: Name of the associated kubernetes context. Defaults to None.
        namespace: Namespace of the associated kubernetes context. Defaults to None.
        no_input: If True, all required data must be provided since no interactive user
            input is allowed. Defaults to False.

    Returns:
        0 if creation succeeded, else 1
    """
    del kwargs

    creator = PlatformCreator()
    new_platforms_created = ''
    with input_disabled(no_input):
        try:
            if all_platforms:
                if name or kubernetes_context or namespace:
                    raise ValueError('When creating platforms with --all, not other arguments are allowed')
                all_created_platforms = creator.create_all()
                for created_platform in all_created_platforms:
                    _setup_k8s_platform(created_platform)
                    _sync_platform(created_platform)
                new_platforms_created = ', '.join([x.name for x in all_created_platforms])
            else:
                new_platform = creator.create(name=name, kubernetes_context=kubernetes_context, namespace=namespace)
                _setup_k8s_platform(new_platform)
                _sync_platform(new_platform)
                new_platforms_created = new_platform.name
        except MCLIConfigError:
            logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
            return 1
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1
        except PlatformValidationError as e:
            logger.error(e)
            return 1
        except ConfigException:
            logger.error(f'{FAIL} Could not find a valid kubeconfig file. If you think this is wrong, double-check '
                         'your `$KUBECONFIG` environment variable.')
            return 1

    logger.info(f'{OK} Created platform: {new_platforms_created}')
    return 0


def configure_platform_argparser(parser: argparse.ArgumentParser):
    """Add platform creation arguments to the argparser
    """

    parser.add_argument(
        'kubernetes_context',
        nargs='?',
        metavar='CONTEXT',
        help='The Kubernetes context the platform should use. If omitted, you will be given a list of options',
    )
    parser.add_argument('--name', help='Optional name to give the platform. Defaults to CONTEXT.')
    parser.add_argument('--namespace',
                        help=textwrap.dedent("""
        Namespace that should be used within the given Kubernetes context. Defaults to the namespace associated
        with the specified context, if one exists."""))

    parser.add_argument('--all',
                        default=False,
                        action='store_true',
                        dest='all_platforms',
                        help='Create all available platforms.  Defaults to false')


def _setup_k8s_platform(platform: MCLIPlatform):
    """Run K8s platform setup
    """
    # pylint: disable-next=import-outside-toplevel
    from mcli.serverside.platforms.platform import GenericK8sPlatform, PlatformSetupError
    k8s_platform = GenericK8sPlatform.from_mcli_platform(platform)
    try:
        k8s_platform.setup()
    except PlatformSetupError as e:
        logger.warning(f'{FAIL} Platform setup failed with error: {e}')


def _sync_platform(platform: MCLIPlatform):
    config = MCLIConfig.load_config()
    config.platforms.append(platform)
    secret_manager = SecretManager(config.platforms[0])

    # Sync all secrets
    with console.status(f'Syncing secrets to platform {platform.name}'):
        for platform_secret in secret_manager.get_secrets():
            with MCLIPlatform.use(platform):
                platform_secret.create(platform.namespace)

    config.save_config()
