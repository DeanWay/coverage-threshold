#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

echo "type checking source"
mypy src/coverage_threshold/
echo "type checking tests"
mypy tests/
