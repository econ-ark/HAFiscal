# EconARK Repository Architecture: Understanding Self-Contained LaTeX Projects

**PROMPT**: You are working with EconARK-style LaTeX repositories that use a sophisticated self-contained architecture. Understanding this system is CRITICAL to avoid breaking the portability features while fixing compilation issues.

## CORE ARCHITECTURE PRINCIPLE

**These repositories are designed to be FULLY PORTABLE and SELF-CONTAINED.** Every file needed for compilation is included in the repo and accessed via a relative path system.

## HOW THE RELATIVE PATH SYSTEM WORKS

### Step 1: Root Definition
Every main LaTeX file starts with:
```latex
\input{./.econtexRoot}
```

This file contains:
```latex
\providecommand{\econtexRoot}{}\renewcommand{\econtexRoot}{.}
\providecommand{\econtexPaths}{}\renewcommand{\econtexPaths}{\econtexRoot/Resources/.econtexPaths}
\input{\econtexPaths}
```

### Step 2: Path Resolution Chain
```
\input{./.econtexRoot}
    ↓ defines \econtexRoot as "." (current directory)
    ↓ defines \econtexPaths as "\econtexRoot/{PathToResources}/.econtexPaths"
    ↓ inputs ./{PathToResources}/.econtexPaths.tex

./{PathToResources}/.econtexPaths.tex contains:
    ↓ \providecommand{\handoutShortcuts}{\econtexRoot/{PathToResources}/texmf-local/tex/latex/handoutShortcuts}
    ↓ \providecommand{\handoutSetup}{\econtexRoot/{PathToResources}/texmf-local/tex/latex/handoutSetup}
    ↓ [many other path definitions]

Main document uses:
    ↓ \usepackage{\handoutShortcuts}
    ↓ resolves to: \usepackage{./{PathToResources}/texmf-local/tex/latex/handoutShortcuts}
    ↓ loads: ./{PathToResources}/texmf-local/tex/latex/handoutShortcuts.sty
```

**Common path variations**:
- `Resources/` (standard)
- `@resources/` (alternative naming)
- `@local/` (local resources)
- Other project-specific directory names

### Step 3: File Guarantee
Since `\econtexRoot` = "." and all paths are relative, **every referenced file exists in the repo** and will be found on any machine.

## CRITICAL UNDERSTANDING FOR AI ASSISTANTS

### ✅ THESE PATTERNS ARE GOOD (Features, not bugs):
- `\usepackage{\handoutShortcuts}` - **Self-contained package loading**
- `\input{\econtexPaths}` - **Centralized path management**
- `\econtexRoot/{PathToResources}/...` paths - **Guaranteed relative paths**
- Multiple `.sty` files in `{PathToResources}/texmf-local/` - **Bundled dependencies**
- Path variations like `@resources/`, `@local/`, etc. - **Project-specific organization**

### ❌ DO NOT "FIX" THESE:
- Variable-based package loading (`\usepackage{\variableName}`)
- Relative path definitions in `.econtexPaths.tex`
- The `\econtexRoot` system
- Local texmf directory structure

### ✅ DO FIX THESE:
- Macro redefinition warnings (`\newcommand` → `\providecommand`)
- Package compatibility issues
- Font warnings and cosmetic issues
- Missing files that should be in the repo

## REPOSITORY STRUCTURE PATTERN

```
Repository-Name/
├── .econtexRoot.tex              # Defines root as "."
├── MainDocument.tex              # Uses \input{./.econtexRoot}
├── body.tex                      # Generated content
├── {PathToResources}/            # Could be Resources/, @resources/, @local/, etc.
│   ├── .econtexPaths.tex         # Central path definitions
│   ├── LaTeXInputs/
│   │   └── MainDocument.sty      # Document-specific styles
│   └── texmf-local/
│       └── tex/latex/
│           ├── handoutSetup.sty   # Shared utilities
│           ├── handoutShortcuts.sty
│           ├── econark.sty        # Core EconARK package
│           └── [other .sty files]
├── Figures/                      # Document figures
├── Tables/                       # Document tables
└── [other content directories]
```

**Common resource directory names**:
- `Resources/` - Standard EconARK convention
- `@resources/` - Alternative naming convention
- `@local/` - Local resources directory
- `LaTeX/` - LaTeX-specific resources
- Other project-specific names

## VERIFICATION COMMANDS

To verify the self-contained architecture works:

```bash
# 1. Check that .econtexRoot exists and defines paths correctly
cat .econtexRoot.tex

# 2. Find the resources directory (could be Resources/, @resources/, @local/, etc.)
find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d

# 3. Verify all path definitions resolve to existing files
# (Replace {PathToResources} with actual directory found above)
grep "providecommand.*tex/latex" {PathToResources}/.econtexPaths.tex

# 4. Confirm all referenced .sty files exist in the repo
find . -name "*.sty" -type f

# 5. Verify all .sty files are tracked in git
git ls-files | grep "\.sty$"

# 6. Test that variable-based packages resolve correctly
grep "\\usepackage{\\\\.*}" *.tex
# For each \variableName found, check:
grep "providecommand.*variableName" {PathToResources}/.econtexPaths.tex
```

## REAL COMPILATION TESTING

**CRITICAL**: File existence checks are insufficient. You MUST test actual LaTeX compilation to verify the architecture works correctly, as `kpsewhich` behavior and package dependencies can only be verified through real compilation.

### Create a Proper Test Document

**IMPORTANT**: The test document must follow the exact same pattern as working EconARK documents to avoid false failures.

Create `test-econark-architecture.tex`:

```latex
\input{./.econtexRoot}\documentclass{\handout}
\usepackage{\handoutSetup}\usepackage{\handoutShortcuts}
\usepackage{\LaTeXInputs/YourDocument}

\begin{document}

\title{EconARK Architecture Verification Test}
\author{Portability Test}
\date{\today}
\maketitle

\section{Package Loading Verification}

This document tests whether all EconARK packages load correctly using the same pattern as working documents.

\subsection{Testing Package-Provided Commands}
Testing if package commands are defined:
\begin{itemize}
\item \texttt{cnstr} command: \ifdefined\cnstr defined\else NOT DEFINED\fi
\item \texttt{BalGroFac} command: \ifdefined\BalGroFac defined\else NOT DEFINED\fi
\item \texttt{PopnGroFac} command: \ifdefined\PopnGroFac defined\else NOT DEFINED\fi
\item \texttt{TargetNrm} command: \ifdefined\TargetNrm defined\else NOT DEFINED\fi
\end{itemize}

\subsection{Testing Math Commands}
If packages loaded correctly, these should render properly:
\begin{itemize}
\item Constraint: $\cnstr{c}$ (should show formatted constraint)  
\item Balance growth factor: $\BalGroFac$ (should show math symbol)
\item Population growth factor: $\PopnGroFac$ (should show math symbol)
\end{itemize}

\subsection{Architecture Test Results}

\textbf{SUCCESS CRITERIA:}
\begin{itemize}
\item Document compiles without fatal errors
\item Package commands show "defined" 
\item Math symbols render as symbols, not literal text
\item No LaTeX commands appear as literal text in output
\end{itemize}

\textbf{This test follows the exact same package loading pattern as working EconARK documents:}
\begin{itemize}
\item Uses \texttt{\textbackslash documentclass\{\textbackslash handout\}} 
\item Loads \texttt{\textbackslash handoutSetup} first
\item Then loads \texttt{\textbackslash handoutShortcuts}
\item Finally loads document-specific style file
\end{itemize}

\textbf{NOTE}: Document-specific commands like \texttt{\textbackslash scale} and \texttt{\textbackslash riskyshk} are defined in individual documents, not packages, so they won't appear as "defined" in this test.

\end{document}
```

### Run the Compilation Test

```bash
# Compile the test document
pdflatex -interaction=nonstopmode test-econark-architecture.tex

# Check compilation success
echo "Exit code: $?"

# Extract text from PDF to verify proper rendering
pdftotext test-econark-architecture.pdf test-econark-architecture.txt

# Check for critical failure indicators
echo "=== CHECKING FOR LITERAL LATEX COMMANDS (CRITICAL FAILURE) ==="
grep -E "(provideboolean|setboolean|definecolor|newcolumntype)" test-econark-architecture.txt || echo "✅ No literal LaTeX commands found"

echo "=== CHECKING PACKAGE COMMAND DEFINITIONS ==="
grep -E "(NOT DEFINED|defined)" test-econark-architecture.txt

echo "=== CHECKING FOR COMPILATION ERRORS ==="
grep -i "error\|fatal\|emergency" test-econark-architecture.log | head -5
```

### Interpreting Test Results

**✅ ARCHITECTURE WORKING CORRECTLY:**
- PDF compiles successfully (exit code 0 or 1 with PDF generated)
- Package commands show "defined" (cnstr, BalGroFac, PopnGroFac, TargetNrm)
- Math symbols render properly as symbols
- No literal LaTeX commands in PDF text
- Clean compilation with only minor warnings

**❌ CRITICAL ARCHITECTURE FAILURE:**
- LaTeX commands appear as literal text in PDF (indicates wrong document class or missing base packages)
- Fatal compilation errors preventing PDF generation
- Most package commands show "NOT DEFINED"

**⚠️ COMMON TESTING MISTAKES TO AVOID:**
- Using `\documentclass{article}` instead of `\documentclass{\handout}`
- Loading packages in wrong order or loading conflicting packages
- Testing document-specific commands that aren't meant to be globally available
- Expecting all commands to be defined when some are document-specific

### Understanding Command Types

**Package-Provided Commands** (should show "defined"):
- `\cnstr`, `\BalGroFac`, `\PopnGroFac`, `\TargetNrm` (from econark.sty)
- Various formatting and utility commands

**Document-Specific Commands** (defined per document):
- `\scale`, `\riskyshk`, `\riskyshkvar` (defined in individual .tex files)
- These are NOT expected to be "defined" in a generic test

## LONG-TERM CONSOLIDATION STRATEGY

### Current State:
- Multiple `.sty` files provide different services
- Each repo bundles its own copies
- Path system allows flexible organization

### Future Goal:
- Single `econark.sty` package containing all services
- Maintained externally but bundled with each repo
- Simplified dependency management
- Consistent interface across all repos

### Migration Approach:
1. **Preserve current architecture** during fixes
2. **Document dependencies** clearly
3. **Test self-containment** thoroughly
4. **Gradually consolidate** services into `econark.sty`
5. **Maintain backward compatibility**

## COMMON MISUNDERSTANDINGS TO AVOID

### ❌ "This has portability issues"
**Wrong**: The relative path system ENSURES portability

### ❌ "Variable-based package loading is risky"
**Wrong**: It's a sophisticated dependency management system

### ❌ "Local texmf directories won't exist on other machines"
**Wrong**: They're part of the repo and will exist wherever the repo is cloned

### ❌ "We should use standard LaTeX package loading"
**Wrong**: This IS standard loading, just with computed paths

## DEBUGGING SELF-CONTAINED ARCHITECTURE

If compilation fails on another machine, follow this systematic debugging approach:

### Step 1: Verify File Structure
```bash
# All these should exist and be non-empty
ls -la .econtexRoot.tex

# Find the actual resources directory name
RESOURCE_DIR=$(find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d | head -1)
ls -la $RESOURCE_DIR/.econtexPaths.tex
find $RESOURCE_DIR/texmf-local -name "*.sty"
```

### Step 2: Verify Git Tracking
```bash
# All necessary files should be tracked
git status
git ls-files | grep -E "\.(tex|sty)$"
```

### Step 3: Test Path Resolution
```bash
# Test the path definitions
grep "econtexRoot" .econtexRoot.tex

# Find and check the actual resources directory
RESOURCE_DIR=$(find . -maxdepth 1 -name "*resource*" -o -name "@*" -o -name "Resources" -type d | head -1)
grep "handoutShortcuts" $RESOURCE_DIR/.econtexPaths.tex
```

### Step 4: **CRITICAL** - Real Compilation Test
```bash
# Create and run the architecture test document
# (Use the test document from REAL COMPILATION TESTING section above)

pdflatex -interaction=nonstopmode test-econark-architecture.tex
EXIT_CODE=$?

echo "Compilation exit code: $EXIT_CODE"

# Extract and analyze the PDF content
pdftotext test-econark-architecture.pdf test-econark-architecture.txt

# Check for critical failure patterns
echo "=== LITERAL LATEX COMMANDS (CRITICAL FAILURE) ==="
grep -E "(provideboolean|setboolean|definecolor|newcolumntype|paperwidth)" test-econark-architecture.txt || echo "✅ No literal LaTeX commands found"

echo "=== PACKAGE COMMAND DEFINITION STATUS ==="
grep -E "(NOT DEFINED|defined)" test-econark-architecture.txt

echo "=== COMPILATION ERRORS ==="
grep -i "error\|fatal\|emergency" test-econark-architecture.log | head -5
```

### Step 5: Interpret Results

**✅ SUCCESS INDICATORS:**
- Exit code 0 (or 1 with PDF generated)
- No literal LaTeX commands in PDF text
- Package commands show "defined" (cnstr, BalGroFac, PopnGroFac, TargetNrm)
- Math symbols render properly as symbols

**❌ CRITICAL FAILURE INDICATORS:**
- LaTeX commands appear as literal text → **Wrong document class or missing base packages**
- Fatal errors preventing PDF generation → **Path resolution problems**
- Most package commands show "NOT DEFINED" → **Package loading failures**

**⚠️ TESTING ERRORS TO AVOID:**
- Using `\documentclass{article}` instead of `\documentclass{\handout}`
- Testing document-specific commands that aren't globally available
- Loading packages in wrong order

**IMPORTANT**: A dry run test (`pdflatex -draftmode`) is **insufficient** for verifying the architecture. Only real compilation with PDF generation and text extraction can reveal package dependency issues and `kpsewhich` problems.

## RULES FOR WORKING WITH EconARK REPOS

### ✅ SAFE TO MODIFY:
- Main document `.tex` files (for macro redefinitions)
- Document-specific `.sty` files in `{PathToResources}/LaTeXInputs/`
- Generated files like `body.tex`
- Content files (figures, tables, etc.)

### ⚠️ MODIFY WITH CAUTION:
- Shared `.sty` files in `{PathToResources}/texmf-local/` (may affect other documents)
- Path definitions in `{PathToResources}/.econtexPaths.tex`

### ❌ NEVER MODIFY:
- `.econtexRoot.tex` (breaks the entire system)
- The relative path architecture
- Variable-based package loading patterns

## SUCCESS CRITERIA

A properly functioning EconARK repo should:
- ✅ Compile successfully on any machine with TeXLive
- ✅ Require no external package installation
- ✅ Work in any directory location
- ✅ Have all dependencies tracked in git
- ✅ Produce identical output across machines

---

**Remember**: This architecture is a FEATURE that ensures portability. Your job is to fix compilation warnings while preserving this sophisticated dependency management system. 