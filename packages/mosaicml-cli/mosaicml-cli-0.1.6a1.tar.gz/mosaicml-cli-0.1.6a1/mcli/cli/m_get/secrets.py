"""CLI getter for secrets"""
import logging
from dataclasses import dataclass
from typing import Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MESSAGE, MCLIConfig, MCLIConfigError
from mcli.models import MCLISecret, SecretType
from mcli.objects.secrets.platform_secret import SecretManager

logger = logging.getLogger(__name__)


@dataclass
class SecretDisplayItem(MCLIDisplayItem):
    name: str
    type: SecretType


class MCLISecretDisplay(MCLIGetDisplay):
    """`mcli get secrets` display class
    """

    def __init__(self, secrets: List[MCLISecret]):
        self.secrets = secrets

    def __iter__(self) -> Generator[SecretDisplayItem, None, None]:
        for secret in self.secrets:
            yield SecretDisplayItem(name=secret.name, type=secret.secret_type)


def get_secrets(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    """Get currently configured secrets from the reference platform

    Args:
        output: Output display type. Defaults to OutputDisplay.TABLE.

    Returns:
        0 if call succeeded, else 1
    """
    del kwargs

    try:
        conf: MCLIConfig = MCLIConfig.load_config()
    except MCLIConfigError:
        logger.error(MESSAGE.MCLI_NOT_INITIALIZED)
        return 1

    if not conf.platforms:
        logger.warning('No platforms found. Secrets require at least one platform to be configured.')
        return 0

    ref_platform = conf.platforms[0]
    manager = SecretManager(ref_platform)
    mcli_secrets = [ps.secret for ps in manager.get_secrets()]
    display = MCLISecretDisplay(mcli_secrets)
    display.print(output)
    return 0
