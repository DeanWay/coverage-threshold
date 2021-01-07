from decimal import Decimal

from coverage_threshold.lib import check_all_files, check_totals
from coverage_threshold.lib.check_result import Fail, Pass
from coverage_threshold.model.config import Config, ModuleConfig
from coverage_threshold.model.report import (
    CoverageSummaryModel,
    FileCoverageModel,
    ReportMetadata,
    ReportModel,
)

test_report = ReportModel(
    meta=ReportMetadata(branch_coverage=False),
    files={
        "src/main.py": FileCoverageModel(
            summary=CoverageSummaryModel(
                covered_lines=1,
                num_statements=2,
            )
        ),
        "src/lib.py": FileCoverageModel(
            summary=CoverageSummaryModel(
                covered_lines=2,
                num_statements=2,
            )
        ),
    },
    totals=CoverageSummaryModel(
        covered_lines=3,
        num_statements=4,
    ),
)


def test_check_all_files() -> None:
    assert (
        check_all_files(test_report, Config(file_line_coverage_min=Decimal("50.0")))
        == Pass()
    )
    assert check_all_files(
        test_report, Config(file_line_coverage_min=Decimal("75.0"))
    ) == Fail(
        ['File: "src/main.py" failed LINE coverage metric, expected: 75.0, was 50.0000']
    )


def test_check_totals() -> None:
    assert check_totals(test_report, Config(line_coverage_min=Decimal("75.0")))
