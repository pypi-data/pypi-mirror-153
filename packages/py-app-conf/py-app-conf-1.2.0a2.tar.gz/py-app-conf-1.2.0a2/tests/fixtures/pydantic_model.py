import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple
from uuid import UUID

import pytest
from pydantic import BaseModel, Field

from tests.fixtures.data import get_default_data


class MyEnum(str, Enum):
    ONE = "one"
    TWO = "two"


class SubModel(BaseModel):
    a: str
    b: float


class MyModel(BaseModel):
    string: str
    integer: int
    custom: SubModel
    dictionary: Dict[str, SubModel]
    str_list: List[str]
    int_tuple: Tuple[int, ...]
    uuid: UUID
    date: datetime.date
    time: datetime.datetime

    default_string: str = "woo"
    default_custom: SubModel = SubModel(a="yeah", b=5.6)
    default_enum: MyEnum = MyEnum.ONE
    default_enum_list: List[MyEnum] = Field(
        default_factory=lambda: [MyEnum.ONE, MyEnum.TWO]
    )
    default_uuid_list: List[UUID] = Field(
        default_factory=lambda: [UUID("a" * 32), UUID("b" * 32)]
    )
    default_time_with_tz: datetime.datetime = datetime.datetime(
        2022, 1, 1, tzinfo=datetime.timezone.utc
    )
    default_time_list: List[datetime.datetime] = Field(
        default_factory=lambda: [
            datetime.datetime(2022, 1, 1, tzinfo=datetime.timezone.min),
            datetime.datetime(2022, 1, 2, tzinfo=datetime.timezone.max),
        ]
    )
    default_date_list: List[datetime.date] = Field(
        default_factory=lambda: [
            datetime.date(2022, 1, 1),
            datetime.date(2022, 1, 2),
        ]
    )
    file_path: Path = Path("/a/b.txt")


def get_pydantic_model_object() -> MyModel:
    all_kwargs = get_default_data()
    return MyModel(**all_kwargs)


@pytest.fixture
def pydantic_model_object() -> MyModel:
    yield get_pydantic_model_object()
