from decimal import Decimal

from coverage_threshold.model.config import Config
from coverage_threshold.model.coverage_json import JsonReportModel

from .check_result import CheckResult, fold_check_results
from ._file import each_file_line_coverage_metric
from ._totals import total_line_coverage_metric


def check_all(report: JsonReportModel, config: Config) -> CheckResult:
    return fold_check_results(
        [
            each_file_line_coverage_metric(
                report, config.line_coverage_threshold_for_every_file or Decimal("100.0")
            ),
            total_line_coverage_metric(report, config.total_line_coverage_threshold or Decimal("0.0")),
        ]
    )
