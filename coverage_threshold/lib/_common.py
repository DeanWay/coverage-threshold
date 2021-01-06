from coverage_threshold.model.coverage_json import CoverageSummaryModel
from decimal import Decimal


def percent_lines_covered(summary: CoverageSummaryModel) -> Decimal:
    if summary.num_statements == 0:
        return Decimal(0)
    else:
        return (
            Decimal(summary.covered_lines) / Decimal(summary.num_statements)
        ) * Decimal("100.0")
