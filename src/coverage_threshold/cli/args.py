import argparse
from decimal import Decimal
from typing import Optional

from coverage_threshold.lib.alternative import fallback
from coverage_threshold.model.config import Config

parser = argparse.ArgumentParser(
    description=(
        "A command line tool for checking coverage reports "
        + "against configurable coverage minimums"
    )
)
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
    "--combined-coverage-min",
    type=Decimal,
    required=False,
    help="minimum global average combined line and branch coverage threshold",
)
parser.add_argument(
    "--number-missing-lines-max",
    type=int,
    required=False,
    help="maximum global threshold for lines not covered",
)
parser.add_argument(
    "--file-line-coverage-min",
    type=Decimal,
    required=False,
    help="the line coverage threshold for each file",
)
parser.add_argument(
    "--file-branch-coverage-min",
    type=Decimal,
    required=False,
    help="the branch coverage threshold for each file",
)
parser.add_argument(
    "--file-combined-coverage-min",
    type=Decimal,
    required=False,
    help="the combined line and branch coverage threshold for each file",
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
    default=None,
    help="path to config file (default: ./pyproject.toml)",
)


class ArgsNamespace(argparse.Namespace):
    line_coverage_min: Optional[Decimal]
    branch_coverage_min: Optional[Decimal]
    combined_coverage_min: Optional[Decimal]
    number_missing_lines_max: Optional[int]
    file_line_coverage_min: Optional[Decimal]
    file_branch_coverage_min: Optional[Decimal]
    file_combined_coverage_min: Optional[Decimal]
    coverage_json: str
    config: str


def combine_config_with_args(args: ArgsNamespace, config: Config) -> Config:
    return Config(
        line_coverage_min=fallback(args.line_coverage_min, config.line_coverage_min),
        branch_coverage_min=fallback(
            args.branch_coverage_min, config.branch_coverage_min
        ),
        combined_coverage_min=fallback(
            args.combined_coverage_min, config.combined_coverage_min
        ),
        number_missing_lines_max=fallback(
            args.number_missing_lines_max, config.number_missing_lines_max
        ),
        file_line_coverage_min=fallback(
            args.file_line_coverage_min, config.file_line_coverage_min
        ),
        file_branch_coverage_min=fallback(
            args.file_branch_coverage_min, config.file_branch_coverage_min
        ),
        file_combined_coverage_min=fallback(
            args.file_combined_coverage_min, config.file_combined_coverage_min
        ),
        modules=config.modules,
    )
