#!/bin/bash

set -ef -o pipefail

function check_command {
    if ! command -v "$1" &> /dev/null; then
        echo "$1 not found. Exiting."
        exit 1
    fi
}

check_command git
check_command git-cliff
check_command uv

if [ -z "$1" ]; then
    echo " > No semver verb specified, run release with <major|minor|patch> parameter."
    exit 1
fi

CURRENT_VERSION=$(uvx poetry version -s)
echo " > Current version is $CURRENT_VERSION"

uvx poetry version "$1"
NEXT_VERSION=$(uvx poetry version -s)

echo " > jsonschema-markdown bumped to $NEXT_VERSION"
echo "Updating CHANGELOG.md"
git-cliff --unreleased --tag "$NEXT_VERSION" --prepend CHANGELOG.md > /dev/null

echo " > Commiting changes and adding git tag"
git add pyproject.toml CHANGELOG.md
git commit -m "chore(ci): Bump version to $NEXT_VERSION"
git tag -a "$NEXT_VERSION" -m "$NEXT_VERSION"

read -p " > Are you sure you want to push the changes and tags to the remote repository? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo " > Pushing changes and tags to the remote repository"
    git push
    git push --tags
else
    echo " > Changes and tags were not pushed to the remote repository"
fi
