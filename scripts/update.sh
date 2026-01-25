#!/bin/bash
# update.sh — Sync updates from paperdigest template
# Usage: ./scripts/update.sh [--check]
#   --check  Only check if updates are available (no merge)

set -e

echo "Pulling latest from origin..."
git pull --rebase origin main

echo "Fetching updates from upstream (paperdigest template)..."
git fetch upstream

# Count commits behind upstream
BEHIND=$(git rev-list --count HEAD..upstream/main)

if [ "$BEHIND" -eq 0 ]; then
    echo "✅ Already up to date with upstream."
    exit 0
fi

echo "📦 $BEHIND commit(s) behind upstream."

# Check-only mode
if [ "$1" = "--check" ]; then
    echo ""
    echo "Run './scripts/update.sh' (without --check) to sync."
    exit 0
fi

echo "Merging updates..."
git merge upstream/main --no-edit

echo "Pushing to origin..."
git push

echo "✅ Done!"