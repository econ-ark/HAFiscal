#!/bin/bash
# Portability Test Script for EconARK LaTeX Repositories
# Run this script in a clean environment (VM) to test self-contained architecture

echo "=== EconARK Repository Portability Test ==="
echo "Testing directory: $(pwd)"
echo "Date: $(date)"
echo

# Test 1: Verify core architecture files exist
echo "=== TEST 1: Core Architecture Files ==="
if [ -f ".econtexRoot.tex" ]; then
    echo "✅ .econtexRoot.tex exists"
    echo "Contents:"
    cat .econtexRoot.tex
else
    echo "❌ .econtexRoot.tex missing - CRITICAL FAILURE"
    exit 1
fi
echo

# Test 2: Find and verify resources directory
echo "=== TEST 2: Resources Directory Discovery ==="
RESOURCE_DIR=$(find . -maxdepth 1 -name "*resource*" -o -name "@*" -type d | head -1)
if [ -n "$RESOURCE_DIR" ]; then
    echo "✅ Resources directory found: $RESOURCE_DIR"
    if [ -f "$RESOURCE_DIR/econtexPaths.tex" ]; then
        echo "✅ econtexPaths.tex exists in $RESOURCE_DIR"
    elif [ -f "@local/econtexPaths.tex" ]; then
        echo "✅ econtexPaths.tex exists in @local"
    else
        echo "❌ econtexPaths.tex missing in $RESOURCE_DIR and @local"
        exit 1
    fi
else
    echo "❌ No resources directory found"
    exit 1
fi
echo

# Test 3: Verify all .sty files are present
echo "=== TEST 3: Style Files Inventory ==="
echo "All .sty files in repository:"
find . -name "*.sty" -type f | sort
echo
echo "Style files in @resources:"
find "@resources/latex" -name "*.sty" -type f 2>/dev/null | sort
echo "Style files in legacy texmf-local:"
find "$RESOURCE_DIR/texmf-local" -name "*.sty" -type f 2>/dev/null | sort
echo

# Test 4: Check variable-based package definitions
echo "=== TEST 4: Variable-Based Package Definitions ==="
echo "Package variables defined in econtexPaths.tex:"
if [ -f "@local/econtexPaths.tex" ]; then
    grep "providecommand.*latex" "@local/econtexPaths.tex" 2>/dev/null || echo "No package variables found"
elif [ -f "$RESOURCE_DIR/econtexPaths.tex" ]; then
    grep "providecommand.*latex" "$RESOURCE_DIR/econtexPaths.tex" 2>/dev/null || echo "No package variables found"
else
    echo "No econtexPaths.tex found"
fi
echo

# Test 5: Verify main document exists and uses architecture
echo "=== TEST 5: Main Document Analysis ==="
MAIN_TEX=$(find . -maxdepth 1 -name "*.tex" -not -name "body.tex" -not -name ".econtexRoot.tex" | head -1)
if [ -n "$MAIN_TEX" ]; then
    echo "✅ Main document found: $MAIN_TEX"
    echo "Checking for .econtexRoot input:"
    if grep -q "input.*econtexRoot" "$MAIN_TEX"; then
        echo "✅ Uses .econtexRoot architecture"
    else
        echo "⚠️  Does not use .econtexRoot architecture"
    fi
    
    echo "Variable-based packages used:"
    grep "usepackage{\\\\.*}" "$MAIN_TEX" || echo "None found"
else
    echo "❌ No main document found"
    exit 1
fi
echo

# Test 6: LaTeX compilation test (dry run)
echo "=== TEST 6: LaTeX Compilation Test ==="
if command -v pdflatex >/dev/null 2>&1; then
    echo "✅ pdflatex available"
    echo "Running dry compilation test..."
    
    # Create a minimal test document
    cat > test-minimal.tex << 'EOF'
\input{./.econtexRoot}
\documentclass{article}
\begin{document}
Test document for portability verification.
\end{document}
EOF
    
    if pdflatex -draftmode -interaction=nonstopmode test-minimal.tex >/dev/null 2>&1; then
        echo "✅ Minimal compilation successful"
    else
        echo "❌ Minimal compilation failed"
        echo "Error details:"
        pdflatex -draftmode -interaction=nonstopmode test-minimal.tex
    fi
    
    # Clean up test files
    rm -f test-minimal.* 2>/dev/null
    
    # Test main document if it exists
    if [ -n "$MAIN_TEX" ]; then
        echo "Testing main document compilation..."
        BASENAME=$(basename "$MAIN_TEX" .tex)
        if pdflatex -draftmode -interaction=nonstopmode "$MAIN_TEX" >/dev/null 2>&1; then
            echo "✅ Main document compilation successful"
        else
            echo "❌ Main document compilation failed"
            echo "Checking log for critical errors:"
            grep -i "error\|fatal\|emergency\|file.*not found" "logs/$BASENAME.log" 2>/dev/null || echo "No critical errors found in log"
        fi
        
        # Clean up auxiliary files after compilation tests
        if [ -f ../tools/cleanup.sh ]; then
            echo "Running cleanup script..."
            ../tools/cleanup.sh
        elif [ -f tools/cleanup.sh ]; then
            echo "Running cleanup script..."
            ./tools/cleanup.sh
        else
            echo "Manual cleanup of auxiliary files..."
            rm -f *.aux *.out *.toc *.synctex.gz *.fdb_latexmk *.fls 2>/dev/null
rm -f logs/*.log 2>/dev/null
        fi
    fi
else
    echo "⚠️  pdflatex not available - cannot test compilation"
fi
echo

# Test 7: Git repository integrity
echo "=== TEST 7: Git Repository Integrity ==="
if [ -d ".git" ]; then
    echo "✅ Git repository detected"
    echo "Tracked .sty files:"
    git ls-files | grep "\.sty$" | wc -l | xargs echo "Count:"
    
    echo "Untracked files that might be important:"
    git status --porcelain | grep -E "\.(tex|sty)$" || echo "None"
else
    echo "⚠️  Not a git repository or .git not present"
fi
echo

echo "=== PORTABILITY TEST COMPLETE ==="
echo "If all tests show ✅, the repository should be fully portable."
echo "Any ❌ indicates issues that need to be resolved." 