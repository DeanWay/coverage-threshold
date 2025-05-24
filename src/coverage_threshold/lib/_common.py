from decimal import Decimal
from operator import ge as greater_or_eq
from operator import le as less_or_eq
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar

from coverage_threshold.model.report import CoverageSummaryModel

from .check_result import CheckResult, Fail, Pass

Num = TypeVar("Num", Decimal, int)
if TYPE_CHECKING:
    from typing_extensions import Protocol

    T = TypeVar("T", contravariant=True)

    class CheckFunction(Protocol[T]):
        def __call__(
            self,
            summary: CoverageSummaryModel,
            threshold: Optional[T],
            failure_message_prefix: str,
        ) -> CheckResult: ...


def _safe_percent(numerator: int, denomenator: int) -> Decimal:
    if denomenator == 0:
        return Decimal(100)
    else:
        return ((Decimal(numerator) / Decimal(denomenator)) * Decimal(100)).quantize(
            Decimal("0.0001")
        )


def percent_lines_covered(summary: CoverageSummaryModel) -> Decimal:
    return _safe_percent(summary.covered_lines, summary.num_statements)


def percent_branches_covered(summary: CoverageSummaryModel) -> Decimal:
    if summary.covered_branches is not None and summary.num_branches is not None:
        return _safe_percent(summary.covered_branches, summary.num_branches)
    else:
        raise ValueError("missing number of branches or number of branches covered")


def percent_combined_lines_and_branches_covered(
    summary: CoverageSummaryModel,
) -> Decimal:  # pragma: no cover
    if summary.covered_branches is not None and summary.num_branches is not None:
        return _safe_percent(
            summary.covered_lines + summary.covered_branches,
            summary.num_statements + summary.num_branches,
        )
    else:
        raise ValueError("missing number of branches or number of branches covered")


def number_lines_not_covered(summary: CoverageSummaryModel) -> int:
    return summary.num_statements - summary.covered_lines


def _check(
    comparison_function: Callable[[Any, Any], bool],
    coverage_value_from_summary: Callable[[CoverageSummaryModel], Num],
) -> "CheckFunction[Num]":
    def resulting_function(
        summary: CoverageSummaryModel,
        threshold: Optional[Num],
        failure_message_prefix: str,
    ) -> CheckResult:
        if threshold is None:
            return Pass()

        covered = coverage_value_from_summary(summary)
        if comparison_function(threshold, covered):
            return Pass()
        else:
            message = f"{failure_message_prefix}, expected {threshold}, was {covered}"
            return Fail([message])

    return resulting_function


check_line_coverage_min = _check(less_or_eq, percent_lines_covered)
check_branch_coverage_min = _check(less_or_eq, percent_branches_covered)
check_combined_coverage_min = _check(
    less_or_eq, percent_combined_lines_and_branches_covered
)
check_number_missing_lines_max = _check(greater_or_eq, number_lines_not_covered)
