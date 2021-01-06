from coverage_threshold.model.coverage_json import JsonReportModel
from decimal import Decimal
from ._common import percent_lines_covered


def average_line_coverage_at_or_above_threshold(
    report: JsonReportModel, threshold: Decimal
) -> bool:
    return percent_lines_covered(report.totals) >= threshold
