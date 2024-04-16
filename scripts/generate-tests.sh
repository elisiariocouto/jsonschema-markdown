#!/bin/bash

set -euo pipefail

TEST_DIR="$(dirname "$0")/../tests/schema-examples"

# Generate markdown files for each test case
for file in "$TEST_DIR"/*.json; do
    echo "Generating markdown for $file"
    jsonschema-markdown "$file" > "${file%.json}.md"
    echo "Generating markdown for $file with no empty columns"
    jsonschema-markdown --no-empty-columns "$file" > "${file%.json}_no-empty-columns.md"
done

# Generate markdown file for Python example
echo "Generating markdown for Python example"
python3 "$TEST_DIR"/../model.py | jsonschema-markdown - > "$TEST_DIR/../model.md"

echo "Generating markdown for Python example with custom title and no footer"
python3 "$TEST_DIR"/../model.py | jsonschema-markdown --title "Car (custom title)" --no-footer - > "$TEST_DIR/../model_custom-title_no-footer.md"

echo "Generating markdown for Python example with no empty columns"
python3 "$TEST_DIR"/../model.py | jsonschema-markdown --no-empty-columns - > "$TEST_DIR/../model_no-empty-columns.md"
