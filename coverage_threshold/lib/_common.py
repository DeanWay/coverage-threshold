from decimal import Decimal

from coverage_threshold.model.report import CoverageSummaryModel


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
