#!/usr/bin/env bash
# run on localhost before commit, you can add it into git hook

set -o errexit
set -o nounset
set -x  # we want to print commands

# sort import statements automatically
isort

# run linters
black --target-version=py37 billing*

# run linters
flake8

# run mypy (static type checker for Python)
mypy billing*

# run tests
pytest
