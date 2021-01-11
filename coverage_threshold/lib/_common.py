from decimal import Decimal
from typing import TYPE_CHECKING, Callable, Optional

from coverage_threshold.model.report import CoverageSummaryModel

from .check_result import CheckResult, Fail, Pass

if TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import Protocol

    class CheckFunction(Protocol):
        def __call__(
            self,
            summary: CoverageSummaryModel,
            threshold: Optional[Decimal],
            failure_message_prefix: str,
        ) -> CheckResult:
            ...


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


def _check(
    percent_covered_function: Callable[[CoverageSummaryModel], Decimal]
) -> "CheckFunction":
    def resulting_function(
        summary: CoverageSummaryModel,
        threshold: Optional[Decimal],
        failure_message_prefix: str,
    ) -> CheckResult:
        if threshold is None:
            return Pass()
        else:
            percent_covered = percent_covered_function(summary)
            if percent_covered >= threshold:
                return Pass()
            else:
                return Fail(
                    [
                        f"{failure_message_prefix}, expected {threshold}, was {percent_covered}"
                    ]
                )

    return resulting_function


check_line_coverage_min = _check(percent_lines_covered)
check_branch_coverage_min = _check(percent_branches_covered)
check_combined_coverage_min = _check(percent_combined_lines_and_branches_covered)
