---
argument-hint: [path_to_spec_file]
description: Run linting and fix issues
---

# Linting

Discover linting tools configured in the codebase, run them, and fix issues iteratively until all linting passes or maximum iterations reached.

## Variables

- `path_to_spec_file`: $1

## Instructions

### Phase 1: Linting Tool Discovery

Identify which linting tools are configured in the codebase:

1. **Check Configuration Files**
   - Python projects: pyproject.toml (ruff, black, mypy), setup.cfg, .flake8, .pylintrc
   - JavaScript/TypeScript: package.json (eslint, prettier), .eslintrc.*, prettier.config.js
   - Common tools: .editorconfig, pre-commit config files
   
2. **Identify Linting Commands**
   - Check package.json "scripts" section for lint commands
   - Check Makefile, justfile, or task runners for lint targets
   - Check CI/CD configs (.github/workflows, .gitlab-ci.yml) for linting steps
   - Common patterns: `npm run lint`, `ruff check`, `flake8`, `mypy`, `eslint`

3. **Determine Execution Order**
   - Run formatters first (black, prettier) if configured
   - Run linters second (ruff, eslint, flake8)
   - Run type checkers last (mypy, tsc)

### Phase 2: Iterative Linting & Fixing

Execute linting and fix issues in a loop:

1. **Iteration Loop** (max 5 iterations to prevent infinite loops)
   ```yaml
   FOR iteration FROM 1 TO 5:
     Step 1: Run all discovered linting commands
     Step 2: Check if any linting errors exist
     Step 3: If no errors, SUCCESS - exit loop
     Step 4: If errors exist, analyze and fix them
     Step 5: Continue to next iteration
   ```

2. **Running Linters**
   ```bash
   # Execute each discovered linting command
   {discovered_lint_command}
   
   # Capture exit code and output
   # Exit code 0 = passing, non-zero = issues found
   ```

3. **Analyzing Errors**
   - Read linter output carefully
   - Identify file paths and line numbers with issues
   - Understand the specific rule violation
   - Determine if it's fixable automatically or requires code changes

4. **Fixing Issues**
   ```yaml
   IF auto-fixable (formatting, import sorting):
     - Run linter with --fix flag if available
     - Examples: ruff check --fix, eslint --fix, prettier --write
   
   IF requires code changes:
     - Read the spec file at path_to_spec_file for context
     - Read the file with linting errors
     - Make minimal surgical changes to fix violations
     - Preserve existing functionality and patterns
     - Follow the rule's guidance from linter output
   
   ALWAYS:
     - Make smallest possible changes
     - Don't refactor unrelated code
     - Maintain existing code patterns
     - Test that fixes don't break functionality
   ```

5. **Common Fixes**
   - Unused imports: Remove them
   - Import ordering: Use automatic sorters (isort, organize imports)
   - Line length: Break long lines appropriately
   - Formatting: Run auto-formatters (black, prettier)
   - Type errors: Add proper type annotations
   - Variable naming: Rename to follow conventions

### Phase 3: Validation

After fixing or reaching max iterations:

1. **Final Linting Check**
   ```bash
   # Run all linting commands one final time
   {all_lint_commands}
   
   # Expected: All commands exit with code 0 (success)
   ```

2. **Report Results**
   - If all linters pass: Report success
   - If issues remain: Report which linters still have issues and what they are
   - If max iterations reached: Report that limit was hit

## Execution Steps

### Step 1: Discover Linting Configuration

```yaml
1. Search for configuration files:
   - Find: pyproject.toml, package.json, .eslintrc.*, etc.
   - Read: Configuration files to identify tools

2. Identify lint commands:
   - Check: package.json scripts, Makefile, CI configs
   - Extract: Actual commands to run

3. Determine execution order:
   - Formatters: black, prettier
   - Linters: ruff, eslint, flake8
   - Type checkers: mypy, tsc
```

### Step 2: Execute Linting Loop

```bash
iteration = 1
while iteration <= 5:
  echo "Linting iteration $iteration"
  
  # Run all linting commands
  run_all_lint_commands
  
  # Check results
  if all_passed:
    echo "✓ All linting passed"
    exit_success
  
  # Analyze and fix issues
  analyze_errors
  fix_issues
  
  iteration++
  
# If we reach here, max iterations hit
echo "⚠ Max iterations reached, some issues may remain"
```

### Step 3: Validate Final State

```bash
# Run final check
run_all_lint_commands

# Report results
if all_passed:
  echo "✓ Linting completed successfully"
else:
  echo "⚠ Some linting issues remain:"
  list_remaining_issues
```

## Common Linting Tools & Commands

### Python
```bash
# Ruff (fast Python linter)
ruff check .
ruff check --fix .

# Flake8 (linting)
flake8 .

# Black (formatting)
black .

# isort (import sorting)
isort .

# Mypy (type checking)
mypy .
```

### JavaScript/TypeScript
```bash
# ESLint (linting)
npm run lint
npx eslint .
npx eslint --fix .

# Prettier (formatting)
npm run format
npx prettier --check .
npx prettier --write .

# TypeScript compiler (type checking)
npx tsc --noEmit
```

## Anti-Patterns to Avoid

- ❌ Don't skip running linters - always execute discovered commands
- ❌ Don't ignore linting errors - fix them or document why they can't be fixed
- ❌ Don't disable linting rules without understanding why they exist
- ❌ Don't refactor unrelated code while fixing linting issues
- ❌ Don't make changes that break functionality to satisfy linters
- ❌ Don't exceed 5 iterations - exit and report issues instead
- ❌ Don't assume linters are configured - discover them properly
- ❌ Don't run only some linters - execute all discovered ones
- ❌ Don't auto-fix without checking if it's safe
- ❌ Don't modify linting configuration to make errors pass

## Report

After completing linting, provide a structured report:

### Linting Summary

```markdown
## Metadata
Spec File: `{path_to_spec_file}`

## Linting Tools Discovered
{List of linting tools and commands found in codebase}

## Execution Summary
- Total iterations: {N}
- Final status: {PASSED / ISSUES_REMAIN}

## Issues Fixed
{For each iteration, list what was fixed}

## Final State
✓ All linting checks pass
OR
⚠ Remaining issues: {list issues that couldn't be fixed}

## Commands Run
{List all linting commands executed}
```

## Example Workflow

```yaml
Input:
  path_to_spec_file: .agentic-runs/ABC123/spec_ABC123.md

Process:
  1. Discovery:
     - Found: pyproject.toml with ruff and mypy
     - Commands: "ruff check .", "mypy ."
  
  2. Iteration 1:
     - Run: ruff check .
     - Result: 5 errors (unused imports, line too long)
     - Fix: Remove unused imports, break long lines
     - Run: mypy .
     - Result: 2 type errors
     - Fix: Add type annotations
  
  3. Iteration 2:
     - Run: ruff check .
     - Result: PASS
     - Run: mypy .
     - Result: PASS
     - Exit: All linting passed

Output:
  ✓ Linting completed successfully (2 iterations)
  ✓ ruff check: PASS
  ✓ mypy: PASS
```

## Additional Notes

- Focus on automated fixes first (formatting, imports)
- Manual code changes should be minimal and surgical
- If max iterations reached, it's okay - report the state
- Don't break functionality to satisfy linters
- Follow existing code patterns even if linters suggest otherwise
- Context from spec_file_path helps understand intent for complex fixes
