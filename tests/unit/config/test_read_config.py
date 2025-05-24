import os
from decimal import Decimal

from coverage_threshold.cli.read_config import read_config


def test_read_config_parses_default_pyproject_format() -> None:
    config = read_config(path_to_test_config("pyproject.toml"))
    assert config.line_coverage_min == Decimal("75.0")
    assert config.modules is None


# backwards compatibilty for before this project became compliant with pep518
def test_read_config_parses_legacy_pyproject_format() -> None:
    config = read_config(path_to_test_config("legacy.pyproject.toml"))
    assert config.line_coverage_min == Decimal("75.0")
    assert config.modules is None


def test_read_config_parses_complex_pyproject_format() -> None:
    config = read_config(path_to_test_config("complex.pyproject.toml"))
    assert config.line_coverage_min == Decimal("95.0")
    assert config.file_line_coverage_min == Decimal("95.0")
    assert config.branch_coverage_min == Decimal("50.0")
    assert config.modules is not None
    assert config.modules["src/cli/"].file_line_coverage_min == Decimal("40.0")
    assert config.modules["src/cli/my_command.py"].file_line_coverage_min == Decimal(
        "100"
    )
    assert config.modules["src/lib/"].file_line_coverage_min == Decimal("100")
    assert config.modules["src/lib/"].file_branch_coverage_min == Decimal("100")
    assert config.modules["src/model/"].file_line_coverage_min == Decimal("100")
    assert config.modules["src/__main__.py"].file_line_coverage_min == Decimal("0")


def path_to_test_config(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)
