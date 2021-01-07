import argparse
import json
from decimal import Decimal
from typing import Optional

import toml

from coverage_threshold.cli import colors
from coverage_threshold.lib import check_all
from coverage_threshold.lib.check_result import fold_check_results
from coverage_threshold.model.config import Config
from coverage_threshold.model.report import ReportModel

parser = argparse.ArgumentParser(description="")
parser.add_argument(
    "--line-coverage-min",
    type=Decimal,
    required=False,
    help="minimum global average line coverage threshold",
)
parser.add_argument(
    "--branch-coverage-min",
    type=Decimal,
    required=False,
    help="minimum global average branch coverage threshold",
)
parser.add_argument(
    "--file-line-coverage-min",
    type=Decimal,
    required=False,
    help="the coverage threshold for each file",
)
parser.add_argument(
    "--coverage-json",
    type=str,
    default="./coverage.json",
    help="path to coverage json (default: ./coverage.json)",
)
parser.add_argument(
    "--config",
    type=str,
    default="./pyproject.toml",
    help="path to config toml (default: ./coverage.json)",
)


class ArgsNamespace(argparse.Namespace):
    line_coverage_min: Optional[Decimal]
    file_line_coverage_min: Optional[Decimal]
    coverage_json: str
    config: str


def bool_to_return_status(x: bool) -> int:
    return 0 if x else 1


def read_report(coverage_json_filename: str) -> ReportModel:
    with open(coverage_json_filename) as coverage_json_file:
        return ReportModel.parse(json.loads(coverage_json_file.read()))


def read_config(config_file_name: str) -> Config:
    return Config.parse(toml.load(config_file_name).get("coverage-threshold", {}))


def combine_config_with_args(args: ArgsNamespace, config: Config) -> Config:
    return Config(
        line_coverage_min=(
            args.line_coverage_min
            if args.line_coverage_min is not None
            else config.line_coverage_min
        ),
        file_line_coverage_min=(
            args.file_line_coverage_min
            if args.file_line_coverage_min is not None
            else config.file_line_coverage_min
        ),
        branch_coverage_min=(
            args.branch_coverage_min
            if args.branch_coverage_min is not None
            else config.branch_coverage_min
        ),
        modules=config.modules,
    )


def main() -> int:
    args = parser.parse_args(namespace=ArgsNamespace())
    report = read_report(args.coverage_json)
    config_from_file = read_config(args.config)
    config = combine_config_with_args(args, config_from_file)
    all_checks = check_all(report, config)
    if all_checks.result:
        print(colors.OKGREEN + "Success!" + colors.ENDC)
    else:
        print(f"Failed with {len(all_checks.problems)} errors")
        for problem in all_checks.problems:
            print(colors.FAIL + problem + colors.ENDC)
    return bool_to_return_status(all_checks.result)
