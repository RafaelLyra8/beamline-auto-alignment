from dataclasses import dataclass
from typing import ClassVar

import Shadow


@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Vector2:
    x: float
    y: float


class OE:
    def __init__(self, shadow_oe: "Shadow.OE | Shadow.Source", name: str):
        self.shadow_oe = shadow_oe
        self.name = name
        self.idx: int | None = None

    def run(self,beam:Shadow.Beam) -> Shadow.Beam:
        ...


class OE_Container:
    def __init__(self):
        self.oe_list = []
        self._name_counter = {}

    def create_oe(self, shadow_oe: Shadow.OE, name: str) -> OE:
        unique_name = self._get_unique_name(name)
        oe = OE(shadow_oe, unique_name, len(self.oe_list) + 1)
        self.append(oe)
        return oe

    def append(self, oe: OE) -> None:
        if oe.idx is not None:
            raise ValueError(f"OE '{oe.name}' is already in a container")
        oe.idx = len(self.oe_list)
        self.oe_list.append(oe)
        setattr(self, oe.name, oe)

    def _get_unique_name(self, base_name: str) -> str:
        count = self._name_counter.get(base_name, 0) + 1
        self._name_counter[base_name] = count
        return base_name if count == 1 else f"{base_name}_{count}"

    def first_last_slicing_idx(self, first: int, last: int) -> slice:
        return slice(first, None if last is None else last + 1)

    def first_last_slicing(self, first=None, last=None) -> slice:
        first = self._resolve_to_idx(first)
        last = self._resolve_to_idx(last)
        return self.first_last_slicing_idx(first, last)

    def _resolve_to_idx(self, value):
        if isinstance(value, str):
            return self.get_oe_idx(value)
        return value

    def get_oe_idx(self, name: str) -> int:
        for oe in self.oe_list:
            if oe.name == name:
                return oe.idx
        raise ValueError(f"OE with name '{name}' not found.")
