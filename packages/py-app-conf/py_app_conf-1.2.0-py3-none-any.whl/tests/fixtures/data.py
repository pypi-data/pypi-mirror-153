from typing import Any, Dict, Optional, Sequence


def get_default_data(
    exclude_keys: Optional[Sequence[str]] = None, **kwargs
) -> Dict[str, Any]:
    from tests.fixtures.pydantic_model import SubModel

    all_kwargs = dict(
        string="a",
        integer=5,
        custom=SubModel(a="b", b=8.5),
        dictionary={"yeah": SubModel(a="c", b=9.6)},
        str_list=["a", "b", "c"],
        int_tuple=(1, 2, 3),
    )
    if exclude_keys is not None:
        all_kwargs = {
            key: value for key, value in all_kwargs.items() if key not in exclude_keys
        }
    all_kwargs.update(kwargs)
    return all_kwargs
