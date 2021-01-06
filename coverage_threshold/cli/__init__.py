import argparse
import json
from decimal import Decimal
from typing import NamedTuple

from coverage_threshold.model.coverage_json import JsonReportModel
from coverage_threshold.lib import (
    all_files_at_or_above_threshold,
    average_line_coverage_at_or_above_threshold,
)


parser = argparse.ArgumentParser(description="")
parser.add_argument(
    "--min-average-line-threshold",
    type=Decimal,
    default=Decimal("100.0"),
    help="minimum global average line coverage threshold",
)
parser.add_argument(
    "--min-file-line-threshold",
    type=Decimal,
    default=Decimal("0"),
    help="the coverage threshold",
)
parser.add_argument(
    "--coverage-json",
    type=str,
    default="./coverage.json",
    help="path to coverage json (default: ./coverage.json)",
)


class ArgsNamespace(argparse.Namespace):
    min_average_line_threshold: Decimal
    min_file_line_threshold: Decimal
    coverage_json: str


def bool_to_return_status(x: bool) -> int:
    return 0 if x else 1


def read_report(coverage_json_filename: str) -> JsonReportModel:
    with open(coverage_json_filename) as coverage_json_file:
        return JsonReportModel.parse(json.loads(coverage_json_file.read()))


def main() -> int:
    args = parser.parse_args(namespace=ArgsNamespace)
    report = read_report(args.coverage_json)
    result = all(
        [
            average_line_coverage_at_or_above_threshold(
                report, args.min_average_line_threshold
            ),
            all_files_at_or_above_threshold(report, args.min_file_line_threshold),
        ]
    )
    if result:
        print("Success!")
    else:
        print("Fail!")
    return bool_to_return_status(result)
