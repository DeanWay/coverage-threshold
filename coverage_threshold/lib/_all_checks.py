from decimal import Decimal

from coverage_threshold.model.config import Config
from coverage_threshold.model.report import ReportModel

from ._file import check_all_files
from ._totals import check_totals
from .check_result import CheckResult, fold_check_results


def check_all(report: ReportModel, config: Config) -> CheckResult:
    return fold_check_results(
        [
            check_all_files(
                report,
                config,
            ),
            check_totals(report, config),
        ]
    )
