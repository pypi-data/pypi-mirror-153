import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Sequence, Set
from uuid import UUID

import black
import isort
from pydantic import BaseModel
from pydantic.fields import ModelField


def pydantic_model_to_python_config_file(
    model: BaseModel,
    imports: Sequence[str],
    exclude_fields: Sequence[str] = tuple(),
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    unformatted = _pydantic_model_to_python_config_file(model, imports, exclude_fields)
    # Format the python config file with black.
    formatted = _format_python_config_file(unformatted)
    return formatted


def _format_python_config_file(unformatted: str) -> str:
    """
    Format a python config file.

    :param unformatted: The python config file.
    :return: The formatted python config file.
    """
    black_formatted = black.format_str(unformatted, mode=black.FileMode(line_length=80))
    # Now format with isort
    isort_formatted = isort.code(black_formatted)
    return isort_formatted


def _pydantic_model_to_python_config_file(
    model: BaseModel,
    imports: Sequence[str],
    exclude_fields: Sequence[str] = tuple(),
) -> str:
    """
    Generate a python config file from a pydantic model.

    :param model: The pydantic model.
    :return: The python config file.
    """
    detected_stdlib_imports: Set[str] = set()
    # _build_attribute_value() will add imports to detected_stdlib_imports.
    attributes_str = _build_attributes(model, detected_stdlib_imports, exclude_fields)
    imports_str = "\n".join([*imports, *detected_stdlib_imports])
    name = model.__class__.__name__
    return f"""
{imports_str}

config = {name}({attributes_str})
""".strip()


def _build_attributes(
    model: BaseModel, stdlib_imports: Set[str], exclude_fields: Sequence[str] = tuple()
) -> str:
    """
    Build the attribute definition of a pydantic model.

    :param model: The pydantic model.
    :return: The attributes of the model.
    """
    attributes = ""
    field: ModelField
    for field_name, field in model.__fields__.items():
        if field_name in exclude_fields:
            continue
        value = getattr(model, field_name)
        attributes += (
            f"    {field_name} = {_build_attribute_value(value, stdlib_imports)},\n"
        )
    return attributes


def _build_attribute_value(value: Any, stdlib_imports: Set[str]) -> str:
    """
    Build the attribute value of a pydantic model.

    :param value: The value of the attribute.
    :return: The value of the attribute.
    """
    if isinstance(value, Enum):
        return f"{value.__class__.__name__}.{value.name}"
    elif isinstance(value, Path):
        stdlib_imports.add("from pathlib import Path")
        return f'Path("{value}")'
    elif isinstance(value, UUID):
        stdlib_imports.add("from uuid import UUID")
        return f'UUID("{value}")'
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, BaseModel):
        return repr(value)
    elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
        stdlib_imports.add("import datetime")
        return repr(value)
    # elif isinstance(value, datetime.datetime):
    #     stdlib_imports.add("from datetime import datetime")
    #     return f"datetime({value.hour}, {value.minute}, {value.second}, {value.microsecond}, tzinfo={value.tzinfo})"
    # elif isinstance(value, datetime.date):
    #     stdlib_imports.add("from datetime import date")
    #     return f"date({value.year}, {value.month}, {value.day})"
    elif isinstance(value, list):
        return (
            f"[{', '.join(_build_attribute_value(v, stdlib_imports) for v in value)}]"
        )
    elif isinstance(value, tuple):
        return (
            f"({', '.join(_build_attribute_value(v, stdlib_imports) for v in value)})"
        )
    elif isinstance(value, dict):
        return f"{{{', '.join(f'{_build_attribute_value(k, stdlib_imports)}: {_build_attribute_value(v, stdlib_imports)}' for k, v in value.items())}}}"
    else:
        return str(value)
