from coverage_threshold.model.coverage_json import JsonReportModel, FileCoverageModel
from decimal import Decimal
from .check_result import CheckResult, Fail, Pass, fold_check_results
from ._common import percent_lines_covered


def file_at_or_above_line_threshold(
    filename: str, file: FileCoverageModel, threshold: Decimal
) -> CheckResult:
    percent_lines_covered_for_file = percent_lines_covered(file.summary)
    if percent_lines_covered_for_file >= threshold:
        return Pass()
    else:
        return Fail(
            [
                f'File: "{filename}" failed line coverage metric,'
                + f" expected: {threshold}, was {percent_lines_covered_for_file}"
            ]
        )


def each_file_line_coverage_metric(
    report: JsonReportModel, threshold: Decimal
) -> CheckResult:
    return fold_check_results(
        file_at_or_above_line_threshold(filename, file, threshold)
        for filename, file in report.files.items()
    )
