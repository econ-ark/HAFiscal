# Enable CI with Minimal Branch Protection

## Objective
Set up GitHub Actions CI for the Econ-ARK_oc repository with minimal branch protection rules that require CI tests to pass before merging PRs.

## Repository Context
- **Repository**: `llorracc/Econ-ARK_oc` (GitHub)
- **Language**: Python (Poetry-managed package)
- **Purpose**: OpenCollective financial data processing toolkit
- **Main Package**: `econ_ark_oc/` directory contains the Python package
- **Dependencies**: Managed via `pyproject.toml` and `poetry.lock`

## Required CI Tests
The following scripts must ALL pass for CI to succeed:

1. **`/bin/bash reproduce_dates-maker.sh`** - Shell script that creates reproduce scripts for all available dates
2. **`python reproduce_all.py`** - Comprehensive pipeline test that processes all available datasets
3. **`python examples/example_projected_dataframe.py`** - Example script demonstrating projected dataframe functionality

**Note**: The third test requires a date parameter. Use `20250528` as the default test date.

## Implementation Tasks

### Task 1: Create GitHub Actions Workflow

Create `.github/workflows/test.yml` with the following specifications:

**Trigger**: 
- On push to `main` branch only
- On pull requests targeting `main` branch

**Environment**:
- Runner: `ubuntu-latest`
- Python version: `3.10`
- Use Poetry for dependency management

**Steps Required**:
1. Checkout repository code
2. Set up Python 3.10
3. Install Poetry
4. Install project dependencies with Poetry
5. Run the three required test scripts in sequence
6. Each script must exit with code 0 for CI to pass

**Special Considerations**:
- Set working directory to repository root
- Ensure Poetry installs the package in development mode
- Handle the date parameter for the example script
- If any script fails, the entire CI should fail

### Task 2: Configure Branch Protection Rules

Navigate to GitHub repository Settings → Branches and configure protection for the `main` branch:

**Required Settings**:
- ✅ **Require status checks to pass before merging**
  - Include the GitHub Actions workflow as a required status check
  - The status check name will be the job name from the workflow
- ✅ **Require branches to be up to date before merging**
- ❌ **Do NOT require pull request reviews** (minimal protection)
- ❌ **Do NOT restrict pushes** (allow direct pushes to main)
- ❌ **Do NOT prevent force pushes** (keep flexibility)

### Task 3: Verify CI Setup

After implementation, verify the setup works by:

1. **Test CI Trigger**: Make a small change and push to main branch
2. **Check Workflow Execution**: Verify all three scripts run successfully in GitHub Actions
3. **Test Branch Protection**: Create a test PR and confirm it cannot be merged if CI fails
4. **Test Status Checks**: Ensure the workflow appears as a required status check

## Expected Behavior After Setup

### Normal Push to Main:
```bash
git push origin main
```
- ✅ Push succeeds immediately
- 🚀 CI workflow starts automatically
- ✅/❌ CI results appear on commit within 5-10 minutes
- 📧 Notifications sent if CI fails (optional)

### Pull Request Workflow:
```bash
git push origin feature-branch
# Create PR via GitHub UI
```
- 🚀 CI runs automatically on PR
- 🛡️ **Merge blocked** if any of the three scripts fail
- ✅ **Merge allowed** only after all scripts pass
- 🔄 **Re-run CI** automatically when new commits are pushed to PR

### CI Test Details:

**Script 1**: `reproduce_dates-maker.sh`
- **Purpose**: Generates reproduce scripts for available datasets
- **Expected**: Creates/updates `reproduce_*.sh` files
- **Success**: Exit code 0, no errors

**Script 2**: `reproduce_all.py`
- **Purpose**: Full pipeline test across all datasets
- **Expected**: Processes data, generates reports, saves files
- **Success**: Exit code 0, all datasets processed successfully

**Script 3**: `examples/example_projected_dataframe.py 20250528`
- **Purpose**: Tests projected dataframe example functionality
- **Expected**: Loads data, performs analysis, displays results
- **Success**: Exit code 0, example runs without errors

## File Structure After Implementation

```
.github/
└── workflows/
    └── test.yml                    # GitHub Actions workflow

# Repository settings (GitHub UI):
main branch → Protected ✅
├── Require status checks ✅
├── Require up-to-date branches ✅
└── Required status checks:
    └── test / CI-Pipeline ✅
```

## Success Criteria

1. **GitHub Actions workflow** exists and runs on every push/PR
2. **All three scripts** execute successfully in CI environment
3. **Branch protection** prevents merging PRs with failed CI
4. **Direct pushes** to main are still allowed (minimal protection)
5. **CI status** is visible on commits and PRs
6. **No false positives** - CI passes when code is working correctly

## Troubleshooting Notes

**Common Issues**:
- Poetry installation failures → Use official setup-python action
- Missing dependencies → Ensure `poetry install` runs successfully  
- Script execution failures → Check working directory and file permissions
- Branch protection not working → Verify status check names match workflow job names

**Test Data Requirements**:
- Repository must contain `data/20250528/` directory with sample data
- Example scripts depend on processed data files existing
- If data is missing, CI will fail (expected behavior)

This setup provides automated testing while maintaining development flexibility for direct pushes to main branch. 