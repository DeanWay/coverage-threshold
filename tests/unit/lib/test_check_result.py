import pytest
from hypothesis import given
from hypothesis.strategies import characters, integers, lists

from coverage_threshold.lib.check_result import (
    Fail,
    Pass,
    combine_check_results,
    fold_check_results,
)


@given(lists(integers(), min_size=1, max_size=5))
def test_fold_check_results__all_pass(values):
    assert fold_check_results(map(lambda _: Pass(), values)) == Pass()


@given(lists(integers(), min_size=0, max_size=5))
def test_fold_check_results__all_pass_except_one(values):
    assert fold_check_results(
        list(map(lambda _: Pass(), values)) + [Fail(["D'oh!"])]
    ) == Fail(["D'oh!"])


@given(lists(lists(characters(), max_size=2), min_size=1, max_size=5))
def test_fold_check_results__all_fail(values):
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
def test_combine_check_results(a, b, expected_result):
    assert combine_check_results(a, b) == expected_result
