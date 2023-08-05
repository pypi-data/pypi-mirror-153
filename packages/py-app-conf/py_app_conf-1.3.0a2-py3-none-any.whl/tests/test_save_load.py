import shutil
from pathlib import Path
from typing import Optional, Tuple, Type

import pytest
from pydantic import BaseModel

from pyappconf.model import AppConfig, BaseConfig, ConfigFormats
from tests.config import (
    DATA_NAME,
    GENERATED_DATA_DIR,
    INPUT_DATA_DIR,
    JSON_PATH,
    NON_EXISTENT_INPUT_JSON_PATH,
    NON_EXISTENT_NAME,
    RECURSIVE_INPUT_FOLDER,
    TOML_PATH,
    YAML_PATH,
)
from tests.fixtures.data import get_default_data
from tests.fixtures.model import (
    MyConfigPyFormat,
    SubModel,
    get_model_classes,
    get_model_object,
    model_class_with_defaults,
    model_classes,
    model_object,
    model_object_with_defaults,
)
from tests.fixtures.temp_folder import temp_folder


def _save_load_test(custom_settings: AppConfig) -> Tuple[BaseConfig, Type[BaseConfig]]:
    mod = get_model_object(settings=custom_settings)
    mod.save()
    assert str(mod.settings.config_location).endswith(
        custom_settings.default_format.value
    )

    OrigConfig, SubModel = get_model_classes()

    class MyConfig(OrigConfig):
        _settings = custom_settings

    assert str(MyConfig._settings.config_location).endswith(
        custom_settings.default_format.value
    )
    obj = MyConfig.load()
    # Check that loaded config is the same as the one used for saving
    assert mod == obj
    return obj, MyConfig


def test_save_load_toml():
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.TOML,
    )
    _save_load_test(custom_settings)


def test_save_load_yaml():
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.YAML,
    )
    _save_load_test(custom_settings)


def test_save_load_json():
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.JSON,
    )
    _save_load_test(custom_settings)


def test_save_load_py_config():
    """
    This is structured differently than other save/load tests because py config functionality
    will not work correctly when dynamically modifying the class settings just before load.
    py config uses the imported class to create the config object, and that imported class
    does not have the dynamic modifications applied.
    :return:
    """
    all_kwargs = get_default_data()
    mod = MyConfigPyFormat(**all_kwargs)
    mod.save()
    settings = MyConfigPyFormat._settings
    assert str(mod.settings.config_location).endswith(settings.default_format.value)

    obj = MyConfigPyFormat.load()
    # Check that loaded config is the same as the one used for saving
    assert mod == obj


def test_save_load_yaml_with_schema():
    expect_schema_url = "https://example.com/schema.json"
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.YAML,
        schema_url=expect_schema_url,
    )
    obj, MyConfig = _save_load_test(custom_settings)
    assert MyConfig._settings.schema_url == expect_schema_url
    yaml_str = obj.to_yaml()
    assert expect_schema_url in yaml_str
    yaml_str_no_schema = obj.to_yaml(include_schema_url=False)
    assert expect_schema_url not in yaml_str_no_schema


def test_save_load_json_with_schema():
    expect_schema_url = "https://example.com/schema.json"
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.JSON,
        schema_url=expect_schema_url,
    )
    obj, MyConfig = _save_load_test(custom_settings)
    assert MyConfig._settings.schema_url == expect_schema_url
    json_str = obj.to_json()
    assert expect_schema_url in json_str
    json_str_no_schema = obj.to_json(include_schema_url=False)
    assert expect_schema_url not in json_str_no_schema


def _multi_format_save_load_test(
    custom_settings: AppConfig,
) -> Tuple[BaseConfig, Type[BaseConfig]]:
    # Save in a format other than the default format
    settings_with_other_format: Optional[AppConfig] = None
    for config_format in ConfigFormats:
        if config_format == custom_settings.default_format:
            continue
        settings_with_other_format = custom_settings.copy(default_format=config_format)
    if settings_with_other_format is None:
        raise ValueError("No other formats to test")

    mod = get_model_object(settings=custom_settings)
    mod.save()
    assert str(mod.settings.config_location).endswith(
        custom_settings.default_format.value
    )

    OrigConfig, SubModel = get_model_classes()

    # Now MyConfig is configured with a different format, so it could only be loaded
    # via multi-format
    class MyConfig(OrigConfig):
        _settings = settings_with_other_format

    assert str(MyConfig._settings.config_location).endswith(
        settings_with_other_format.default_format.value
    )
    obj = MyConfig.load(multi_format=True)
    # Check that loaded config is the same as the one used for saving
    assert obj == mod.copy(
        update=dict(
            settings=mod.settings.copy(default_format=custom_settings.default_format)
        )
    )
    return obj, MyConfig


def test_multi_format_save_load_toml(temp_folder: Path):
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=temp_folder,
        default_format=ConfigFormats.TOML,
        py_config_imports=[
            "from tests.fixtures.model import MyConfig, SubModel, MyEnum"
        ],
    )
    _multi_format_save_load_test(custom_settings)


def test_multi_format_save_load_yaml(temp_folder: Path):
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=temp_folder,
        default_format=ConfigFormats.YAML,
        py_config_imports=[
            "from tests.fixtures.model import MyConfig, SubModel, MyEnum"
        ],
    )
    _multi_format_save_load_test(custom_settings)


def test_multi_format_save_load_json(temp_folder: Path):
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=temp_folder,
        default_format=ConfigFormats.JSON,
        py_config_imports=[
            "from tests.fixtures.model import MyConfig, SubModel, MyEnum"
        ],
    )
    _multi_format_save_load_test(custom_settings)


def test_multi_format_save_load_py_config(temp_folder: Path):
    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=temp_folder,
        default_format=ConfigFormats.PY,
        config_name="with-dashes and spaces",
        py_config_imports=[
            "from tests.fixtures.model import MyConfig, SubModel, MyEnum"
        ],
    )
    _multi_format_save_load_test(custom_settings)


def assert_model_loaded_with_extension(
    mod: BaseConfig, model_object: BaseConfig, config_format: ConfigFormats
):
    assert mod.settings.custom_config_folder == INPUT_DATA_DIR
    assert mod.settings.default_format == config_format
    assert mod.settings.config_name == DATA_NAME

    mod.settings = model_object.settings
    assert mod == model_object


def test_load_toml_with_custom_path(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    orig_config_location = MyConfig._settings.config_location
    mod = MyConfig.load(TOML_PATH)
    assert mod._settings.config_location == orig_config_location
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.TOML)


def test_load_yaml_with_custom_path(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    orig_config_location = MyConfig._settings.config_location
    mod = MyConfig.load(YAML_PATH)
    assert mod._settings.config_location == orig_config_location
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.YAML)


def test_load_json_with_custom_path(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    orig_config_location = MyConfig._settings.config_location
    mod = MyConfig.load(JSON_PATH)
    assert mod._settings.config_location == orig_config_location
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.JSON)


def test_load_or_create_with_path_exists(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, _ = model_classes
    orig_config_location = MyConfig._settings.config_location
    mod = MyConfig.load_or_create(JSON_PATH)
    assert mod._settings.config_location == orig_config_location
    assert_model_loaded_with_extension(mod, model_object, ConfigFormats.JSON)


def test_load_or_create_with_path_does_not_exist(
    model_object_with_defaults: BaseConfig, model_class_with_defaults: Type[BaseConfig]
):
    MyConfig = model_class_with_defaults
    model_object = model_object_with_defaults
    orig_config_location = MyConfig._settings.config_location
    mod = MyConfig.load_or_create(NON_EXISTENT_INPUT_JSON_PATH)
    assert mod._settings.config_location == orig_config_location
    assert mod.settings.custom_config_folder == INPUT_DATA_DIR
    assert mod.settings.default_format == ConfigFormats.JSON
    assert mod.settings.config_name == NON_EXISTENT_NAME

    mod.settings = model_object.settings
    assert mod == model_object


@pytest.mark.parametrize(
    "path, expect_string",
    [
        (RECURSIVE_INPUT_FOLDER / "1", "loaded from 1"),
        (RECURSIVE_INPUT_FOLDER / "2", "loaded from recursive"),
        # Third and fourth cases - didn't find recursive, go to default location
        (INPUT_DATA_DIR, "a"),
        (None, "a"),
    ],
)
def test_load_recursive(path: Optional[Path], expect_string: str):
    OrigConfig, SubModel = get_model_classes()

    shutil.copy(
        INPUT_DATA_DIR / "data.toml", GENERATED_DATA_DIR / "recursive-config.toml"
    )

    custom_settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        config_name="recursive-config",
    )

    class MyConfig(OrigConfig):
        _settings = custom_settings

    orig_config_location = MyConfig._settings.config_location
    mod = MyConfig.load_recursive(path)
    assert mod._settings.config_location == orig_config_location

    assert mod.string == expect_string
