""" Conftest for Fixtures """
# Copyright 2021 MosaicML. All Rights Reserved.

from typing import List

import pytest

# Add the path of any pytest fixture files you want to make global
pytest_plugins = ['tests.fixtures', 'tests.cli.fixtures', 'tests.api.fixtures']


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption('--include-api',
                     action='store_true',
                     help="""\
        Use this flag to include tests that will call the MosaicML API. Make
        sure that you have a valid API key either in the mcli_config or
        set as an environment variable before running these tests.""")


def pytest_collection_modifyitems(config: pytest.Config, items: List[pytest.Item]) -> None:
    include_api = config.getoption('include_api')

    # Deselect api tests
    if not include_api:
        remaining = []
        deselected = []
        for item in items:
            if item.get_closest_marker('apitest') is not None:
                # ignore tests that involve querying the graphql api
                deselected.append(item)
            else:
                remaining.append(item)

        if deselected:
            config.hook.pytest_deselected(items=deselected)
            items[:] = remaining
