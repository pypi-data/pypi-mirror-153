from pathlib import Path
from typing import Any, Dict, Type

import toml
from pydantic import BaseModel
from toml import TomlEncoder


def add_model_to_pyproject_toml(
    config_data: Dict[str, Any],
    path: Path,
    config_name: str,
    toml_encoder: Type[TomlEncoder],
) -> str:
    if path.exists():
        data = toml.load(path)
    else:
        data = {}

    if "tool" not in data:
        data["tool"] = {}

    data["tool"][config_name] = config_data

    toml_str = toml.dumps(data, encoder=toml_encoder())
    return toml_str


def read_config_data_from_pyproject_toml(path: Path, config_name: str) -> dict:
    data = toml.load(path)
    return data["tool"][config_name]
