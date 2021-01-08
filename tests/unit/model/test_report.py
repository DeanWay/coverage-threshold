from decimal import Decimal

import pytest

from coverage_threshold.model.report import (
    CoverageSummaryModel,
    FileCoverageModel,
    ReportMetadata,
    ReportModel,
)


def test_report_parse__full() -> None:
    assert ReportModel.parse(
        {
            "meta": {
                "branch_coverage": True,
            },
            "files": {
                "src/__init__.py": {
                    "summary": {
                        "covered_lines": 1,
                        "num_statements": 2,
                        "num_branches": 3,
                        "covered_branches": 4,
                    },
                },
                "src/main.py": {
                    "summary": {
                        "covered_lines": 5,
                        "num_statements": 6,
                        "num_branches": 7,
                        "covered_branches": 8,
                    },
                },
            },
            "totals": {
                "covered_lines": 9,
                "num_statements": 10,
                "num_branches": 11,
                "covered_branches": 12,
            },
        }
    ) == ReportModel(
        meta=ReportMetadata(branch_coverage=True),
        files={
            "src/__init__.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=1,
                    num_statements=2,
                    num_branches=3,
                    covered_branches=4,
                )
            ),
            "src/main.py": FileCoverageModel(
                summary=CoverageSummaryModel(
                    covered_lines=5,
                    num_statements=6,
                    num_branches=7,
                    covered_branches=8,
                )
            ),
        },
        totals=CoverageSummaryModel(
            covered_lines=9,
            num_statements=10,
            num_branches=11,
            covered_branches=12,
        ),
    )
