from decimal import Decimal

from coverage_threshold.model.config import Config
from coverage_threshold.model.report import ReportModel

from ._common import percent_branches_covered, percent_lines_covered
from .check_result import CheckResult, Fail, Pass, fold_check_results


def check_total_line_coverage_min(report: ReportModel, config: Config) -> CheckResult:
    percent_total_lines_covered = percent_lines_covered(report.totals)
    threshold = (
        config.line_coverage_min
        if config.line_coverage_min is not None
        else Decimal("100.0")
    )
    if percent_total_lines_covered >= threshold:
        return Pass()
    else:
        return Fail(
            [
                f"Total line coverage metric failed,"
                + f" expected: {threshold}, was {percent_total_lines_covered}"
            ]
        )


def check_total_branch_coverage_min(report: ReportModel, config: Config) -> CheckResult:
    if config.branch_coverage_min is None:
        return Pass()
    else:
        if not report.meta.branch_coverage:
            raise ValueError(
                "trying to check branch coverage without providing"
                + " a report with branch coverage data"
            )
        percent_total_branches_covered = percent_branches_covered(report.totals)
        if percent_total_branches_covered >= config.branch_coverage_min:
            return Pass()
        else:
            return Fail(
                [
                    f"Total branch coverage metric failed,"
                    + f" expected: {config.branch_coverage_min}, was {percent_total_branches_covered}"
                ]
            )


def check_totals(report: ReportModel, config: Config) -> CheckResult:
    return fold_check_results(
        [
            check_total_line_coverage_min(report, config),
            check_total_branch_coverage_min(report, config),
        ]
    )
