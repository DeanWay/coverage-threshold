from coverage_threshold.model.coverage_json import JsonReportModel, FileCoverageModel
from decimal import Decimal
from ._common import percent_lines_covered


def file_at_or_above_line_threshold(
    file: FileCoverageModel, threshold: Decimal
) -> bool:
    return percent_lines_covered(file.summary) >= threshold


def all_files_at_or_above_threshold(
    report: JsonReportModel, threshold: Decimal
) -> bool:
    return all(
        file_at_or_above_line_threshold(file, threshold)
        for file in report.files.values()
    )
