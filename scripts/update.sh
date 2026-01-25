#!/bin/bash
# update.sh — Sync updates from paperdigest template

set -e

echo "Fetching updates from upstream (paperdigest template)..."
git fetch upstream

echo "Merging updates..."
git merge upstream/main --no-edit

echo "Done! Run 'git status' to check for any conflicts."