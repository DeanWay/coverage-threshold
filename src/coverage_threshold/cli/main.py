from coverage_threshold.cli import colors
from coverage_threshold.cli.args import ArgsNamespace, combine_config_with_args, parser
from coverage_threshold.cli.read_config import read_config
from coverage_threshold.cli.read_report import read_report
from coverage_threshold.lib import check_all


def bool_to_return_status(x: bool) -> int:
    return 0 if x else 1


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
