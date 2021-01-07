from decimal import Decimal

from coverage_threshold.model.config import Config
from coverage_threshold.model.report import ReportModel

from ._file import each_file_line_coverage_metric
from ._totals import total_line_coverage_metric
from .check_result import CheckResult, fold_check_results


def check_all(report: ReportModel, config: Config) -> CheckResult:
    return fold_check_results(
        [
            each_file_line_coverage_metric(
                report,
                config,
            ),
            total_line_coverage_metric(report, config),
        ]
    )
