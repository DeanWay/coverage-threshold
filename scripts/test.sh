#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

pytest tests/ src/coverage-threshold/ --doctest-modules
