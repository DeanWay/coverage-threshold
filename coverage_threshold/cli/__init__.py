import argparse
import json
from decimal import Decimal
from typing import NamedTuple

from coverage_threshold.model.coverage_json import JsonReportModel
from coverage_threshold.lib import (
    each_file_line_coverage_metric,
    total_line_coverage_metric,
)
from coverage_threshold.lib.check_result import fold_check_results


parser = argparse.ArgumentParser(description="")
parser.add_argument(
    "--total-line-coverage-threshold",
    type=Decimal,
    default=Decimal("100.0"),
    help="minimum global average line coverage threshold",
)
parser.add_argument(
    "--line-coverage-threshold-for-every-file",
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
    total_line_coverage_threshold: Decimal
    line_coverage_threshold_for_every_file: Decimal
    coverage_json: str


def bool_to_return_status(x: bool) -> int:
    return 0 if x else 1


def read_report(coverage_json_filename: str) -> JsonReportModel:
    with open(coverage_json_filename) as coverage_json_file:
        return JsonReportModel.parse(json.loads(coverage_json_file.read()))


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def main() -> int:
    args = parser.parse_args(namespace=ArgsNamespace)
    report = read_report(args.coverage_json)
    result = fold_check_results(
        [
            each_file_line_coverage_metric(report, args.line_coverage_threshold_for_every_file),
            total_line_coverage_metric(report, args.total_line_coverage_threshold),
        ]
    )
    if result.result:
        print(bcolors.OKGREEN + "Success!" + bcolors.ENDC)
    else:
        print("Fail!")
        for problem in result.problems:
            print(bcolors.FAIL + problem + bcolors.ENDC)
    return bool_to_return_status(result)
