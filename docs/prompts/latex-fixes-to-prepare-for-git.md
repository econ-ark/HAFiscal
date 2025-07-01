# AI-Friendly LaTeX Compilation Fixes: Macro Redefinitions and Warnings

**PROMPT**: You are helping fix LaTeX compilation warnings and errors. Follow this systematic approach to ensure clean compilation and portability across different machines.

## STEP 0: UNDERSTAND THE REPOSITORY ARCHITECTURE

**IMPORTANT**: Before making any changes, read `prompts/econark-repo-architecture.md` to understand how EconARK repositories work. The self-contained relative path system is a FEATURE, not a bug.

**Run these commands to verify the self-contained architecture:**

1. **Verify the EconARK architecture is present**:
   ```bash
   # Check for the root definition file
   ls -la .econtexRoot.tex
   
   # Find the resources directory (could be Resources/, @resources/, @local/, etc.)
   find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d
   
   # Check for centralized path definitions in the found directory
   RESOURCE_DIR=$(find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d | head -1)
   ls -la $RESOURCE_DIR/.econtexPaths.tex
   ```

2. **Confirm all dependencies are bundled**:
   ```bash
   # List all .sty files in project (should be comprehensive)
   find . -name "*.sty" -type f
   
   # Check if all are tracked in git
   git ls-files | grep "\.sty$"
   ```

3. **Verify variable-based package loading works correctly**:
   ```bash
   # Find variable-based packages (this is GOOD in EconARK repos)
   grep "\\usepackage{\\\\.*}" *.tex
   
   # For each variable found, verify it's defined in .econtexPaths.tex
   RESOURCE_DIR=$(find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d | head -1)
   grep -r "providecommand.*handoutShortcuts" $RESOURCE_DIR/.econtexPaths.tex
   ```

4. **Test self-containment**:
   ```bash
   # Test if LaTeX can find all packages (dry run)
   pdflatex -draftmode -interaction=nonstopmode document.tex
   
   # Check for "file not found" errors (should be none)
   grep -i "file.*not found\|cannot find\|No file" document.log
   ```

**CRITICAL**: In EconARK repositories, `\usepackage{\variableName}` patterns are GOOD - they indicate proper use of the self-contained architecture.

## STEP 1: DIAGNOSE COMPILATION ISSUES

1. **Compile the document**:
   ```bash
   pdflatex -interaction=nonstopmode document.tex
   ```

2. **Find all warnings/errors**:
   ```bash
   grep -i "warning\|error\|redefin\|already defined" document.log
   ```

3. **CRITICAL: Check for redundant package loading**:
   ```bash
   # Find which packages are loaded multiple times
   grep -r "\\usepackage.*econark" . --include="*.tex" --include="*.sty"
   grep -r "\\usepackage.*handout" . --include="*.tex" --include="*.sty"
   ```

4. **Locate macro definitions (document-specific files only)**:
   ```bash
   grep -r "\\newcommand\|\\newcolumntype" . --include="*.tex" --exclude-dir="texmf-local"
   grep -r "\\newcommand\|\\newcolumntype" Resources/LaTeXInputs/ --include="*.sty"
   ```

5. **Check package compatibility issues**:
   ```bash
   grep -i "incompatible\|obsolete" document.log
   ```

## STEP 2: APPLY FIXES (in order of priority)

### Fix A: Handle Command Redefinition Issues
- **CRITICAL**: NEVER modify shared packages in texmf-local directories
- **Target**: Document-specific files (.tex) and document-specific style files ONLY
- **Common Cause**: Redundant package loading (e.g., econark loaded by both handoutShortcuts and document-specific .sty)
- **Solution**: Remove redundant `\usepackage` statements from document-specific files
- **Alternative**: Change `\newcommand` to `\providecommand` in document-specific files only
- **Reason**: Shared packages represent the EconARK ecosystem and must remain unchanged

### Fix B: Remove duplicate definitions
- **Target**: Local style files that duplicate global definitions
- **Change**: Comment out duplicates with explanation
- **Example**: `% \newcolumntype{d}[1]{D{.}{.}{#1}} % Already defined in handoutSetup.sty`

### Fix C: Handle package compatibility issues
- **KOMA-Script conflicts**: Comment out incompatible packages like `sectsty`
- **Example**: `% \usepackage{sectsty} % Commented out - incompatible with KOMA-Script and not used`
- **Font packages**: Check for conflicts between font-related packages

### Fix D: Suppress cosmetic warnings with silence package
- **Add to style file**:
```latex
\usepackage{silence}
\WarningFilter{pdfTeX}{destination with the same identifier}
\WarningFilter{LaTeX Font Warning}{Font shape `U/wasy/b/n'}
\WarningFilter{Package hyperref Warning}{Token not allowed in a PDF string}
\WarningFilter{LaTeX Warning}{Unused global option(s)}
```

### Fix E: Fix hyperref PDF string issues
- **Problem**: Math commands in section titles cause hyperref warnings
- **Solution**: Provide plain text version for PDF bookmarks
- **Example**: `\section[Plain Text]{Math \cite{ref} Title}` 

### Fix F: Improve float placement
- **Problem**: `h` float specifier warnings
- **Solution**: Use better placement options
- **Change**: `\begin{figure}[h]` → `\begin{figure}[htbp]`

### Fix G: Handle font shape warnings
- **Problem**: Missing bold variants of symbol fonts (wasy, etc.)
- **Solutions**:
  1. Suppress with silence package (recommended for cosmetic issues)
  2. Or declare font substitutions (if needed):
```latex
\AtBeginDocument{%
  \DeclareFontShape{U}{wasy}{b}{n}{<->ssub*wasy/m/n}{}%
  \DeclareFontShape{U}{wasy}{bx}{n}{<->ssub*wasy/m/n}{}%
}
```

### Fix H: Verify self-contained architecture integrity
- **Purpose**: Ensure the EconARK repository architecture is working correctly
- **Check**: Variable-based package loading should work seamlessly
- **Actions**:
  1. **Verify all referenced files exist**:
     ```bash
     # Check that all \usepackage{\variableName} resolve to existing files
     grep "\\usepackage{\\\\.*}" *.tex
     # For each variable, confirm the file exists
     find Resources/texmf-local -name "*.sty"
     ```
  2. **Ensure git tracking**:
     ```bash
     # All .sty files should be tracked
     git ls-files | grep "\.sty$"
     ```
  3. **Test compilation in clean environment** (if possible)

**Note**: The resources directory may have different names across projects:
- `Resources/` (standard)
- `@resources/` (alternative naming)  
- `@local/` (local resources)
- Other project-specific directory names

Always use the discovery commands above to find the actual directory name before proceeding.

## STEP 3: VERIFY FIXES

1. **Recompile**: `pdflatex -interaction=nonstopmode document.tex`
2. **Check exit code**: Should be 0 for success
3. **Verify warnings eliminated**: `grep -i "warning\|error" document.log`
4. **Confirm successful compilation and unchanged output quality**

## CRITICAL RULES FOR AI ASSISTANTS:
- ✅ **DO change**: Main .tex files, document-specific .sty files in LaTeXInputs/
- ❌ **NEVER change**: Files in texmf-local/ directories (shared EconARK packages)
- ❌ **NEVER change**: econark.sty, handoutSetup.sty, handoutShortcuts.sty, etc.
- ✅ **First check**: Is the issue caused by redundant package loading?
- ✅ **Always test compilation** after each change
- ✅ **Use warning suppression** for cosmetic issues that don't affect output
- ✅ **Backup files** before making changes

## COMMON PATTERNS AND SOLUTIONS:

### Pattern 1: Redundant package loading (MOST COMMON)
```latex
# In document-specific .sty file - BEFORE
\usepackage{\econark}  % Already loaded by handoutShortcuts!

# AFTER
% \usepackage{\econark} % Already loaded by handoutShortcuts.sty
```

### Pattern 2: Command redefinitions in document-specific files
```latex
# In document-specific files only - BEFORE
\newcommand{\scale}{x}
\newcommand{\riskyshk}{\varepsilon}

# AFTER  
\providecommand{\scale}{x}
\providecommand{\riskyshk}{\varepsilon}
```

### Pattern 2: Column type duplicates
```latex
# Before
\newcolumntype{d}[1]{D{.}{.}{#1}}

# After
% \newcolumntype{d}[1]{D{.}{.}{#1}} % Already defined in handoutSetup.sty
```

### Pattern 3: Package conflicts
```latex
# Before
\usepackage{sectsty}  # Causes KOMA-Script warnings

# After
% \usepackage{sectsty} % Commented out - incompatible with KOMA-Script and not used
```

### Pattern 4: Hyperref section titles
```latex
# Before
\section{The \cite{cvAppendix} Approximation}

# After
\section[The Carroll and Viceira Approximation]{The \cite{cvAppendix} Approximation}
```

### Pattern 5: Float placement
```latex
# Before
\begin{figure}[h]

# After
\begin{figure}[htbp]
```

## WARNING CATEGORIES:

### Critical (Must Fix):
- Command redefinition errors
- Package loading errors  
- Missing files that should be in the repository
- Broken self-contained architecture (files not tracked in git)

### Important (Should Fix):
- Package compatibility warnings
- Hyperref PDF string issues
- Float placement warnings

### Cosmetic (Can Suppress):
- Font shape warnings (missing bold variants)
- Duplicate PDF destinations (in dual-structure documents)
- Unused global options

## AUTOMATION SCRIPT TEMPLATE

```bash
#!/bin/bash
# AI-friendly script to fix common LaTeX issues

echo "=== STEP 0: DEPENDENCY ANALYSIS ==="
echo "Finding resources directory..."
RESOURCE_DIR=$(find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d | head -1)
echo "Resources directory: $RESOURCE_DIR"

echo "Checking for variable-based package loading..."
grep "\\usepackage{\\\\.*}" *.tex && echo "✅ Variable-based loading detected (GOOD in EconARK repos)"

echo "=== STEP 1: DIAGNOSE ==="
pdflatex -interaction=nonstopmode "$1.tex"
grep -i "already defined\|redefin" "$1.log"

echo "=== STEP 2: APPLY FIXES ==="
# Replace newcommand with providecommand in main document
sed -i.bak 's/\\newcommand{/\\providecommand{/g' *.tex

echo "=== STEP 3: VERIFY ==="
pdflatex -interaction=nonstopmode "$1.tex"
echo "Exit code: $?"
grep -i "warning\|error" "$1.log" | wc -l
```

## EXPECTED RESULT

After applying these fixes:
- ✅ **Clean compilation** with exit code 0
- ✅ **Eliminated critical warnings** and suppressed cosmetic warnings  
- ✅ **Identical document output** quality
- ✅ **Improved portability** across different machines
- ✅ **Future compilations** are cleaner and more reliable

## TROUBLESHOOTING

### Command Already Defined Errors
**FIRST CHECK**: Redundant package loading
```bash
# Check if econark is loaded multiple times
grep -r "\\usepackage.*econark" . --include="*.tex" --include="*.sty"
# If found in both handoutShortcuts.sty AND document-specific .sty:
# Remove from document-specific .sty file
```

### If issues persist:
1. **Check for typos** in command names
2. **Verify all required packages** are loaded
3. **Look for circular dependencies** between style files
4. **Consider using `\AtBeginDocument{}`** for late-loading definitions
5. **Use `\makeatletter` and `\makeatother`** for internal command redefinitions

### NEVER DO:
- ❌ Modify econark.sty, handoutSetup.sty, handoutShortcuts.sty
- ❌ Change any files in texmf-local/ directories
- ❌ Assume shared packages need fixing

---

**Note for AI Assistants**: Always backup files before making changes and test thoroughly. These fixes address symptoms of poor macro management but the root cause is often architectural - consider suggesting refactoring macro definitions for long-term maintainability. 