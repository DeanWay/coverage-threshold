#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

pytest tests/ coverage_threshold/ --doctest-modules
