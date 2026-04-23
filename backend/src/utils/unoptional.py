from typing import Type, TypeVar

T = TypeVar("T")


def unoptional(elem: T | None, name_elem: str | None = None, to_raise: Type[Exception] = ValueError) -> T:
    """Take an element which can be optional, and raise an error if it is None

    Args:
        elem (T | None): The checked element
        name_elem (str | None, optional): The name of the element - For the raise message. Defaults to None.

    Raises:
        ValueError: If the element is None

    Returns:
        elem: the element without None Type
    """
    if elem is None:
        raise ValueError(f"l'élément {name_elem} vaut None")
    else:
        return elem
