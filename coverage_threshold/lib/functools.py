from typing import Callable, Iterable, Iterator, TypeVar

T = TypeVar('T')

def take_while(f: Callable[[T], bool], iterable: Iterable[T]) -> Iterator[T]:
    for x in iterable:
        if f(x):
            yield x
        else:
            break


def prefix_match_length(prefix: str, string: str) -> int:
    if not string.startswith(prefix):
        return 0
    else:
        return len(
            list(take_while(lambda pair: pair[0] == pair[1], zip(prefix, string)))
        )
