from decimal import Decimal
from typing import Mapping, Optional

import pytest

from coverage_threshold.lib import check_all
from coverage_threshold.lib.check_result import Fail, Pass
from coverage_threshold.model.config import Config, ModuleConfig
from coverage_threshold.model.report import (
    CoverageSummaryModel,
    FileCoverageModel,
    ReportMetadata,
    ReportModel,
)


def create_report(
    files: Optional[Mapping[str, FileCoverageModel]] = None,
    meta: ReportMetadata = ReportMetadata(branch_coverage=False),
    totals: CoverageSummaryModel = CoverageSummaryModel(
        covered_lines=4,
        num_statements=4,
    ),
) -> ReportModel:
    if files is None:
        files = {"src/main.py": FileCoverageModel(summary=totals)}
    return ReportModel(
        meta=meta,
        files=files,
        totals=totals,
    )


def test_check_totals() -> None:
    assert (
        check_all(
            create_report(
                totals=CoverageSummaryModel(covered_lines=3, num_statements=4)
            ),
            Config(line_coverage_min=Decimal("75.0")),
        )
        == Pass()
    )
    assert check_all(
        create_report(totals=CoverageSummaryModel(covered_lines=2, num_statements=3)),
        Config(line_coverage_min=Decimal("67.0")),
    ) == Fail(["Total line coverage metric failed, expected 67.0, was 66.6667"])


def test_check_totals__with_number_missing_lines_max() -> None:
    report = create_report(
        totals=CoverageSummaryModel(covered_lines=3, num_statements=7)
    )
    assert (
        check_all(
            report, Config(line_coverage_min=Decimal(0), number_missing_lines_max=5)
        )
        == Pass()
    )
    assert (
        check_all(
            report, Config(line_coverage_min=Decimal(0), number_missing_lines_max=4)
        )
        == Pass()
    )
    assert check_all(
        report, Config(line_coverage_min=Decimal(0), number_missing_lines_max=3)
    ) == Fail(["Total number missing lines max failed, expected 3, was 4"])


def test_check_all_files() -> None:
    report = create_report(
        files={
            "a.py": FileCoverageModel(
                summary=CoverageSummaryModel(covered_lines=1, num_statements=2)
            ),
            "b.py": FileCoverageModel(
                summary=CoverageSummaryModel(covered_lines=3, num_statements=4)
            ),
        }
    )

    assert check_all(report, Config(file_line_coverage_min=Decimal("50.0"))) == Pass()
    assert check_all(report, Config(file_line_coverage_min=Decimal("75.0"))) == Fail(
        ['File: "a.py" failed LINE coverage metric, expected 75.0, was 50.0000']
    )


def test_checking_branch_coverage_fails_without_branch_report() -> None:
    report = create_report(meta=ReportMetadata(branch_coverage=False))
    expected_error_message = "missing number of branches or number of branches covered"

    with pytest.raises(ValueError) as e:
        check_all(report, Config(branch_coverage_min=Decimal("50.0")))
    assert str(e.value) == expected_error_message

    with pytest.raises(ValueError) as e:
        check_all(report, Config(combined_coverage_min=Decimal("50.0")))
    assert str(e.value) == expected_error_message

    with pytest.raises(ValueError) as e:
        check_all(report, Config(file_branch_coverage_min=Decimal("75.0")))
    assert str(e.value) == expected_error_message


def test_check_totals_with_branch_coverage() -> None:
    report = create_report(
        meta=ReportMetadata(branch_coverage=True),
        totals=CoverageSummaryModel(
            covered_lines=5,
            num_statements=5,
            covered_branches=3,
            num_branches=4,
        ),
    )
    assert (
        check_all(
            report,
            Config(branch_coverage_min=Decimal("75.0")),
        )
        == Pass()
    )
    assert check_all(
        report,
        Config(branch_coverage_min=Decimal("75.001")),
    ) == Fail(["Total branch coverage metric failed, expected 75.001, was 75.0000"])


def test_check_totals_with_combined_coverage() -> None:
    report = create_report(
        meta=ReportMetadata(branch_coverage=True),
        totals=CoverageSummaryModel(
            covered_lines=5,
            num_statements=5,
            covered_branches=3,
            num_branches=5,
        ),
    )
    assert (
        check_all(
            report,
            Config(combined_coverage_min=Decimal("80.0")),
        )
        == Pass()
    )
    assert check_all(
        report,
        Config(combined_coverage_min=Decimal("80.001")),
    ) == Fail(["Total combined coverage metric failed, expected 80.001, was 80.0000"])


def test_check_all_files_with_branch_coverage() -> None:
    report = create_report(
        meta=ReportMetadata(branch_coverage=True),
        files={
            "a.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=1,
                    num_branches=2,
                )
            ),
            "b.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=3,
                    num_branches=4,
                )
            ),
        },
    )

    assert check_all(report, Config(file_branch_coverage_min=Decimal("50.0"))) == Pass()
    assert check_all(report, Config(file_branch_coverage_min=Decimal("75.0"))) == Fail(
        ['File: "a.py" failed BRANCH coverage metric, expected 75.0, was 50.0000']
    )


def test_check_all_files_with_combined_coverage() -> None:
    report = create_report(
        meta=ReportMetadata(branch_coverage=True),
        files={
            "a.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=1,
                    num_branches=5,
                )
            ),
            "b.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=3,
                    num_branches=5,
                )
            ),
        },
    )

    assert (
        check_all(report, Config(file_combined_coverage_min=Decimal("60.0"))) == Pass()
    )
    assert check_all(
        report, Config(file_combined_coverage_min=Decimal("80.0"))
    ) == Fail(
        [
            'File: "a.py" failed COMBINED line plus branch coverage metric'
            + ", expected 80.0, was 60.0000"
        ]
    )


def test_module_level_config() -> None:
    report = create_report(
        meta=ReportMetadata(branch_coverage=True),
        files={
            "src/model/a.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=1,
                    num_branches=2,
                )
            ),
            "src/model/b.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=3,
                    num_branches=4,
                )
            ),
            "src/cli/command.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=5,
                    covered_branches=4,
                    num_branches=4,
                )
            ),
        },
    )

    assert (
        check_all(
            report,
            Config(
                modules={
                    "src/model/": ModuleConfig(file_branch_coverage_min=Decimal("50.0"))
                }
            ),
        )
        == Pass()
    )
    assert (
        check_all(
            report,
            Config(
                modules={
                    "src/model/": ModuleConfig(
                        file_branch_coverage_min=Decimal("75.0")
                    ),
                    "src/model/a": ModuleConfig(
                        file_branch_coverage_min=Decimal("50.0")
                    ),
                }
            ),
        )
        == Pass()
    )
    assert check_all(
        report,
        Config(
            modules={
                "src/model/": ModuleConfig(file_branch_coverage_min=Decimal("80.0")),
                "src/model/a": ModuleConfig(file_branch_coverage_min=Decimal("50.0")),
            }
        ),
    ) == Fail(
        [
            'File: "src/model/b.py" failed BRANCH coverage metric'
            + ", expected 80.0, was 75.0000"
        ]
    )
