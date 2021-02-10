from dataclasses import dataclass
from functools import reduce
from typing import TYPE_CHECKING, Iterable, List, Union

if TYPE_CHECKING:
    from typing_extensions import Literal


@dataclass(frozen=True)
class Pass:
    result: "Literal[True]" = True


@dataclass(frozen=True)
class Fail:
    problems: List[str]
    result: "Literal[False]" = False


CheckResult = Union[Fail, Pass]


def combine_check_results(first: CheckResult, second: CheckResult) -> CheckResult:
    """
    >>> combine_check_results(Pass(), Pass())
    Pass(result=True)

    >>> combine_check_results(Pass(), Fail(['no!']))
    Fail(problems=['no!'], result=False)

    >>> combine_check_results(Fail(['oh!']), Pass())
    Fail(problems=['oh!'], result=False)

    >>> combine_check_results(Fail(['oh!']), Fail(['no!']))
    Fail(problems=['oh!', 'no!'], result=False)
    """
    if isinstance(first, Pass):
        return second
    elif isinstance(second, Pass):
        return first
    else:
        return Fail(first.problems + second.problems)


def fold_check_results(results: Iterable[CheckResult]) -> CheckResult:
    return reduce(combine_check_results, results)
