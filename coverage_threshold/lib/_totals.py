from decimal import Decimal

from coverage_threshold.model.config import Config
from coverage_threshold.model.report import ReportModel

from ._common import percent_lines_covered
from .check_result import CheckResult, Fail, Pass, fold_check_results


def check_totals(report: ReportModel, config: Config) -> CheckResult:
    percent_lines_covered_for_file = percent_lines_covered(report.totals)
    threshold = config.line_coverage_min or Decimal("100.0")
    if percent_lines_covered_for_file >= threshold:
        return Pass()
    else:
        return Fail(
            [
                f"Total line coverage metric failed,"
                + f" expected: {threshold}, was {percent_lines_covered_for_file}"
            ]
        )
