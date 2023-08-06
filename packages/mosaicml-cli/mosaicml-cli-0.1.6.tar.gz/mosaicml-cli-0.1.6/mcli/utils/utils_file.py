"""A collection of filesystem utils"""
import os
from pathlib import Path
from typing import List


def delete_file_if_exists(path: Path) -> bool:
    if path.exists() or path.is_symlink():
        path.unlink()
        return True
    return False


def create_symlink(from_path: Path, to_path: Path) -> None:
    os.symlink(to_path, from_path)


def list_directories(path: Path) -> List[Path]:
    return [x for x in path.iterdir() if x.is_dir() and x.name != '__pycache__']


def get_home_directory() -> Path:
    return Path.home()


def is_yaml(path: Path) -> bool:
    return path.name.endswith('yaml') or path.name.endswith('yml')


def list_yamls(path: Path) -> List[Path]:
    return [x for x in path.iterdir() if x.is_file() and is_yaml(x)]
