import json

from coverage_threshold.model.report import ReportModel


def read_report(coverage_json_filename: str) -> ReportModel:
    with open(coverage_json_filename) as coverage_json_file:
        return ReportModel.parse(json.loads(coverage_json_file.read()))
