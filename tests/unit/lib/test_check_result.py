from typing import List

import pytest
from hypothesis import given
from hypothesis.strategies import characters, integers, lists

from coverage_threshold.lib.check_result import (
    CheckResult,
    Fail,
    Pass,
    combine_check_results,
    fold_check_results,
)


@given(integers(min_value=1, max_value=10))
def test_fold_check_results__all_pass(length: int) -> None:
    assert fold_check_results(Pass() for _ in range(length)) == Pass()


@given(integers(min_value=1, max_value=10))
def test_fold_check_results__all_pass_except_one(length: int) -> None:
    assert fold_check_results(
        [*(Pass() for _ in range(length)), Fail(["D'oh!"])]
    ) == Fail(["D'oh!"])


@given(lists(lists(characters(), max_size=2), min_size=1, max_size=5))
def test_fold_check_results__all_fail(values: List[str]) -> None:
    assert fold_check_results(map(lambda string: Fail([string]), values)) == Fail(
        values
    )


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (Pass(), Pass(), Pass()),
        (Pass(), Fail(["!"]), Fail(["!"])),
        (Fail(["!"]), Pass(), Fail(["!"])),
        (Fail(["one"]), Fail(["two"]), Fail(["one", "two"])),
    ],
)
def test_combine_check_results(
    a: CheckResult, b: CheckResult, expected_result: CheckResult
) -> None:
    assert combine_check_results(a, b) == expected_result
