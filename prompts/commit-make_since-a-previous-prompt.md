# Commit Message Generation Prompt - Since Specific Prompt

## Purpose
This prompt guides the creation of clear, consistent, and informative commit messages for changes made since a specific prompt in the chat session, identified by the user.

## Setup Instructions
Before generating the commit message, please:

1. **Ask the user to identify the starting prompt** by providing:
   - A unique phrase or sentence from the prompt content
   - Example: "examine the codebase in this repo to be sure you understand what it does"
   - Example: "add a new feature to the system"
   - Example: "create a comprehensive test suite"

2. **Confirm the identified prompt** by showing:
   - The approximate message number or timestamp
   - A brief excerpt of the prompt content
   - Ask for user confirmation before proceeding

3. **Analyze all changes since that prompt** including:
   - File creations, modifications, and deletions
   - Documentation updates
   - Code restructuring or refactoring
   - Configuration changes
   - Any other modifications made

## Commit Message Guidelines

### Short Message (First Line)
- Format: `<type>: <subject>`
- Length: 50 characters or less
- Types: feat, fix, docs, style, refactor, test, chore
- Subject: Use imperative mood ("add" not "added")
- No period at the end

### Body Message (Detailed)
- Explain the complete scope of work done since the identified prompt
- List all major changes and improvements
- Group related changes into logical sections
- Separate major sections with blank lines
- Use bullet points for clarity
- Include specific file names and changes where relevant

## Analysis Framework

When analyzing changes since the identified prompt, consider:

### Code Changes
- New files created
- Files moved or renamed
- Import statement updates
- Function/class modifications
- Configuration file changes

### Documentation Changes
- README updates
- New documentation files
- Updated usage instructions
- API documentation changes

### Structural Changes
- Directory reorganization
- Package structure modifications
- Build/deployment configuration
- Dependency updates

### Quality Improvements
- Code cleanup
- Error handling improvements
- Performance optimizations
- Testing additions

## Output Requirements

Generate and save two files:
1. **Short commit message**: `/tmp/git-commit-short-msg.txt`
2. **Detailed body message**: `/tmp/git-commit-body-msg.txt`

## Execution Workflow

After the commit messages are generated and saved, you can review and execute the commit by simply providing:

```
execute prompts/commit-make.sh
```

This will:
- Display the proposed commit messages
- Show current git status
- Prompt you to confirm or abort the commit
- Execute `git add .` and `git commit` if you choose to proceed

## Example Workflow

**Step 1: User provides prompt identifier**
```
User: "Generate commit message since 'examine the codebase in this repo'"
```

**Step 2: AI confirms the prompt**
```
AI: "I found the prompt at message #15: 'examine the codebase in this repo to be sure you understand what it does, how, and why'. This was followed by [brief description of subsequent work]. Is this correct?"
```

**Step 3: AI analyzes and generates messages**
```
Short: "feat: add comprehensive reporting system"

Body: "Implemented comprehensive reporting system with multiple output formats.

Major Changes:

Core Features:
- Added report generation engine with CSV and Markdown output
- Implemented data categorization and analysis functions
- Created automated report pipeline for batch processing

Documentation:
- Updated README.md with new usage patterns and examples
- Added comprehensive API documentation
- Created user guide for report customization

Testing:
- Added test suite for all report generation functions
- Implemented data validation and error handling
- Created example datasets for testing"

- Created migration guide and completion summary

Backward Compatibility:
```

## Template Examples

### For Large Refactoring Work
```
Short: "refactor: modernize codebase architecture"

Body: "Comprehensive modernization of [PROJECT NAME] from [OLD PATTERN] to [NEW PATTERN].

[Major sections with specific changes...]
```

### For Documentation Updates  
```
Short: "docs: update documentation for new workflow"

Body: "Updated documentation to reflect [CHANGES] and improve [ASPECT].

[Specific documentation changes...]
```

### For Feature Addition
```
Short: "feat: add [FEATURE NAME]"

Body: "Implemented [FEATURE] to [PURPOSE/BENEFIT].

[Implementation details...]
```

## User Interaction Required

This prompt requires user input to:
1. Identify the starting prompt by content
2. Confirm the correct prompt was found
3. Provide any additional context about the scope or focus of changes

The AI should ask for this information before proceeding with commit message generation. 