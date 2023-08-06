"""
Generate test data for file output
"""
from pyappconf import AppConfig
from pyappconf.py_config.generate import pydantic_model_to_python_config_file
from tests.config import (
    DATA_NAME,
    INPUT_DATA_DIR,
    JSON_PATH,
    JSON_WITH_SCHEMA_PATH,
    PY_CONFIG_PATH,
    PYDANTIC_PY_CONFIG_PATH,
    PYPROJECT_TOML_CLEAN_CONFIG_PATH,
    PYPROJECT_TOML_MIXED_CONFIG_PATH,
    RECURSIVE_CONFIG_1_PATH,
    RECURSIVE_CONFIG_ROOT_PATH,
    SCHEMA_JSON_PATH,
    TOML_PATH,
    YAML_PATH,
    YAML_WITH_SCHEMA_PATH,
)
from tests.fixtures.model import MyConfig, get_model_object
from tests.fixtures.pydantic_model import get_pydantic_model_object


def generate_basic_configs():
    conf = get_model_object()
    conf.to_json(out_path=JSON_PATH, json_kwargs=dict(indent=2))
    conf.to_yaml(out_path=YAML_PATH)
    conf.to_toml(out_path=TOML_PATH)
    conf.to_py_config(out_path=PY_CONFIG_PATH)
    conf.to_pyproject_toml(out_path=PYPROJECT_TOML_CLEAN_CONFIG_PATH)
    conf.to_pyproject_toml(out_path=PYPROJECT_TOML_MIXED_CONFIG_PATH)


def generate_configs_with_schema():
    settings_with_schema = AppConfig(
        app_name="MyApp", schema_url="https://example.com/schema.json"
    )
    conf_with_schema = get_model_object(settings=settings_with_schema)
    conf_with_schema.to_json(out_path=JSON_WITH_SCHEMA_PATH, json_kwargs=dict(indent=2))
    conf_with_schema.to_yaml(out_path=YAML_WITH_SCHEMA_PATH)


def generate_recursive_configs():
    config_1 = get_model_object(string="loaded from 1")
    config_1.to_toml(RECURSIVE_CONFIG_1_PATH)
    config_recursive = get_model_object(string="loaded from recursive")
    config_recursive.to_toml(RECURSIVE_CONFIG_ROOT_PATH)


def generate_json_schema():
    schema = MyConfig.schema_json(indent=2)
    SCHEMA_JSON_PATH.write_text(schema)


def generate_pydantic_py_config_file():
    model = get_pydantic_model_object()
    conf_str = pydantic_model_to_python_config_file(
        model,
        ["from tests.fixtures.pydantic_model import MyModel, SubModel, MyEnum"],
    )
    PYDANTIC_PY_CONFIG_PATH.write_text(conf_str)


if __name__ == "__main__":
    generate_basic_configs()
    generate_configs_with_schema()
    generate_recursive_configs()
    generate_json_schema()
    generate_pydantic_py_config_file()
