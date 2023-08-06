"""Utils for modifying MCTL Configs"""
import random
import string
from typing import Optional

import coolname
from jinja2 import Environment, StrictUndefined


def uuid_generator(length: int = 10) -> str:
    allowed_characters = string.ascii_lowercase + string.digits
    items = random.choices(population=allowed_characters, k=length)
    return ''.join(items)


def get_unique_name(stem: Optional[str] = None):
    if stem is None:
        stem = coolname.generate_slug(2)
    return f'{stem}-{uuid_generator(6)}'


def format_jinja(input_text: str, config: dict, **kwargs):
    if input_text is None:
        return input_text

    env = Environment(undefined=StrictUndefined, **kwargs)
    template = env.from_string(input_text)
    return template.render(**config)
