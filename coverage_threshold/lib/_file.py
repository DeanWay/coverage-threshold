from decimal import Decimal
from typing import Tuple, Iterator, Optional

from coverage_threshold.model.config import Config, ModuleConfig
from coverage_threshold.model.report import ReportModel, FileCoverageModel
from coverage_threshold.lib.functools import prefix_match_length
from .check_result import CheckResult, Fail, Pass, fold_check_results
from ._common import percent_lines_covered


def best_matching_module_config_for_file(
    filename: str, config: Config
) -> Optional[ModuleConfig]:
    # naive approach here, this can be improved if this turns out to be slow
    # but for most projects we're dealing with a few thousand files so shouldn't
    # need to optomize this for most cases
    if config.modules is None:
        return None
    match_length_per_module_config: Iterator[Tuple[int, ModuleConfig]] = (
        (prefix_match_length(prefix, filename), module)
        for prefix, module in config.modules.items()
    )
    matches = list(filter(lambda match: match[0] > 0, match_length_per_module_config))
    if len(matches) > 0:
        return max(matches, key=lambda match: match[0])[1]
    else:
        return None


def file_at_or_above_line_threshold(
    filename: str, file: FileCoverageModel, config: Config
) -> CheckResult:
    percent_lines_covered_for_file = percent_lines_covered(file.summary)
    module_config = best_matching_module_config_for_file(filename, config)
    threshold = (
        module_config.line_converage_threshold
        if module_config
        else config.line_coverage_threshold_for_every_file
    ) or Decimal("0")
    if percent_lines_covered_for_file >= threshold:
        return Pass()
    else:
        return Fail(
            [
                f'File: "{filename}" failed line coverage metric,'
                + f" expected: {threshold}, was {percent_lines_covered_for_file}"
            ]
        )


def each_file_line_coverage_metric(report: ReportModel, config: Config) -> CheckResult:
    return fold_check_results(
        file_at_or_above_line_threshold(filename, file, config)
        for filename, file in report.files.items()
    )
