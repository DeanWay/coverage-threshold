from typing import Any, Optional, Type, TypeVar

T = TypeVar("T", bound=Any)


def parse_option_field(
    obj: Any, type_constructor: Type[T], field_name: str
) -> Optional[T]:
    return (
        type_constructor(obj[field_name])
        if field_name in obj and obj[field_name] is not None
        else None
    )
