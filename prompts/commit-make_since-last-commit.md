# Commit Message Generation Prompt - Since Last Commit

## Purpose
This prompt guides the creation of clear, consistent, and informative commit messages for changes made since the last commit.

## Setup Instructions
Before using this prompt:

1. **Identify the last commit hash:**
   ```bash
   git log --oneline -n 5
   ```

2. **Analyze changes since last commit:**
   ```bash
   git status
   git diff --stat HEAD
   git diff --name-only HEAD
   ```

3. **Review specific changes:**
   ```bash
   git diff HEAD
   ```

## Instructions
Based on the changes since the last commit, please:

1. **Generate a concise commit message** following these guidelines:
   - First line: Short summary (50 chars or less)
   - Format: `<type>: <subject>`
   - Types: feat, fix, docs, style, refactor, test, chore
   - Subject: Use imperative mood ("add" not "added")
   - No period at the end

2. **Create a detailed body message** that:
   - Explains WHAT was changed and WHY since the last commit
   - Lists specific files modified with brief descriptions
   - Describes the impact and purpose of changes
   - Groups related changes together logically
   - Separates paragraphs with blank lines
   - Uses bullet points for clarity when listing multiple items

## Common Commit Types
- **feat**: New feature or functionality
- **fix**: Bug fix or correction
- **docs**: Documentation changes
- **style**: Code formatting, whitespace, etc.
- **refactor**: Code restructuring without changing functionality
- **test**: Adding or updating tests
- **chore**: Build process, dependency updates, etc.

## Template Analysis
Fill in based on your project's actual changes:

**Current Changes Since Last Commit:**
- [FILE_NAME]: [X] lines changed (+[ADDED]/-[REMOVED]) - [DESCRIPTION]
- [FILE_NAME]: [X] lines changed (+[ADDED]/-[REMOVED]) - [DESCRIPTION]
- [Additional files as needed]

## Output Files
The generated messages should be saved to:
- Short message: `/tmp/git-commit-short-msg.txt`
- Body message: `/tmp/git-commit-body-msg.txt`

## Execution Workflow

After the commit messages are generated and saved, you can review and execute the commit by simply providing:

```
execute prompts/commit-make.sh
```

This will:
- Display the proposed commit messages
- Show current git status
- Prompt you to confirm or abort the commit
- Create a combined message file to avoid git flag conflicts
- Execute `git add .` and `git commit -F` if you choose to proceed

### Important: Git Commit Flag Fix
The script automatically creates a combined message file (`/tmp/git-commit-combined-msg.txt`) to prevent the error that occurs when trying to use both `-F` (file) and `-m` (message) flags together with `git commit`. The script uses only the `-F` flag with the combined message file for reliability.

## Example Templates

**Good short message examples:**
```
feat: add user authentication system
fix: resolve memory leak in data processor
docs: update API documentation with examples
refactor: simplify database connection logic
```

**Good body message template:**
```
[Brief overview of what was accomplished and why]

Key Changes:
- [FILE/COMPONENT]: [Description of changes]
  - [Specific detail or improvement]
  - [Another specific detail]

- [FILE/COMPONENT]: [Description of changes]
  - [Specific detail or improvement]

[Additional sections as needed:]
Technical Details:
- [Technical implementation notes]
- [Performance considerations]
- [Breaking changes if any]

Impact:
- [User-facing impact]
- [Developer experience improvements]
- [System performance changes]
```

## Usage Workflow

1. **Run git analysis commands** (see Setup Instructions)
2. **Fill in the template** with your actual file changes
3. **Generate messages** using the guidelines above
4. **Save to output files** as specified
5. **Review and refine** before committing

## Best Practices

- **Be specific**: Include actual file names and line counts
- **Explain why**: Don't just list what changed, explain the purpose
- **Group related changes**: Organize by component or feature
- **Use active voice**: "Add feature" not "Feature was added"
- **Keep scope focused**: Each commit should represent one logical change
- **Include context**: Reference issues, requirements, or decisions when relevant

## Troubleshooting

### Common Git Commit Issues

**Error: "fatal: options '-m' and '-F' cannot be used together"**
- **Cause**: Attempting to use both message flags simultaneously
- **Solution**: The updated script now automatically creates a combined message file
- **Prevention**: Always use only one message method (`-F` for file, `-m` for inline)

**Error: "No changes to commit"**  
- **Cause**: Files haven't been staged with `git add`
- **Solution**: The script automatically runs `git add .` before committing
- **Prevention**: Always check `git status` before committing

**Error: "Please enter a commit message"**
- **Cause**: Empty or missing message files
- **Solution**: Verify message files exist and contain content before running script
- **Prevention**: Always generate and verify message files first

## Next Steps
After generating and saving the messages, review them for clarity and completeness before using them to commit your changes. 