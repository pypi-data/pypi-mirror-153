"""Creators for s3 secrets"""
from pathlib import Path
from typing import Callable, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIS3Secret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.objects.secrets.create.generic import FileSecretFiller, FileSecretValidator
from mcli.utils.utils_interactive import get_validation_callback, list_options
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_validation import validate_existing_filename


class S3SecretFiller(FileSecretFiller):
    """Interactive filler for s3 secret data
    """

    @staticmethod
    def fill_file(prompt: str, helptext: str, validate: Callable[[str], bool]) -> str:
        return list_options(prompt,
                            options=[],
                            helptext=helptext,
                            pre_helptext=None,
                            allow_custom_response=True,
                            validate=validate)

    @classmethod
    def fill_config(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file('Where is your S3 config file located?', 'Path to your config file', validate)

    @classmethod
    def fill_credentials(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_file('Where is your S3 credentials file located?', 'Path to your credentials file', validate)


class S3SecretValidator(FileSecretValidator):
    """Validation methods for secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_file_exists(path: str) -> bool:

        if not validate_existing_filename(path):
            raise SecretValidationError(
                f'{FAIL} File does not exist. File path {path} does not exist or is not a file.')
        return True


class S3SecretCreator(S3SecretFiller, S3SecretValidator):
    """Creates s3 secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               mount_directory: Optional[str] = None,
               credentials_file: Optional[str] = None,
               config_file: Optional[str] = None) -> MCLIS3Secret:

        # Validate mount directory and files
        if mount_directory:
            self.validate_mount(mount_directory)

        if credentials_file:
            self.validate_file_exists(credentials_file)

        if config_file:
            self.validate_file_exists(config_file)

        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.s3_credentials, name=name)
        assert isinstance(secret, MCLIS3Secret)

        if not config_file:
            config_file = self.fill_config(get_validation_callback(self.validate_file_exists))

        if not credentials_file:
            credentials_file = self.fill_credentials(get_validation_callback(self.validate_file_exists))

        if not mount_directory:
            mount_directory = self.get_valid_mount_path(secret.name)
        secret.mount_directory = mount_directory

        with open(Path(config_file).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.config = fh.read()

        with open(Path(credentials_file).expanduser().absolute(), 'r', encoding='utf8') as fh:
            secret.credentials = fh.read()

        return secret
