from pydantic import BaseModel, ValidationError
from typing import TypeVar, Type, Any

T = TypeVar('T', bound=BaseModel)

def model_validate_list(model: Type[T], lst: list[dict[str, Any]], with_invalidated: bool=False) -> list[T] | tuple[list[T], list[dict[str, Any]]]:
    """
    Helper to validate a list of model
    
    Parameters:
    - model (BaseModel): the model the objects in the list must be
    - lst (list): the list to validate
    
    Returns:
    list[BaseModel]: the list validated
    """
    validated = []
    invalidated = []
    for elem in lst:
        try:
            validated.append(model.model_validate(elem))
        except ValidationError:
            invalidated.append(elem)
    if with_invalidated:
        return validated, invalidated
    else:
        return validated