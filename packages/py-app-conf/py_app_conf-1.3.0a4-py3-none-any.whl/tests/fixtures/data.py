import datetime
from typing import Any, Dict, Optional, Sequence
from uuid import UUID


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
        uuid=UUID("826032aa-465a-4692-b9b4-c81819197ed0"),
        date=datetime.date(2020, 1, 1),
        time=datetime.datetime(2020, 1, 1, 12, 0, 0),
    )
    if exclude_keys is not None:
        all_kwargs = {
            key: value for key, value in all_kwargs.items() if key not in exclude_keys
        }
    all_kwargs.update(kwargs)
    return all_kwargs
