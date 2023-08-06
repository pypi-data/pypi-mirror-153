"""Helpers for formatting run names within a sweep"""
from __future__ import annotations

import uuid
from dataclasses import asdict
from typing import Any, Dict, List, NamedTuple

from mcli.sweeps.local_sweep_config import LocalRunConfig
from mcli.utils.utils_config import format_jinja
from mcli.utils.utils_string_validation import ensure_rfc_compatibility
from mcli.utils.utils_types import nested_to_dot


class RunTemplate(NamedTuple):
    """Run template with help string - for use in interactive queries
    """
    template: str
    help: str

    @classmethod
    def from_string(cls, template: str) -> RunTemplate:
        return cls(template, '')


RUN_TEMPLATE_SWEEP_ONLY = RunTemplate("""{{ sweep }}""", 'Sweep only')
RUN_TEMPLATE_ALGO_STR = RunTemplate("""{{ sweep }}-{{ algorithm_str }}""", 'Sweep + algorithms')
SIMPLE_RUN_TEMPLATES = [RUN_TEMPLATE_SWEEP_ONLY, RUN_TEMPLATE_ALGO_STR]

RUN_TEMPLATE_SWEEP_VALUES = RunTemplate(
    """{{ sweep }}{%- for value in search.values() -%}-{{ value|e|replace(".", "p") }}{%- endfor -%}""",
    'Sweep + search values',
)
RUN_TEMPLATE_SWEEP_ITEMS = RunTemplate(
    """{{ sweep }}{% for key, value in search.items() -%}
            {% set sepkey = key.split(".") %}-{{ sepkey|last|e }}-{{ value|e|replace(".", "p") }}
        {%- endfor %}""",
    'Sweep + search keys and values',
)
RUN_TEMPLATE_SWEEP_SHORT_ITEMS = RunTemplate(
    """{{ sweep }}-{% for key, value in search.items() -%}
            {% set sepkey = key.split(".") %}{% set keylist = sepkey[-1].split("_") %}{% if keylist|length is gt(1) -%}
            {{ "-" }}
                {% for ss in keylist -%}
                    {{ ss|e|first }}
                {%- endfor %}
            {%- else -%}
                {{ keylist|first }}
            {%- endif %}{{ "-" }}{{ value|e|replace(".", "p") }}
        {%- endfor %}""",
    'Sweep + short search keys and values',
)

ALL_RUN_TEMPLATES = SIMPLE_RUN_TEMPLATES + [
    RUN_TEMPLATE_SWEEP_VALUES, RUN_TEMPLATE_SWEEP_ITEMS, RUN_TEMPLATE_SWEEP_SHORT_ITEMS
]


def format_run_name(template: RunTemplate, formatters: Dict[str, Any]) -> str:
    """Format a run name according to the given template and data

    Args:
        template: Template string to be formatted
        formatters: Dictionary of data used to format the template

    Returns:
        A formatted string
    """
    name = format_jinja(template.template, formatters, trim_blocks=True, lstrip_blocks=True)
    name = ensure_rfc_compatibility(name, 58, r'\-', end_alnum_verification=False)
    name = f'{name}-{str(uuid.uuid4())[:4]}'
    return name


def format_run_name_helper(template: RunTemplate, formatters: Dict[str, Any]) -> str:
    """Format a run name with a helper string

    Returns the formatted string, along with the RunTemplate help text right-justified.

    Args:
        template: Template string to be formatted, with associated help text
        formatters: Dictionary of data used to format the template

    Returns:
        A formatted string with help text
    """
    name = format_run_name(template, formatters)
    return f'{name.ljust(40)}\t({template.help})'


def get_run_format_options(config: LocalRunConfig, search_parameters: List[str]) -> Dict[str, Any]:
    """Get a dictionary of data for formatting

    Creates a dictionary for formatting run names based on the LocalRunConfig. Every field in the LocalRunConfig can
    be used. The `parameters` field is changed to dot-syntax so that it can be easily used. Also adds an
    'algorithm_str' field that is a '-'-separated list of algorithms or 'none' if no algorithms are used. Lastly,
    adds the search parameters for this particular run under the 'search' key.

    Args:
        config: A single, complete LocalRunConfig
        search_parameters: The search parameters that correspond to this run

    Returns:
        Dictionary of data used to format a run template
    """
    format_options = asdict(config)
    format_options['parameters'] = nested_to_dot(format_options['parameters'])
    format_options['algorithm_str'] = '-'.join(
        format_options['algorithm']).lower() if format_options['algorithm'] else 'none'
    format_options['search'] = {key: format_options['parameters'][key] for key in search_parameters}
    return format_options
