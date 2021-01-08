from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis.strategies import integers

from coverage_threshold.lib._common import _safe_percent, percent_branches_covered
from coverage_threshold.model.report import CoverageSummaryModel


@given(integers())
def test_safe_percent__100_percent_when_denomenator_is_zero(numerator: int) -> None:
    assert _safe_percent(numerator, 0) == Decimal(100)


@given(
    integers(min_value=0, max_value=10 ** 10), integers(min_value=1, max_value=10 ** 10)
)
def test_safe_percent__regular_fraction_otherwise(
    numerator: int, denomenator: int
) -> None:
    assert _safe_percent(numerator, denomenator) == (
        Decimal(numerator) / Decimal(denomenator) * Decimal(100)
    ).quantize(Decimal("0.0001"))


def test_percent_branches_covered__given_invalid_object() -> None:
    with pytest.raises(ValueError) as e:
        percent_branches_covered(
            CoverageSummaryModel(num_statements=1, covered_lines=1)
        )
    assert str(e.value) == "missing number of branches or number of branches covered"
