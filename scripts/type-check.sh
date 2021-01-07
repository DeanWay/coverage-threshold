#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

echo "type checking source"
mypy --strict coverage_threshold/
echo "type checking tests"
mypy --strict tests/
