from dataclasses import dataclass
from functools import reduce
from typing import TYPE_CHECKING, Iterable, List, Union

if TYPE_CHECKING:
    from typing_extensions import Literal  # pragma: no cover


@dataclass(frozen=True)
class Pass:
    result: "Literal[True]" = True


@dataclass(frozen=True)
class Fail:
    problems: List[str]
    result: "Literal[False]" = False


CheckResult = Union[Fail, Pass]


def combine_check_results(first: CheckResult, second: CheckResult) -> CheckResult:
    if isinstance(first, Pass):
        return second
    elif isinstance(second, Pass):
        return first
    else:
        return Fail(first.problems + second.problems)


def fold_check_results(results: Iterable[CheckResult]) -> CheckResult:
    return reduce(combine_check_results, results)
