"""Helper Utils for Yaml Files"""
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


class StringDumpYAML(YAML):
    """ Yaml dump to string """

    def dump(  #type: ignore
        self,
        data: Any,
        stream: Union[Path, 'StreamType'] = None,  # type: ignore
        transform: Any = None,
    ) -> Any:

        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, transform=transform)
        if inefficient:
            return stream.getvalue()  # type: ignore
        return ''


def load_yaml(path: Union[str, Path]) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf8') as fh:
        config = yaml.safe_load(fh)
        if config is None:
            config = {}
    assert isinstance(config, dict), \
        f'Error expected config to be a dict but got {config}'
    return config
