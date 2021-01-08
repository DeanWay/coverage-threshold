import subprocess
from typing import Final

from coverage_threshold.cli import colors

EXAMPLE_PROJECT_PATH = "./example_project"
SUCCESS_MESSAGE = f"{colors.OKGREEN}Success!{colors.ENDC}\n"


def test_cli_runs_successfully_on_example_project() -> None:
    subprocess.run(
        ["coverage", "run", "-m", "pytest", "tests/"],
        cwd=EXAMPLE_PROJECT_PATH,
    )
    subprocess.run(["coverage", "json"], cwd=EXAMPLE_PROJECT_PATH)
    process = subprocess.run(
        ["coverage-threshold"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=EXAMPLE_PROJECT_PATH,
    )
    assert process.returncode == 0
    assert process.stderr == b""
    assert process.stdout == SUCCESS_MESSAGE.encode("utf-8")


def test_cli_fails() -> None:
    subprocess.run(
        ["coverage", "run", "-m", "pytest", "tests/"],
        cwd=EXAMPLE_PROJECT_PATH,
    )
    subprocess.run(["coverage", "json"], cwd=EXAMPLE_PROJECT_PATH)
    process = subprocess.run(
        ["coverage-threshold", "--line-coverage-min", "100.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=EXAMPLE_PROJECT_PATH,
    )
    assert process.returncode == 1
    assert process.stderr == b""
    assert process.stdout == (
        "Failed with 1 errors\n"
        + f"{colors.FAIL}Total line coverage metric failed, expected: 100.0, was 75.0000{colors.ENDC}\n"
    ).encode("utf-8")
