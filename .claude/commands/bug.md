---
argument-hint: [run_id] [path_to_draft_file] [path_to_spec_file]
description: Plan a bugfix
---

# Bugfix Planning

Create a comprehensive bugfix plan at `path_to_spec_file` following the `Plan Format`. Use the `Instructions` to guide your research and root cause analysis.

## Variables

- `run_id`: $1
- `path_to_draft_file`: $2
- `path_to_spec_file`: $3

## Instructions

### Phase 1: Research & Root Cause Analysis

Before creating the plan, thoroughly investigate the bug:

1. **Bug Reproduction**
   - Understand the exact steps to reproduce the bug
   - Identify expected vs actual behavior
   - Determine the scope and impact of the bug

2. **Codebase Investigation**
   - Search for the code paths involved in the bug
   - Identify where the bug manifests and where it originates
   - Review related code that might be affected
   - Check for similar bugs or patterns in the codebase

3. **Root Cause Analysis**
   - Trace the bug back to its source
   - Understand why the bug exists (logic error, edge case, race condition, etc.)
   - Identify any related issues that should be fixed together

4. **Context Collection**
   - List all files involved in the bug
   - Document existing patterns to maintain
   - Note integration points that could be affected
   - Identify test files that need updates

### Phase 2: Plan Creation

CRITICAL: Before writing the plan, THINK DEEPLY about:
- The root cause of the bug (not just symptoms)
- The minimal surgical fix that solves the problem
- What could break if we change this code
- How to validate the fix doesn't cause regressions
- What tests are needed to prevent this bug in the future
- How errors should be logged to help diagnose similar issues
- What information an agent needs in logs to debug failures

The goal is a targeted fix that solves the root cause without introducing new issues.

IMPORTANT: A coding agent will implement this fix by reading logs and error messages. Ensure the plan includes:
- Clear logging strategy for debugging the affected code path
- Structured error handling that produces actionable error messages
- Validation steps that prove the bug is fixed

Create the plan following the `Plan Format` below:
- Replace every `<placeholder>` with detailed, specific content
- Be surgical: fix only what's necessary
- Follow existing codebase patterns and conventions
- Include comprehensive validation to prevent regressions
- Provide sufficient context for the implementer to succeed

### Phase 3: Validation Strategy

Ensure the plan includes:
- Steps to reproduce the bug before and after the fix
- Executable validation commands for syntax/style checking
- Test commands that validate the fix
- Regression test approach
- Manual validation steps if applicable

## Plan Format

Create a file at `path_to_spec_file` with the following structure:

```markdown
# Bug: <bug name>

## Metadata
run_id: `{run_id}`
path_to_draft_file: `{path_to_draft_file}`

## Bug Description
<Describe the bug in detail, including symptoms, expected behavior, and actual behavior>

## Problem Statement
<Clearly define the specific problem that needs to be solved>

## Solution Statement
<Describe the proposed solution approach to fix the bug>

## Steps to Reproduce
<List exact steps to reproduce the bug>

1. <Step 1>
2. <Step 2>
3. <Observed behavior>
4. <Expected behavior>

## Root Cause Analysis
<Analyze and explain the root cause of the bug. Don't just describe symptoms - explain WHY the bug exists>

```
Root Cause: <Concise explanation>

Details:
- <What in the code causes this>
- <Why the current implementation fails>
- <Under what conditions the bug manifests>
```

## Context & References

### Documentation & Resources
MUST READ - Include these in context during implementation:

```yaml
- file: <path/to/affected_code.ext>
  why: <What patterns must be preserved>
  critical: <Key insight about the bug>

- file: <path/to/test_file.ext>
  why: <Existing test patterns to follow>

- doc: <External documentation if needed>
  section: <Specific section>
  critical: <Important detail>
```

### Relevant Files
Existing files involved in this bug:

- `path/to/file1` - <reason for involvement, what to change>
- `path/to/file2` - <reason for involvement, what to preserve>

### New Files
Files that need to be created (if any):

- `path/to/new_test.ext` - <purpose and responsibility>

### Known Constraints
```
CRITICAL: <Library/framework constraints>
- <Specific limitation or requirement>
- <Common pitfall related to this bug>
```

## Fix Implementation Blueprint

### Data Models & Structure (if applicable)
If the fix requires changes to data structures:

```
<List any data model, type, or schema changes needed>
<Include validation rules that were missing>
<Note existing patterns to maintain>
```

### Logging & Error Handling Strategy

CRITICAL: An AI agent will debug failures by reading logs. Design for agent-readability.

```yaml
Logging:
  What: Entry to affected code path, error conditions (with context), fix application
  Levels: DEBUG (execution flow), INFO (milestones), WARNING (edge cases), ERROR (failures)
  Pattern: <Reference existing logging pattern from codebase>

Error Handling:
  Types: <Specific error types this bug relates to>
  Include: What operation, what inputs (sanitized), what failed, where (file/function)
  Pattern: Catch specific errors, log with context, raise actionable messages
```

### Implementation Tasks

IMPORTANT: Execute every task in order, top to bottom. Keep changes minimal and surgical.

```yaml
Task 1: <Descriptive task name>
  ACTION: <MODIFY/CREATE/DELETE>
  FILE: <path/to/file>
  INSTRUCTIONS:
    - FIND: <exact pattern or location to find>
    - FIX: <what to change and why>
    - PRESERVE: <existing behavior to maintain>
    - TEST: <how to verify this specific change>

Task 2: <Add/Update tests>
  ACTION: <MODIFY/CREATE>
  FILE: <path/to/test_file>
  INSTRUCTIONS:
    - MIRROR: <existing test pattern to follow>
    - ADD: <test cases that would catch this bug>
    - VERIFY: <what these tests should validate>

<Continue with all tasks in implementation order...>

Task N: Run Validation
  ACTION: VALIDATE
  INSTRUCTIONS:
    - Execute all validation commands
    - Reproduce bug steps - should now work correctly
    - Fix any errors iteratively
    - Verify zero regressions
```

### Per-Task Implementation Details

For complex fixes, include pseudocode or detailed logic:

```
Task X: <task name>

<Pseudocode showing the fix with critical details>

Key considerations:
- BUG: <Exact issue in current code>
- FIX: <How this change solves the root cause>
- PATTERN: <Existing pattern to maintain - reference file/line>
- ERROR HANDLING: <How errors should be handled with context>
- LOGGING: <What to log for debugging>
- VALIDATION: <How to verify this specific fix>

Example:
  function affectedFunction(input):
    log.debug("Entering affectedFunction", input_type=input.type)

    // BUG: Missing validation allowed invalid input (see issue #X)
    // FIX: Add validation check before processing
    if not isValid(input):
      log.error("Invalid input detected", input=sanitized(input), reason=validation_error)
      throw ValidationError("Input validation failed: {specific reason}")

    // Rest of function unchanged to minimize risk
    result = processInput(input)
    log.info("affectedFunction completed successfully")
    return result
```

## Testing Strategy

### Regression Tests
<Describe tests needed to prevent this bug from recurring>

```
Test cases to implement:
- test_bug_reproduction: <test that would fail before fix, pass after>
- test_edge_cases_from_bug: <edge cases exposed by this bug>
- test_related_scenarios: <related scenarios that shouldn't break>
- test_error_messages: Verify error messages are actionable
- test_logging: Verify appropriate logs at affected code path
```

### Validation Tests
<Describe how to validate the fix works>

### Regression Prevention
<List existing tests that should still pass>

- <Existing test suite 1>
- <Existing test suite 2>

## Acceptance Criteria
<List specific, measurable criteria that must be met for the bug to be considered fixed>

- [ ] Bug reproduction steps no longer produce the error
- [ ] All existing tests still pass
- [ ] New tests added to prevent regression
- [ ] No new warnings or errors introduced
- [ ] <Additional criterion>

## Validation Loop

Execute validation in levels, fixing errors before proceeding to next level.

### Level 1: Syntax & Style
```bash
<command to check syntax/linting>
<command to check types/static analysis>

# Expected: No errors. If errors occur, read and fix them before proceeding.
```

### Level 2: Bug Reproduction
```bash
# Reproduce the bug using the steps from "Steps to Reproduce" section
# Expected: Bug should no longer occur. Document what happens now.
```

### Level 3: Unit Tests
```bash
<command to run unit tests with verbose output>

# Expected: All tests pass, including new tests for this bug.
# If failures occur:
# 1. Read the error message carefully
# 2. Understand the root cause
# 3. Fix the code
# 4. Re-run tests
# 5. Repeat until all pass
```

### Level 4: Regression Tests
```bash
<command to run full test suite>

# Expected: No regressions. All existing tests still pass.
```

### Level 5: Build Validation
```bash
<command to build/compile the project>

# Expected: Clean build with no errors or warnings
```

### Level 6: Manual Validation (if applicable)
```bash
<command to start the application/service>

# Manual validation steps:
<List specific steps to manually verify the fix works>

# Expected behavior:
<Describe what should happen now vs. before>

# Where to check logs:
<Specify log file locations or commands to view logs>

# What to look for in logs:
- Before fix: <what logs showed when bug occurred>
- After fix: <what logs should show now>
```

## Final Validation Checklist
- [ ] All syntax/style checks pass
- [ ] Bug can no longer be reproduced
- [ ] All new tests pass
- [ ] All existing tests still pass (no regressions)
- [ ] Build completes without errors
- [ ] Manual validation confirms fix (if applicable)
- [ ] All acceptance criteria met
- [ ] Error cases handled gracefully with actionable messages
- [ ] Appropriate logging at affected code paths
- [ ] No sensitive data in logs or error messages

## Anti-Patterns to Avoid
- ❌ Don't fix symptoms - fix root causes
- ❌ Don't make unnecessary changes beyond the fix
- ❌ Don't skip validation because "it's a small fix"
- ❌ Don't ignore failing tests - they might reveal related issues
- ❌ Don't remove error handling to "fix" errors
- ❌ Don't add workarounds when proper fixes are possible
- ❌ Don't assume the bug is isolated - check for similar issues
- ❌ Don't catch all exceptions - be specific
- ❌ Don't use generic error messages
- ❌ Don't swallow errors without logging context
- ❌ <Add project-specific anti-patterns>

## Notes
<Optional: List any additional notes, related bugs, future considerations, or context that will be helpful during implementation>
```

## Report

After creating the plan:
- Return exclusively the path to the plan file created
- Do not include any additional explanation or summary
