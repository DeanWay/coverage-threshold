from decimal import Decimal
from itertools import chain
from typing import Callable, Optional, Union

from coverage_threshold.model.config import Config, ModuleConfig
from coverage_threshold.model.report import FileCoverageModel, ReportModel

from ._common import (
    check_branch_coverage_min,
    check_combined_coverage_min,
    check_line_coverage_min,
)
from .check_result import CheckResult, fold_check_results


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


def threshold_from_config_and_module_config(
    config: Config,
    module_config: Optional[ModuleConfig],
    attribute: Callable[[Union[Config, ModuleConfig]], Optional[Decimal]],
) -> Optional[Decimal]:
    if module_config is not None and attribute(module_config) is not None:
        return attribute(module_config)
    else:
        return attribute(config)


def check_file_line_coverage_min(
    filename: str,
    file_coverage: FileCoverageModel,
    config: Config,
    module_config: Optional[ModuleConfig],
) -> CheckResult:
    def file_line_coverage_min_from_config(
        config_obj: Union[Config, ModuleConfig]
    ) -> Optional[Decimal]:
        return config_obj.file_line_coverage_min

    return check_line_coverage_min(
        summary=file_coverage.summary,
        threshold=threshold_from_config_and_module_config(
            config, module_config, attribute=file_line_coverage_min_from_config
        ),
        failure_message_prefix=f'File: "{filename}" failed LINE coverage metric',
    )


def check_file_branch_coverage_min(
    filename: str,
    file_coverage: FileCoverageModel,
    config: Config,
    module_config: Optional[ModuleConfig],
) -> CheckResult:
    def file_branch_coverage_min_from_config(
        config_obj: Union[Config, ModuleConfig]
    ) -> Optional[Decimal]:
        return config_obj.file_branch_coverage_min

    return check_branch_coverage_min(
        summary=file_coverage.summary,
        threshold=threshold_from_config_and_module_config(
            config, module_config, attribute=file_branch_coverage_min_from_config
        ),
        failure_message_prefix=f'File: "{filename}" failed BRANCH coverage metric',
    )


def check_file_combined_coverage_min(
    filename: str,
    file_coverage: FileCoverageModel,
    config: Config,
    module_config: Optional[ModuleConfig],
) -> CheckResult:
    def file_branch_coverage_min_from_config(
        config_obj: Union[Config, ModuleConfig]
    ) -> Optional[Decimal]:
        return config_obj.file_combined_coverage_min

    return check_combined_coverage_min(
        summary=file_coverage.summary,
        threshold=threshold_from_config_and_module_config(
            config, module_config, attribute=file_branch_coverage_min_from_config
        ),
        failure_message_prefix=f'File: "{filename}" failed COMBINED line plus branch coverage metric',
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
                config=config,
                module_config=module_config,
            ),
            check_file_combined_coverage_min(
                filename=filename,
                file_coverage=file_coverage,
                config=config,
                module_config=module_config,
            ),
        ]
        for filename, file_coverage, module_config in files_with_module_config
    )
    return fold_check_results(chain(*file_checks))
