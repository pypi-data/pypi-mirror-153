"""Base creator for secrets"""
import logging
import uuid
from typing import Callable, List, Optional, Set

from mcli.config import MCLIConfig
from mcli.models import MCLIPlatform, MCLISecret, SecretType
from mcli.objects.secrets import SECRET_CLASS_MAP
from mcli.objects.secrets.platform_secret import SecretManager
from mcli.utils.utils_interactive import ValidationError, get_validation_callback, list_options
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_validation import validate_secret_name

logger = logging.getLogger(__name__)


class SecretValidationError(ValidationError):
    """Secret could not be configured with the provided values
    """


class SecretFiller():
    """Interactive filler for secret data
    """

    @staticmethod
    def fill_name(validate: Callable[[str], bool]) -> str:
        return list_options(
            input_text='What would you like to name this secret?',
            options=[],
            helptext='Must be unique',
            pre_helptext=None,
            allow_custom_response=True,
            validate=validate,
        )


class SecretValidator():
    """Validation methods for secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    def __init__(self):

        conf = MCLIConfig.load_config()
        self.validate_one_platform_exists(conf.platforms)
        self.existing_secrets = self.get_existing_secrets(conf.platforms[0])
        self.existing_secret_names = {secret.name for secret in self.existing_secrets}

    @staticmethod
    def get_existing_secrets(platform: MCLIPlatform) -> List[MCLISecret]:
        secret_manager = SecretManager(platform)
        return [ps.secret for ps in secret_manager.get_secrets()]

    @staticmethod
    def validate_one_platform_exists(platforms: List[MCLIPlatform]) -> bool:

        if not platforms:
            raise SecretValidationError(
                f'{FAIL} No platforms found. You must have at least one platform setup before you add secrets. '
                'Please try running `mcli create platform` first to generate one.')
        return True

    @staticmethod
    def validate_secret_name_available(name: str, existing_names: Set[str]) -> bool:

        if name in existing_names:
            raise SecretValidationError(f'{FAIL} Existing secret. Secret named {name} already exists. Please choose '
                                        f'something not in {sorted(list(existing_names))}.')
        return True

    @staticmethod
    def validate_secret_name_rfc(name: str) -> bool:

        result = validate_secret_name(name)
        if not result:
            raise SecretValidationError(f'{FAIL} {result.message}')
        return True

    def validate_secret_name_full(self, name: str) -> bool:
        return self.validate_secret_name_rfc(name) and self.validate_secret_name_available(
            name, self.existing_secret_names)


class SecretCreator(SecretValidator, SecretFiller):
    """Creates base secrets for the CLI
    """

    @staticmethod
    def create_base_secret(name: str, secret_type: SecretType) -> MCLISecret:
        secret_class = SECRET_CLASS_MAP.get(secret_type)
        if not secret_class:
            raise SecretValidationError(f'{FAIL} The secret type: {secret_type} does not exist.')

        return secret_class(name, secret_type)

    def create(self,
               secret_type: SecretType,
               name: Optional[str] = None,
               make_name_unique: bool = False,
               **kwargs) -> MCLISecret:

        del kwargs

        if name:
            try:
                self.validate_secret_name_available(name, self.existing_secret_names)
            except SecretValidationError:
                if make_name_unique:
                    name = f'{name[:58]}-{str(uuid.uuid4())[:4]}'
                else:
                    raise
            self.validate_secret_name_rfc(name)

        if not name:
            name = self.fill_name(validate=get_validation_callback(self.validate_secret_name_full))

        return self.create_base_secret(name, secret_type)
