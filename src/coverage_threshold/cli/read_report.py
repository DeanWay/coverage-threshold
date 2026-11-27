import json
from typing import Optional

from coverage_threshold.model.report import ReportModel


def read_report(coverage_json_filename: Optional[str]) -> ReportModel:
    with open(coverage_json_filename or "./coverage.json") as coverage_json_file:
        return ReportModel.parse(json.loads(coverage_json_file.read()))
