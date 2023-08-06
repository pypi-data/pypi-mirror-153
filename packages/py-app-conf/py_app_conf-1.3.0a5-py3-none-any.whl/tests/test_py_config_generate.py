from pyappconf import BaseConfig
from pyappconf.py_config.generate import pydantic_model_to_python_config_file
from tests.config import PYDANTIC_PY_CONFIG_PATH
from tests.fixtures.pydantic_model import MyModel, pydantic_model_object


def test_pydantic_model_to_config_file(pydantic_model_object: MyModel):
    config_str = pydantic_model_to_python_config_file(
        pydantic_model_object,
        ["from tests.fixtures.pydantic_model import MyModel, SubModel, MyEnum"],
    )
    assert config_str == PYDANTIC_PY_CONFIG_PATH.read_text()
