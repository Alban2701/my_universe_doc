from typing import TypeVar

T = TypeVar("T")


def is_not_none(elem: T | None, name_elem: str | None = None) -> T:
    if elem is None:
        raise ValueError(f"l'élément {name_elem} vaut None")
    else:
        return elem
