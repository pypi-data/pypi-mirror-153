from typing import Tuple, Type

from pydantic import BaseModel

from pyappconf.model import BaseConfig
from tests.config import JSON_PATH, SCHEMA_JSON_PATH, TOML_PATH, YAML_PATH
from tests.fixtures.model import model_classes, model_object


def test_to_json(model_object: BaseConfig):
    assert model_object.to_json() == JSON_PATH.read_text()


def test_to_yaml(model_object: BaseConfig):
    assert model_object.to_yaml() == YAML_PATH.read_text()


def test_to_toml(model_object: BaseConfig):
    assert model_object.to_toml() == TOML_PATH.read_text()


def test_from_json(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, SubModel = model_classes
    loaded_object = MyConfig.parse_json(JSON_PATH)
    assert model_object == loaded_object


def test_from_yaml(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, SubModel = model_classes
    loaded_object = MyConfig.parse_yaml(YAML_PATH)
    assert model_object == loaded_object


def test_from_toml(
    model_object: BaseConfig, model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]
):
    MyConfig, SubModel = model_classes
    loaded_object = MyConfig.parse_toml(TOML_PATH)
    assert model_object == loaded_object


def test_json_schema(model_classes: Tuple[Type[BaseConfig], Type[BaseModel]]):
    MyConfig, SubModel = model_classes
    assert MyConfig.schema_json(indent=2) == SCHEMA_JSON_PATH.read_text()
