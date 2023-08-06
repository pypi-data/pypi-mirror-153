""" mcli clean Entrypoint """
import os
import shutil

from mcli import config
from mcli.api.utils.nuke_db import nuke_db
from mcli.utils.utils_interactive import query_yes_no


def clean_mcli(remove_db: bool = False, **kwargs) -> int:
    del kwargs
    if not os.path.exists(config.MCLI_CONFIG_DIR):
        print("Already clean!")
        return 1

    if not query_yes_no(
            question="Are you sure you want to clean up your MCLI Configs?\n"
            f" This is a destructive action!\nA backup will be saved at {config.MCLI_BACKUP_CONFIG_DIR}:",
            default=False,
    ):
        print("Exiting...")
        return 1

    if os.path.exists(config.MCLI_BACKUP_CONFIG_DIR):
        if not query_yes_no(question="A current backup exists, overwrite it?:"):
            print("Exiting...")
            return 1
        else:
            shutil.rmtree(config.MCLI_BACKUP_CONFIG_DIR)
    shutil.move(str(config.MCLI_CONFIG_DIR), str(config.MCLI_BACKUP_CONFIG_DIR))

    if remove_db:
        print('Nuking the DB')
        success = nuke_db()
        if success:
            print('Wiping DB Successful')

    print('All clean!')
    return 0
