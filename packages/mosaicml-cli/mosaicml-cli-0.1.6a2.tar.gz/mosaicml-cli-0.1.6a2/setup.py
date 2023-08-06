""" Copyright 2021 MosaicML. All Rights Reserved. """

import os

import setuptools
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# pylint: disable-next=exec-used,consider-using-with
exec(open('mcli/version.py', 'r', encoding='utf-8').read())

install_requires = [
    'argcomplete>=2.0.0',
    'argparse>=1.4.0',
    'coolname>=1.1.0',
    'fire>=0.4.0',
    'kubernetes>=21.7.0',
    'parse>=1.19.0',
    'prompt_toolkit>=3.0.24',
    'pyyaml>=5.4.1',
    'rich>=10.16.2',
    'ruamel.yaml>=0.17.21',
    'toml>=0.10.2',
    'typing_extensions>=4.0.1',
    'wandb>=0.12.2',
    'yaspin>=2.1.0',
    'jinja2',
]

extra_deps = {}

extra_deps['dev'] = [
    'isort>=5.9.3',
    'pre-commit>=2.17.0',
    'pylint>=2.12.2',
    'pytest>=6.2.5',
    'pytest-mock>=3.7.0',
    'radon>=5.1.0',
    'yapf>=0.32.0',
]
extra_deps['internal'] = [
    'mosaicml-mutil',
]

extra_deps['sphinx'] = [
    'furo>=2022.3.4',
    'sphinx>=4.4.0',
    'sphinx-argparse>=0.3.1',
    'sphinx-copybutton>=0.5.0',
    'sphinx-markdown-tables>=0.0.15',
    'sphinx-panels>=0.6.0',
    'sphinx-rtd-theme>=1.0.0',
    'sphinxcontrib-applehelp>=1.0.2',
    'sphinxcontrib-devhelp>=1.0.2',
    'sphinxcontrib-htmlhelp>=2.0.0',
    'sphinxcontrib-images>=0.9.4',
    'sphinxcontrib-jsmath>=1.0.1',
    'sphinxcontrib-katex>=0.8.6',
    'sphinxcontrib-qthelp>=1.0.3',
    'sphinxcontrib-serializinghtml>=1.1.5',
    'sphinxemoji>=0.2.0',
    'sphinxext-opengraph>=0.6.1',
    'myst-parser>=0.16.1',
]


def package_files(directory: str):
    # from https://stackoverflow.com/a/36693250
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name='mosaicml-cli',
    version=__version__,  # type: ignore pylint: disable=undefined-variable
    author='MosaicML',
    author_email='team@mosaicml.com',
    description='Running stuff',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mosaicml/mosaicml-cli',
    include_package_data=True,
    package_data={
        '': package_files('mcli-yamls'),
    },
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'mosaic = mcli.cli.cli:main',
            'mos = mcli.cli.cli:main',
            'mcli = mcli.cli.cli:main',
            'm = mcli.cli.cli:main',
            'script_mcli_add_stable_s3 = mcli_scripts.add_stable_s3:main',
        ],
    },
    extras_require=extra_deps,
    python_requires='>=3.8',
    ext_package='mcli',
)
