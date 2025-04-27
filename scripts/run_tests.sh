#!/usr/bin/env bash
echo "Running python tests via pytest..."
pytest -v --maxfail=1 --disable-warnings
echo "Coverage report:"
pip install coverage
coverage run -m pytest
coverage report --fail-under=80
