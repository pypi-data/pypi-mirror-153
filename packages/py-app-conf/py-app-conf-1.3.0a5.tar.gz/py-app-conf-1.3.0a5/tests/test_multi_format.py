import shutil
from pathlib import Path

from pyappconf import ConfigFormats
from tests.config import (
    JSON_PATH,
    PY_CONFIG_PATH,
    PYPROJECT_TOML_CLEAN_CONFIG_PATH,
    TOML_PATH,
    YAML_PATH,
)
from tests.fixtures.model import MyConfig, model_object
from tests.fixtures.temp_folder import temp_folder


def test_load_yaml_via_multi_format(temp_folder: Path, model_object: MyConfig):
    shutil.copy(YAML_PATH, temp_folder / "config.yaml")

    config = MyConfig.load(temp_folder, multi_format=True)
    expect_altered_settings = MyConfig._settings_with_overrides(
        custom_config_folder=temp_folder, default_format=ConfigFormats.YAML
    )
    assert config == model_object.copy(update=dict(settings=expect_altered_settings))


def test_load_json_via_multi_format(temp_folder: Path, model_object: MyConfig):
    shutil.copy(JSON_PATH, temp_folder / "config.json")

    config = MyConfig.load(temp_folder, multi_format=True)
    expect_altered_settings = MyConfig._settings_with_overrides(
        custom_config_folder=temp_folder, default_format=ConfigFormats.JSON
    )
    assert config == model_object.copy(update=dict(settings=expect_altered_settings))


def test_load_toml_via_multi_format(temp_folder: Path, model_object: MyConfig):
    shutil.copy(TOML_PATH, temp_folder / "config.toml")

    config = MyConfig.load(temp_folder, multi_format=True)
    expect_altered_settings = MyConfig._settings_with_overrides(
        custom_config_folder=temp_folder, default_format=ConfigFormats.TOML
    )
    assert config == model_object.copy(update=dict(settings=expect_altered_settings))


def test_load_py_config_via_multi_format(temp_folder: Path, model_object: MyConfig):
    shutil.copy(PY_CONFIG_PATH, temp_folder / "config.py")

    config = MyConfig.load(temp_folder, multi_format=True)
    expect_altered_settings = MyConfig._settings_with_overrides(
        custom_config_folder=temp_folder, default_format=ConfigFormats.PY
    )
    assert config == model_object.copy(update=dict(settings=expect_altered_settings))


def test_load_pyproject_toml_via_multi_format(
    temp_folder: Path, model_object: MyConfig
):
    shutil.copy(PYPROJECT_TOML_CLEAN_CONFIG_PATH, temp_folder / "pyproject.toml")

    config = MyConfig.load(temp_folder, multi_format=True)
    expect_altered_settings = MyConfig._settings_with_overrides(
        custom_config_folder=temp_folder, default_format=ConfigFormats.PYPROJECT
    )
    assert config == model_object.copy(update=dict(settings=expect_altered_settings))
