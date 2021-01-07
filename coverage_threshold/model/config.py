from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Mapping, Optional

from .util import parse_option_field


@dataclass(frozen=True)
class Config:
    line_coverage_min: Optional[Decimal] = None
    branch_coverage_min: Optional[Decimal] = None
    file_line_coverage_min: Optional[Decimal] = None
    file_branch_coverage_min: Optional[Decimal] = None
    modules: Optional[Mapping[str, ModuleConfig]] = None

    @staticmethod
    def parse(obj: Any) -> Config:
        return Config(
            line_coverage_min=parse_option_field(obj, Decimal, "line_coverage_min"),
            branch_coverage_min=parse_option_field(obj, Decimal, "branch_coverage_min"),
            file_line_coverage_min=parse_option_field(
                obj, Decimal, "file_line_coverage_min"
            ),
            file_branch_coverage_min=parse_option_field(
                obj, Decimal, "file_branch_coverage_min"
            ),
            modules={k: ModuleConfig.parse(v) for k, v in obj["modules"].items()}
            if "modules" in obj
            else None,
        )


@dataclass(frozen=True)
class ModuleConfig:
    file_line_coverage_min: Optional[Decimal] = None
    file_branch_coverage_min: Optional[Decimal] = None

    @staticmethod
    def parse(obj: Any) -> ModuleConfig:
        return ModuleConfig(
            file_line_coverage_min=parse_option_field(
                obj, Decimal, "file_line_coverage_min"
            ),
            file_branch_coverage_min=parse_option_field(
                obj, Decimal, "file_branch_coverage_min"
            ),
        )
