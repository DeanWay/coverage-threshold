from decimal import Decimal

from coverage_threshold.model.config import Config
from coverage_threshold.model.report import ReportModel

from ._common import (
    check_branch_coverage_min,
    check_combined_coverage_min,
    check_line_coverage_min,
)
from .check_result import CheckResult, fold_check_results


def check_total_line_coverage_min(report: ReportModel, config: Config) -> CheckResult:
    threshold = (
        config.line_coverage_min
        if config.line_coverage_min is not None
        else Decimal("100.0")
    )
    return check_line_coverage_min(
        summary=report.totals,
        threshold=threshold,
        failure_message_prefix="Total line coverage metric failed",
    )


def check_total_branch_coverage_min(report: ReportModel, config: Config) -> CheckResult:
    return check_branch_coverage_min(
        summary=report.totals,
        threshold=config.branch_coverage_min,
        failure_message_prefix="Total branch coverage metric failed",
    )


def check_total_combined_coverage_min(
    report: ReportModel, config: Config
) -> CheckResult:
    return check_combined_coverage_min(
        summary=report.totals,
        threshold=config.combined_coverage_min,
        failure_message_prefix="Total combined coverage metric failed",
    )


def check_totals(report: ReportModel, config: Config) -> CheckResult:
    return fold_check_results(
        [
            check_total_line_coverage_min(report, config),
            check_total_branch_coverage_min(report, config),
            check_total_combined_coverage_min(report, config),
        ]
    )
