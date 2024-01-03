#!/bin/bash

set -e
set +x

echo "Running local CI ..."

echo "Running lints ..."

echo "Lint markdown ..."
docker run --rm -v "$(pwd):/app" docdee/mdlint -c /app/.markdownlint.yml -i CHANGELOG.md "**/*.md"

echo "Lint shell scripts ..."
docker run --rm -v "$(pwd):/app" koalaman/shellcheck-alpine:stable find /app -type f -name '*.sh' -exec shellcheck {} +

echo "Lint code (flake8) ..."
echo "> we want O's"
# stop the build if there are Python syntax errors or undefined names
docker run --rm -v "$(pwd):/app" pipelinecomponents/flake8 flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
# exit-zero treats all errors as warnings.
docker run --rm -v "$(pwd):/app" pipelinecomponents/flake8 flake8 . --count --max-complexity=10 --max-line-length=120 --statistics

echo "CI successfully finished."
