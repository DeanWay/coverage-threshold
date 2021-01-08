from decimal import Decimal

import pytest

from coverage_threshold.model.config import Config, ModuleConfig


def test_config_parse__empty():
    assert Config.parse({}) == Config()


def test_config_parse__ignores_extra_fields():
    assert Config.parse({"lol": 123}) == Config()


@pytest.mark.parametrize(
    "field_name",
    [
        "line_coverage_min",
        "branch_coverage_min",
        "file_line_coverage_min",
        "file_branch_coverage_min",
    ],
)
def test_config_parse__optional_decimals(field_name):
    assert Config.parse({field_name: 123}) == Config(**{field_name: Decimal("123")})
    assert Config.parse({field_name: None}) == Config()


def test_config_parse__modules_emtpy():
    assert Config.parse({"modules": {"src/lib/": {}}}) == Config(
        modules={"src/lib/": ModuleConfig()}
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "file_line_coverage_min",
        "file_branch_coverage_min",
    ],
)
def test_config_parse__modules_optional_decimals(field_name):
    assert Config.parse({"modules": {"src/lib/": {field_name: 123}}}) == Config(
        modules={"src/lib/": ModuleConfig(**{field_name: Decimal("123")})}
    )
