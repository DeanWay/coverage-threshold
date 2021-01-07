from coverage_threshold.model.report import ReportModel
from decimal import Decimal
from .check_result import CheckResult, Fail, Pass, fold_check_results
from ._common import percent_lines_covered


def total_line_coverage_metric(
    report: ReportModel, threshold: Decimal
) -> CheckResult:
    percent_lines_covered_for_file = percent_lines_covered(report.totals)
    if percent_lines_covered_for_file >= threshold:
        return Pass()
    else:
        return Fail(
            [
                f"Total line coverage metric failed,"
                + f" expected: {threshold}, was {percent_lines_covered_for_file}"
            ]
        )
