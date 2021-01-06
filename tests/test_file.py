from decimal import Decimal

from coverage_threshold.model.coverage_json import (
    JsonReportModel,
    FileCoverageModel,
    CoverageSummaryModel,
    JsonReportMetadata,
)
from coverage_threshold.lib import (
    all_files_at_or_above_threshold,
    average_line_coverage_at_or_above_threshold,
)

test_report = JsonReportModel(
    meta=JsonReportMetadata(branch_coverage=False),
    files={
        "src/main.py": FileCoverageModel(
            summary=CoverageSummaryModel(
                covered_lines=1,
                num_statements=2,
                percent_covered=Decimal("50.0"),
                missing_lines=0,
                excluded_lines=0,
            )
        ),
        "src/lib.py": FileCoverageModel(
            summary=CoverageSummaryModel(
                covered_lines=2,
                num_statements=2,
                percent_covered=Decimal("100.0"),
                missing_lines=0,
                excluded_lines=0,
            )
        ),
    },
    totals=CoverageSummaryModel(
        covered_lines=3,
        num_statements=4,
        percent_covered=Decimal("75.0"),
        missing_lines=0,
        excluded_lines=0,
    ),
)


def test_all_files_at_or_above_threshold() -> None:
    assert all_files_at_or_above_threshold(test_report, Decimal("50.0"))
    assert all_files_at_or_above_threshold(test_report, Decimal("75.0")) is False


def test_average_line_coverage_at_or_above_threshold() -> None:
    assert average_line_coverage_at_or_above_threshold(test_report, Decimal("75.0"))
