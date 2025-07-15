#!/usr/bin/env bash

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

# Get current date components
YEAR=$(date +%Y)
MONTH=$(date +%-m)  # %-m removes zero padding

# Get the latest version for current year and month
LATEST_TAG=$(git tag -l "${YEAR}.${MONTH}.*" | sort -V | tail -n 1)

if [ -z "$LATEST_TAG" ]; then
    # No version for current year/month exists, start at 0
    MICRO=0
else
    # Extract micro version and increment
    MICRO=$(echo "$LATEST_TAG" | cut -d. -f3)
    MICRO=$((MICRO + 1))
fi

NEXT_VERSION="${YEAR}.${MONTH}.${MICRO}"
CURRENT_VERSION=$(uv version --short)

echo " > Current version is $CURRENT_VERSION"
echo " > Setting new version to $NEXT_VERSION"

# Manually update version in pyproject.toml
sed -i '' "s/^version = .*/version = \"${NEXT_VERSION}\"/" pyproject.toml

echo " > Version bumped to $NEXT_VERSION"
echo "Updating CHANGELOG.md"
git-cliff --unreleased --tag "$NEXT_VERSION" --prepend CHANGELOG.md > /dev/null

echo " > Commiting changes and adding git tag"
git add pyproject.toml CHANGELOG.md uv.lock
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
