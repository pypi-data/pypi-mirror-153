""" mcli clean Entrypoint """
import os
import shutil

from mcli import config
from mcli.api.utils.nuke_db import nuke_db


def clean_mcli(remove_db: bool = False, **kwargs) -> int:
    del kwargs
    try:
        shutil.rmtree(config.MCLI_PROJECTS_DIR)
    except Exception as _:  # pylint: disable=broad-except
        pass
    try:
        os.remove(config.CURRENT_PROJECT_SYMLINK_PATH)
    except Exception as _:  # pylint: disable=broad-except
        pass

    if remove_db:
        print('Nuking the DB')
        success = nuke_db()
        if success:
            print('Wiping DB Successful')

    try:
        os.remove(config.MCLI_CONFIG_PATH)
    except Exception as _:  # pylint: disable=broad-except
        pass

    print('All clean!')
    return 0
