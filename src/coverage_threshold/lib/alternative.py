from typing import Optional, TypeVar

T = TypeVar("T")


def fallback(left: Optional[T], right: Optional[T]) -> Optional[T]:
    """
    >>> left = object()
    >>> right = object()

    >>> result = fallback(None, None)
    >>> result is None
    True

    >>> result = fallback(left, None)
    >>> result is left
    True

    >>> result = fallback(None, right)
    >>> result is right
    True

    >>> result = fallback(left, right)
    >>> result is left
    True
    """
    return left if left is not None else right
