from pyappconf import BaseConfig
from pyappconf.py_config.generate import pydantic_model_to_python_config_file
from tests.fixtures.pydantic_model import MyModel, pydantic_model_object


def test_pydantic_model_to_config_file(pydantic_model_object: MyModel):
    config_str = pydantic_model_to_python_config_file(
        pydantic_model_object,
        ["from tests.fixtures.pydantic_model import MyModel, SubModel, MyEnum"],
    )
    assert (
        config_str
        == 'from tests.fixtures.pydantic_model import MyModel, SubModel, MyEnum\nfrom pathlib import Path\n\nconfig = MyModel(\n    string="a",\n    integer=5,\n    custom=SubModel(a="b", b=8.5),\n    dictionary={"yeah": SubModel(a="c", b=9.6)},\n    str_list=["a", "b", "c"],\n    int_tuple=(1, 2, 3),\n    default_string="woo",\n    default_custom=SubModel(a="yeah", b=5.6),\n    default_enum=MyEnum.ONE,\n    default_enum_list=[MyEnum.ONE, MyEnum.TWO],\n    file_path=Path("/a/b.txt"),\n)\n'
    )
