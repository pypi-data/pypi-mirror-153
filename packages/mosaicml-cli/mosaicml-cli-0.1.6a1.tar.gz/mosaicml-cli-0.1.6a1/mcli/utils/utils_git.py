"""Utils for git subcommands"""
import subprocess
from typing import List, Optional


def get_git_root():
    git_command = 'git rev-parse --show-toplevel'
    git_root = subprocess.getoutput(git_command)
    return git_root


def get_git_repo_name() -> Optional[str]:
    git_remote = get_git_remote()
    if git_remote is None:
        return None
    git_remote = git_remote.replace('.git', '')
    git_remote = git_remote.replace('git@github.com:', '')
    git_remote = git_remote.replace('https://github.com/', '')
    git_remote = git_remote.replace('http://github.com/', '')
    return git_remote


def get_git_remote() -> Optional[str]:
    git_command = 'git remote get-url origin'
    git_remote = subprocess.getoutput(git_command)
    if git_remote == 'fatal: not a git repository (or any of the parent directories): .git':
        return None
    return git_remote


def get_git_tags() -> List[str]:
    git_command = 'git tag -l'
    git_tags = subprocess.getoutput(git_command)
    if 'fatal' in git_tags or git_tags == '':
        return []
    return sorted(git_tags.split('\n'), reverse=True)


def get_git_branch_current() -> Optional[str]:
    git_command = 'git branch --show-current'
    git_branch = subprocess.getoutput(git_command)
    if 'fatal' in git_branch:
        return None
    if git_branch == '':
        if get_git_tag_current() is not None:
            return get_git_tag_current()
        return None
    return git_branch


def get_git_tag_current() -> Optional[str]:
    git_command = 'git describe --exact-match --tags'
    git_tag = subprocess.getoutput(git_command)
    if 'fatal' in git_tag or git_tag == '':
        return None
    return git_tag
