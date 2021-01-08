from decimal import Decimal
from itertools import chain
from typing import Iterable, Iterator, List, Optional, Tuple

from coverage_threshold.model.config import Config, ModuleConfig
from coverage_threshold.model.report import FileCoverageModel, ReportModel

from ._common import percent_branches_covered, percent_lines_covered
from .check_result import CheckResult, Fail, Pass, fold_check_results


def best_matching_module_config_for_file(
    filename: str, config: Config
) -> Optional[ModuleConfig]:
    # naive approach here, this can be improved if this turns out to be slow
    # but for most projects we're dealing with a few thousand files so shouldn't
    # need to optomize this for most cases
    if config.modules is None:
        return None
    matches = [
        (prefix, module)
        for prefix, module in config.modules.items()
        if filename.startswith(prefix)
    ]
    if len(matches) > 0:
        return max(matches, key=lambda match: len(match[0]))[1]
    else:
        return None


def check_file_line_coverage_min(
    filename: str,
    file_coverage: FileCoverageModel,
    config: Config,
    module_config: Optional[ModuleConfig],
) -> CheckResult:
    threshold_from_config = (
        module_config.file_line_coverage_min
        if module_config is not None
        and module_config.file_line_coverage_min is not None
        else config.file_line_coverage_min
        if config.file_line_coverage_min is not None
        else None
    )
    threshold = (
        threshold_from_config if threshold_from_config is not None else Decimal(0)
    )
    percent_lines_covered_for_file = percent_lines_covered(file_coverage.summary)
    if percent_lines_covered_for_file >= threshold:
        return Pass()
    else:
        return Fail(
            [
                f'File: "{filename}" failed LINE coverage metric,'
                + f" expected: {threshold}, was {percent_lines_covered_for_file}"
            ]
        )


def check_file_branch_coverage_min(
    filename: str,
    file_coverage: FileCoverageModel,
    report: ReportModel,
    config: Config,
    module_config: Optional[ModuleConfig],
) -> CheckResult:
    threshold = (
        module_config.file_branch_coverage_min
        if module_config is not None
        else config.file_branch_coverage_min
        if config.file_branch_coverage_min is not None
        else None
    )
    if threshold is None:
        return Pass()
    else:
        if not report.meta.branch_coverage:
            raise ValueError(
                "trying to check branch coverage without providing"
                + " a report with branch coverage data"
            )
        percent_total_branches_covered = percent_branches_covered(file_coverage.summary)
        if percent_total_branches_covered >= threshold:
            return Pass()
        else:
            return Fail(
                [
                    f'File: "{filename}" failed BRANCH coverage metric,'
                    + f" expected: {threshold}, was {percent_total_branches_covered}"
                ]
            )


def check_all_files(report: ReportModel, config: Config) -> CheckResult:
    files_with_module_config = (
        (
            filename,
            file_coverage,
            best_matching_module_config_for_file(filename, config),
        )
        for filename, file_coverage in report.files.items()
    )
    file_checks = (
        [
            check_file_line_coverage_min(
                filename=filename,
                file_coverage=file_coverage,
                config=config,
                module_config=module_config,
            ),
            check_file_branch_coverage_min(
                filename=filename,
                file_coverage=file_coverage,
                report=report,
                config=config,
                module_config=module_config,
            ),
        ]
        for filename, file_coverage, module_config in files_with_module_config
    )
    return fold_check_results(chain(*file_checks))
