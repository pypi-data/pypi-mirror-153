"""Creators for docker secrets"""
from typing import Callable, Optional

from mcli.models import SecretType
from mcli.objects.secrets import MCLIDockerRegistrySecret
from mcli.objects.secrets.create.base import SecretCreator, SecretValidationError
from mcli.utils.utils_interactive import get_validation_callback, list_options
from mcli.utils.utils_logging import FAIL
from mcli.utils.utils_string_validation import validate_email_address, validate_url


class DockerSecretFiller():
    """Interactive filler for docker secret data
    """

    @staticmethod
    def fill_str(prompt: str, helptext: str, validate: Callable[[str], bool], is_password: bool = False, **kwargs):
        del is_password
        return list_options(input_text=prompt,
                            options=[],
                            helptext=helptext,
                            validate=validate,
                            allow_custom_response=True,
                            pre_helptext=None,
                            **kwargs)

    @classmethod
    def fill_username(cls) -> str:
        return cls.fill_str('What is your username?', 'Username for this registry', lambda s: True)

    @classmethod
    def fill_password(cls) -> str:
        return cls.fill_str('What is your password/API token?', 'Token associated with this registry', lambda s: True)

    @classmethod
    def fill_email(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_str('What is your email address?', 'Email associated with this registry', validate)

    @classmethod
    def fill_server(cls, validate: Callable[[str], bool]) -> str:
        return cls.fill_str('What is the URL for this registry?',
                            '',
                            validate,
                            default_response='https://index.docker.io/v1/')


class DockerSecretValidator():
    """Validation methods for docker secret data

    Raises:
        SecretValidationError: Raised for any validation error for secret data
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        is_valid_email = validate_email_address(email)
        if not is_valid_email:
            raise SecretValidationError(f'{FAIL} {email} does not appear to be a valid email address.')
        return True

    @staticmethod
    def validate_server(url: str) -> bool:
        is_valid_url = validate_url(url)
        if not is_valid_url:
            raise SecretValidationError(f'{FAIL} {url} does not appear to be a valid URL.')
        return True


class DockerSecretCreator(DockerSecretFiller, DockerSecretValidator):
    """Creates docker secrets for the CLI
    """

    def create(self,
               name: Optional[str] = None,
               docker_username: Optional[str] = None,
               docker_password: Optional[str] = None,
               docker_email: Optional[str] = None,
               docker_server: Optional[str] = None,
               **kwargs) -> MCLIDockerRegistrySecret:
        del kwargs

        if docker_server:
            self.validate_server(docker_server)

        if docker_email:
            self.validate_email(docker_email)

        # Get base secret
        base_creator = SecretCreator()
        secret = base_creator.create(SecretType.docker_registry, name)
        assert isinstance(secret, MCLIDockerRegistrySecret)

        if not secret.docker_server:
            secret.docker_server = docker_server or self.fill_server(get_validation_callback(self.validate_server))

        if not secret.docker_username:
            secret.docker_username = docker_username or self.fill_username()

        if not secret.docker_password:
            secret.docker_password = docker_password or self.fill_password()

        if not secret.docker_email:
            secret.docker_email = docker_email or self.fill_email(get_validation_callback(self.validate_email))

        return secret
