# coverage threshold

A command line tool for checking coverage reports against configurable coverage minimums.
Currently built for use around python's [coverage](https://pypi.org/project/coverage/)


### Installation
`pip install coverage-threshold`

also recommended:

`pip install coverage`

### Usage
Typical execution:
```bash
coverage run -m pytest tests/  # or any test runner here
coverage json
coverage-threshold
```

cli command options:

```
> coverage-threshold --help
usage: coverage-threshold [-h] [--line-coverage-min LINE_COVERAGE_MIN]
                          [--branch-coverage-min BRANCH_COVERAGE_MIN]
                          [--combined-coverage-min COMBINED_COVERAGE_MIN]
                          [--file-line-coverage-min FILE_LINE_COVERAGE_MIN]
                          [--file-branch-coverage-min FILE_BRANCH_COVERAGE_MIN]
                          [--file-combined-coverage-min FILE_COMBINED_COVERAGE_MIN]
                          [--coverage-json COVERAGE_JSON] [--config CONFIG]

A command line tool for checking coverage reports against configurable coverage minimums

optional arguments:
  -h, --help            show this help message and exit
  --line-coverage-min LINE_COVERAGE_MIN
                        minimum global average line coverage threshold
  --branch-coverage-min BRANCH_COVERAGE_MIN
                        minimum global average branch coverage threshold
  --combined-coverage-min COMBINED_COVERAGE_MIN
                        minimum global average combined line and branch coverage threshold
  --file-line-coverage-min FILE_LINE_COVERAGE_MIN
                        the line coverage threshold for each file
  --file-branch-coverage-min FILE_BRANCH_COVERAGE_MIN
                        the branch coverage threshold for each file
  --file-combined-coverage-min FILE_COMBINED_COVERAGE_MIN
                        the combined line and branch coverage threshold for each file
  --coverage-json COVERAGE_JSON
                        path to coverage json (default: ./coverage.json)
  --config CONFIG       path to config file (default: ./pyproject.toml)
```


### Config

the current expected config file format is [toml](https://toml.io/en/)
the default config file used is `pyproject.toml` but and alternative path can be specified with `--config`

example config:
```toml
[coverage-threshold]
line_coverage_min = 95
file_line_coverage_min = 95
branch_coverage_min = 50

    [coverage-threshold.modules."src/cli/"]
    file_line_coverage_min = 40

    [coverage-threshold.modules."src/cli/my_command.py"]
    file_line_coverage_min = 100

    [coverage-threshold.modules."src/lib/"]
    file_line_coverage_min = 100
    file_branch_coverage_min = 100

    [coverage-threshold.modules."src/model/"]
    file_line_coverage_min = 100

    [coverage-threshold.modules."src/__main__.py"]
    file_line_coverage_min = 0
```

Each string key in `config.modules` is treated as a path prefix, where the longest matching prefix is used to configure the coverage thresholds for each file
