from enum import Enum
from typing import Optional, Sequence, Tuple, Type

import pytest
from pydantic import BaseModel

from pyappconf.model import AppConfig, BaseConfig, ConfigFormats
from tests.config import ENV_PATH, GENERATED_DATA_DIR
from tests.fixtures.data import get_default_data
from tests.fixtures.pydantic_model import MyModel, SubModel


class MyEnum(str, Enum):
    ONE = "one"
    TWO = "two"


class MyConfig(MyModel, BaseConfig):
    _settings: AppConfig = AppConfig(
        app_name="MyApp",
        py_config_imports=[
            "from tests.fixtures.model import MyConfig, SubModel, MyEnum"
        ],
    )

    class Config:
        env_prefix = "MYAPP_"
        env_file = ENV_PATH


class MyConfigPyFormat(MyConfig):
    _settings = AppConfig(
        app_name="MyApp",
        custom_config_folder=GENERATED_DATA_DIR,
        default_format=ConfigFormats.PY,
        py_config_imports=[
            "from tests.fixtures.model import MyConfigPyFormat, SubModel, MyEnum"
        ],
    )


def get_model_classes() -> Tuple[Type[BaseConfig], Type[BaseModel]]:
    return MyConfig, SubModel


def get_model_class_with_defaults() -> Type[BaseConfig]:
    class MyDefaultConfig(BaseConfig):
        a: str = "a"
        b: int = 2

        _settings: AppConfig = AppConfig(app_name="MyApp")

        class Config:
            env_prefix = "MYAPP_"
            env_file = ENV_PATH

    return MyDefaultConfig


def get_model_object(
    exclude_keys: Optional[Sequence[str]] = None, **kwargs
) -> BaseConfig:
    MyConfig, SubModel = get_model_classes()
    all_kwargs = get_default_data(exclude_keys=exclude_keys, **kwargs)
    conf = MyConfig(**all_kwargs)
    return conf


def get_model_object_with_defaults() -> BaseConfig:
    MyDefaultConfig = get_model_class_with_defaults()
    return MyDefaultConfig()


@pytest.fixture(scope="session")
def model_classes() -> Tuple[Type[BaseConfig], Type[BaseModel]]:
    return get_model_classes()


@pytest.fixture(scope="session")
def model_class_with_defaults() -> Type[BaseConfig]:
    return get_model_class_with_defaults()


@pytest.fixture(scope="session")
def model_object() -> BaseConfig:
    return get_model_object()


@pytest.fixture(scope="session")
def model_object_with_defaults() -> BaseConfig:
    return get_model_object_with_defaults()
