#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

coverage run --branch -m pytest tests/ src/coverage_threshold/ --doctest-modules
coverage report -m
coverage json
coverage-threshold
