from enum import Enum
from pathlib import Path, PosixPath
from typing import Any, Callable, Dict, Type
from uuid import UUID

from toml.encoder import TomlEncoder, _dump_str  # type: ignore

from pyappconf.encoding.general import HasStr


def _dump_hasstr(obj: HasStr) -> str:
    return _dump_str(str(obj))


def _dump_enum(obj: Enum) -> str:
    return _dump_str(obj.value)


def _dump_uuid(obj: UUID) -> str:
    return _dump_str(str(obj))


class CustomTomlEncoder(TomlEncoder):
    multi_dump_funcs: Dict[Type, Callable[[Any], str]]

    def __init__(self, _dict=dict, preserve=False):
        super().__init__(_dict=_dict, preserve=preserve)
        self.multi_dump_funcs = {Enum: _dump_enum, UUID: _dump_uuid}
        self.dump_funcs[Path] = _dump_hasstr
        self.dump_funcs[PosixPath] = _dump_hasstr

    def dump_value(self, v):
        """
        Overrides TomlEncoder.dump_value to adds support for putting
        a base class in multi_dump_funcs and have it be used for any
        subclass of that type
        """
        # Lookup function corresponding to v's type
        dump_fn = self.dump_funcs.get(type(v))
        if dump_fn is None:
            for base_cls, fn in self.multi_dump_funcs.items():
                if isinstance(v, base_cls):
                    dump_fn = fn
            if dump_fn is not None:
                # Got a multi dump function
                return dump_fn(v)
        return super().dump_value(v)
