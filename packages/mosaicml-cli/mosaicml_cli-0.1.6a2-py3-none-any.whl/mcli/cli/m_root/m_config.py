""" MCLI Entrypoint mcli config """

from mcli.cli.m_get.envvars import get_environment_variables
from mcli.cli.m_get.platforms import get_platforms
from mcli.cli.m_get.projects import get_projects
from mcli.cli.m_get.secrets import get_secrets
from mcli.config import MCLIConfig


def m_get_config(**kwargs) -> int:
    """Gets the current project config and prints it out

    Args:
        **kwargs:
    """
    del kwargs

    conf = MCLIConfig.load_config()

    spacer = '-' * 20

    def print_padded(text: str):
        print(f'{spacer} {text: ^20} {spacer}')

    print_padded('MCLI Config')
    print(conf)
    print_padded('END')

    print_padded('MCLI Platforms')
    get_platforms()
    print_padded('END')

    print_padded('MCLI Secrets')
    get_secrets()
    print_padded('END')

    print_padded('MCLI EnvVars')
    get_environment_variables()
    print_padded('END')

    if conf.internal:
        try:
            print_padded('MCLI Projects')
            get_projects()
        except:  # pylint: disable=bare-except
            print('MCLI Projects still broken')
        finally:
            print_padded('END')

    return 0
