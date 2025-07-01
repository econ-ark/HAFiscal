#!/bin/bash

# Local CI Runner - Run the same checks as GitHub Actions CI
# This script mimics the CI workflow for local testing

set -e  # Exit on any error

echo "🚀 Running CI checks locally..."
echo "================================="

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        echo "   npm install -g $1"
        exit 1
    fi
}

echo "📋 Checking required tools..."
check_tool markdownlint
check_tool markdown-link-check

echo "✅ All tools are available"
echo

# Step 1: Run markdown linting
echo "🔍 Running markdown linting..."
if markdownlint "**/*.md" --config .markdownlint.yml; then
    echo "✅ Markdown linting passed"
else
    echo "❌ Markdown linting failed"
    exit 1
fi
echo

# Step 2: Check markdown links
echo "🔗 Checking markdown links..."
link_check_failed=false
find . -name "*.md" -not -path "./.git/*" | while read file; do
    echo "  Checking links in: $file"
    if ! markdown-link-check "$file"; then
        link_check_failed=true
    fi
done

if [ "$link_check_failed" = true ]; then
    echo "❌ Link checking failed"
    exit 1
else
    echo "✅ Link checking passed"
fi
echo

# Step 3: Validate file structure
echo "📁 Validating file structure..."

# Check if README exists
if [ ! -f "README.md" ]; then
    echo "❌ ERROR: README.md is missing"
    exit 1
fi

# Check if LICENSE exists
if [ ! -f "LICENSE" ]; then
    echo "⚠️  WARNING: LICENSE file is missing"
fi

# Count markdown files
md_count=$(find . -name "*.md" -not -path "./.git/*" | wc -l)
echo "📄 Found $md_count markdown files"

if [ $md_count -eq 0 ]; then
    echo "❌ ERROR: No markdown files found"
    exit 1
fi

echo "✅ File structure validation passed"
echo

# Step 4: Check shell scripts
echo "🐚 Checking shell scripts..."
shell_scripts=$(find . -name "*.sh" -not -path "./.git/*")

if [ -z "$shell_scripts" ]; then
    echo "ℹ️  No shell scripts found"
else
    for script in $shell_scripts; do
        echo "  Checking: $script"
        if bash -n "$script"; then
            echo "    ✅ Syntax OK"
        else
            echo "    ❌ Syntax error"
            exit 1
        fi
    done
fi

echo "✅ Shell script validation passed"
echo

echo "🎉 All CI checks passed locally!"
echo "You can now push with confidence." 