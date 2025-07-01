#!/bin/bash

# Display the proposed commit messages
echo "Short Commit Message:"
cat /tmp/git-commit-short-msg.txt
echo
echo "Commit Body Message:"
cat /tmp/git-commit-body-msg.txt
echo

# Show git status
git status
echo

# Prompt for confirmation
read -p "Proceed with commit? (yes/no): " confirm
case "$confirm" in
  [Yy][Ee][Ss]|[Yy])
    git add .
    git commit --allow-empty -F /tmp/git-commit-short-msg.txt -F /tmp/git-commit-body-msg.txt
    ;;
  *)
    echo "Commit aborted."
    ;;
esac