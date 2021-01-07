from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, List, Mapping, Optional

from .util import parse_option_field

# replace these dataclass models with pydantic
# if this gets too complex


@dataclass(frozen=True)
class CoverageSummaryModel:
    covered_lines: int
    num_statements: int
    num_branches: Optional[int] = None
    covered_branches: Optional[int] = None

    @staticmethod
    def parse(obj: Any) -> CoverageSummaryModel:
        return CoverageSummaryModel(
            covered_lines=int(obj["covered_lines"]),
            num_statements=int(obj["num_statements"]),
            num_branches=parse_option_field(obj, int, "num_branches"),
            covered_branches=parse_option_field(obj, int, "covered_branches"),
        )


@dataclass(frozen=True)
class FileCoverageModel:
    summary: CoverageSummaryModel

    @staticmethod
    def parse(obj: Any) -> FileCoverageModel:
        return FileCoverageModel(summary=CoverageSummaryModel.parse(obj["summary"]))


@dataclass(frozen=True)
class ReportMetadata:
    branch_coverage: bool

    @staticmethod
    def parse(obj: Any) -> ReportMetadata:
        return ReportMetadata(branch_coverage=bool(obj["branch_coverage"]))


@dataclass(frozen=True)
class ReportModel:
    files: Mapping[str, FileCoverageModel]
    totals: CoverageSummaryModel
    meta: ReportMetadata

    @staticmethod
    def parse(obj: Any) -> ReportModel:
        return ReportModel(
            files={
                filename: FileCoverageModel.parse(value)
                for filename, value in obj["files"].items()
            },
            totals=CoverageSummaryModel.parse(obj["totals"]),
            meta=ReportMetadata.parse(obj["meta"]),
        )
