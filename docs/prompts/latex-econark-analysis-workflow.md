# EconARK Repository Analysis Workflow

**Complete step-by-step guide for analyzing new EconARK LaTeX repositories**

## Overview

This workflow provides a systematic approach to analyze, fix, and document any EconARK LaTeX repository. The tools are designed to work with the EconARK architecture and can be applied to any repository in the ecosystem.

## Prerequisites

- LaTeX installation with pdflatex
- Bash shell environment
- Access to the repository's EconARK package structure

## Step-by-Step Workflow

### Phase 1: Architecture Understanding

**Step 1: Understand the Repository Architecture**

In an AI chat context, ask the AI to:
```
Follow the instructions in prompts/econark-repo-architecture.md
```

This helps you understand the EconARK self-contained system before making any changes.

**Step 2: Verify Repository Structure**
```bash
# Copy and run the architecture verification
cp prompts/econark-repo-architecture_verify.sh tests/
chmod +x tests/econark-repo-architecture_verify.sh
./tests/econark-repo-architecture_verify.sh
```

**Expected Output:** All tests should pass (✅) indicating proper EconARK architecture.

### Phase 2: Compilation and Fixes

**Step 3: Initial Compilation Attempt**
```bash
# Try to compile the main document
pdflatex -interaction=nonstopmode [MAIN_DOCUMENT].tex
```

**Step 4: Apply LaTeX Fixes (if needed)**

If compilation fails, in an AI chat context, ask the AI to:
```
Follow the systematic fixing guide in prompts/latex-fixes-to-prepare-for-git.md
```

**CRITICAL: Most common issue is redundant package loading**
- Check if `econark.sty` is loaded multiple times (by handoutShortcuts AND document-specific .sty)
- Remove redundant `\usepackage{\econark}` from document-specific files
- NEVER modify shared packages in texmf-local directories

**Other common fixes include:**
- Comment out incompatible packages (e.g., sectsty with KOMA-Script)
- Fix hyperref PDF string issues
- Improve float placement

**Step 5: Verify Successful Compilation**
```bash
# Ensure clean compilation
pdflatex -interaction=nonstopmode [MAIN_DOCUMENT].tex
echo "Exit code: $?"  # Should be 0
```

### Phase 3: Macro Analysis and Documentation

**Step 6: Analyze Macro Definitions**
```bash
# Copy and run the macro analysis tool
cp prompts/generate-macro-report.sh tests/
chmod +x tests/generate-macro-report.sh

# Edit the script to use your document name
sed -i 's/Portfolio-CRRA/[YOUR_DOCUMENT_NAME]/g' tests/generate-macro-report.sh

# Run the analysis
./tests/generate-macro-report.sh
```

**Output:** Creates `[DOCUMENT_NAME]_macros-report.md` with two tables:
- Table 1: Redefined macros (should be empty for good compatibility)
- Table 2: Project-specific macros (document extensions)

**Step 7: Review Comprehensive Analysis**

The macro analysis tool now includes both static analysis (regex) and dynamic analysis (LaTeX debugging) for comprehensive verification. Review the generated report for:
- Compilation warnings from LaTeX
- Verification status for each command
- Cross-validation between analysis methods

### Phase 4: Quality Assurance

**Step 8: Review Analysis Results**

Check the macro analysis report:
- **Zero redefinitions** = ✅ Perfect EconARK compatibility
- **Non-zero redefinitions** = ⚠️ Review and minimize
- **Project-specific macros** = ℹ️ Document extensions (acceptable)

**Step 9: Final Compilation Test**
```bash
# Clean build to ensure everything works
rm -f [DOCUMENT_NAME].aux [DOCUMENT_NAME].out [DOCUMENT_NAME].log
pdflatex -interaction=nonstopmode [DOCUMENT_NAME].tex
```

**Step 10: Documentation and Cleanup**
```bash
# Clean up compilation artifacts
latexmk -c

# Remove temporary analysis files
rm -f debug-redefinitions.* *_macros-report.md

# Update .gitignore if needed (analysis artifacts should be regenerated)
echo "# Analysis artifacts (should be regenerated)" >> .gitignore
echo "*_macros-report.md" >> .gitignore
echo "debug-redefinitions.*" >> .gitignore
```

## Tool Reference

### Available Tools in `prompts/`

1. **`econark-repo-architecture.md`** - Understanding guide
2. **`latex-fixes-to-prepare-for-git.md`** - Systematic fixing guide  
3. **`econark-repo-architecture_verify.sh`** - Architecture verification
4. **`generate-macro-report.sh`** - Comprehensive macro analysis (static + dynamic)

### Tool Customization

Before running tools on a new repository:

```bash
# Create tests directory and copy tools
mkdir -p tests
cp prompts/*.sh tests/
chmod +x tests/*.sh

# Update document name in scripts
DOCUMENT_NAME="YourDocument"
sed -i "s/Portfolio-CRRA/$DOCUMENT_NAME/g" tests/*.sh
```

## Expected Outcomes

### ✅ Successful Analysis
- Clean compilation (exit code 0)
- Zero redefinitions in macro report
- All architecture verification tests pass
- Professional documentation generated

### ⚠️ Issues Found
- **Compilation errors**: Follow `latex-fixes-to-prepare-for-git.md`
- **Redefinitions detected**: Review and minimize conflicts
- **Architecture problems**: Verify EconARK package structure

### 📊 Generated Reports
- `[DOCUMENT]_macros-report.md` - Comprehensive macro analysis
- `redefinition-report.md` - Alternative debugging report
- Clean PDF output with proper compilation

## Best Practices

1. **Always start with architecture understanding** - Don't modify the EconARK system
2. **Use `\providecommand` over `\newcommand`** - Prevents redefinition conflicts
3. **Document project-specific macros** - Keep clear records of extensions
4. **Verify architecture** - Ensure the repository remains self-contained
5. **Minimize redefinitions** - Maintain EconARK ecosystem compatibility

## Troubleshooting

### Common Issues

**"Command already defined" errors:**
- Use `\providecommand` instead of `\newcommand`
- Check for duplicate definitions across files

**Package conflicts:**
- Comment out incompatible packages
- Use KOMA-Script compatible alternatives

**Path resolution failures:**
- Verify `.econtexRoot.tex` exists
- Check `Resources/.econtexPaths.tex` structure

**Macro analysis shows many redefinitions:**
- Review if these are actual conflicts
- Consider renaming document-specific commands

## Quick Reference Commands

```bash
# Full workflow for new repository
mkdir -p tests
cp prompts/*.sh tests/ && chmod +x tests/*.sh
./tests/econark-repo-architecture_verify.sh
pdflatex -interaction=nonstopmode [DOCUMENT].tex
./tests/generate-macro-report.sh
latexmk -c  # Clean up artifacts
```

This workflow ensures systematic analysis while maintaining EconARK ecosystem compatibility. 