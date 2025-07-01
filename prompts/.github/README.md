# CI Configuration

This directory contains the GitHub Actions workflows for continuous integration.

## Workflow: CI (`ci.yml`)

This workflow runs on every push to `main`/`master` and on pull requests.

### What it does:

1. **Markdown Linting**: Validates all `.md` files for consistent formatting using `markdownlint`
2. **Link Checking**: Verifies that all links in markdown files are accessible
3. **File Structure Validation**: Ensures required files exist and basic repository structure is maintained
4. **Shell Script Validation**: Checks syntax of any `.sh` files in the repository

### Configuration Files:

- `.markdownlint.yml`: Rules for markdown formatting
- `.github/workflows/ci.yml`: The main CI workflow

### Local Testing:

To test locally before pushing:

```bash
# Install tools
npm install -g markdownlint-cli markdown-link-check

# Run markdown linting
markdownlint "**/*.md" --config .markdownlint.yml

# Check links
find . -name "*.md" -not -path "./.git/*" -exec markdown-link-check {} \;

# Check shell scripts
find . -name "*.sh" -not -path "./.git/*" | while read script; do
  bash -n "$script"
done
```

### Status Badge:

Add this to your main README.md to show CI status:

```markdown
[![CI](https://github.com/llorracc/prompts/actions/workflows/ci.yml/badge.svg)](https://github.com/llorracc/prompts/actions/workflows/ci.yml)
``` 