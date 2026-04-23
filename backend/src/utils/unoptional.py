from typing import Type, TypeVar

from fastapi import HTTPException

T = TypeVar("T")


def unoptional(elem: T | None, exception_message: str | None = None, to_raise: str = "ValueError") -> T:
    """Take an element which can be optional, and raise an error if it is None

    Args:
        elem (T | None): The checked element
        exception_message (str | None, optional): The name of the element - For the raise message. Defaults to None.

    Raises:
        ValueError: If the element is None

    Returns:
        elem: the element without None Type
    """
    if elem is None:
        if to_raise:
            if to_raise == "HttpException":
                raise HTTPException(status_code=404, detail=exception_message)
        
        raise ValueError(exception_message)
    else:
        return elem
