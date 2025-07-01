# Test Repository for Problems - Automated Script Creation

**Prompt for AI to create automated bash script version of EconARK analysis workflow**

## Task

Create a comprehensive bash script in a `tests/` directory that automates the entire EconARK repository analysis workflow from `econark-analysis-workflow.md`. The script should:

1. **Auto-detect the document name** from the current directory name (e.g., if in `Portfolio-CRRA-Latest/`, use `Portfolio-CRRA` as the document name)

2. **Create the script as `tests/test-repo-analysis.sh`** with full automation of:
   - Architecture verification (`econark-repo-architecture_verify.sh`)
   - Initial compilation attempt
   - Systematic LaTeX fixes (if compilation fails)
   - Comprehensive macro analysis (`generate-macro-report.sh`)
   - Final verification and reporting

3. **Include intelligent error handling** that:
   - Stops on critical failures
   - Provides clear status messages
   - Offers suggestions for manual intervention when needed
   - Generates a summary report of all findings

4. **Make it repository-agnostic** by:
   - Auto-detecting the main `.tex` file from directory name
   - Dynamically finding resource paths (Resources/, @resources/, etc.)
   - Adapting to different EconARK repository structures

5. **Provide comprehensive output** including:
   - Real-time progress indicators
   - Summary of all tests performed
   - List of any issues found and fixes applied
   - Final status (✅ success, ⚠️ warnings, ❌ failures)

The script should essentially be a "one-click" solution that runs the entire workflow automatically while providing detailed feedback about what it's doing and what it finds.

## Expected Output

A single executable script `tests/test-repo-analysis.sh` that can be run in any EconARK repository to perform complete automated analysis. 