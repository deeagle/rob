#!/bin/bash

echo "Running local CI ..."

echo "Running lints ..."

echo "Lint markdown ..."
docker run --rm -v "$(pwd):/app" docdee/mdlint -c /app/.markdownlint.yml -i CHANGELOG.md "*.md"

echo "Lint shell scripts ..."
docker run --rm -v "$(pwd):/app" koalaman/shellcheck-alpine:stable find /app -type f -name '*.sh' -exec shellcheck {} +

echo "CI successfully finished."
