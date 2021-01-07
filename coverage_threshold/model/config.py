from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Optional, Mapping

from .util import parse_option_field


@dataclass(frozen=True)
class Config:
    total_line_coverage_threshold: Optional[Decimal] = None
    line_coverage_threshold_for_every_file: Optional[Decimal] = None
    modules: Optional[Mapping[str, ModuleConfig]] = None

    @staticmethod
    def parse(obj: Any) -> Config:
        return Config(
            total_line_coverage_threshold=parse_option_field(
                obj, Decimal, "total_line_coverage_threshold"
            ),
            line_coverage_threshold_for_every_file=parse_option_field(
                obj, Decimal, "line_coverage_threshold_for_every_file"
            ),
            modules={k: ModuleConfig.parse(v) for k, v in obj["modules"].items()}
            if "modules" in obj
            else None,
        )


@dataclass(frozen=True)
class ModuleConfig:
    line_converage_threshold: Optional[Decimal] = None

    @staticmethod
    def parse(obj: Any) -> ModuleConfig:
        return ModuleConfig(
            line_converage_threshold=parse_option_field(
                obj, Decimal, "line_converage_threshold"
            )
        )
