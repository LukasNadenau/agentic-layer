---
argument-hint: [failing_tests] [path_to_spec_file]
description: Resolve failing tests
---

# Resolve Failed Tests

Analyze and fix failing tests using the provided test failure data. Follow the `Instructions` to systematically diagnose, fix, and validate the resolution.

## Variables

- `failing_tests`: $1
- `path_to_spec_file`: $2

## Instructions

### Phase 1: Test Failure Analysis

Before attempting fixes, thoroughly analyze the test failures:

1. **Parse JUnit XML Test Failure Data**
   - Read the JUnit XML file from `failing_tests` path
   - Extract test names from `<testcase>` elements with `<failure>` or `<error>` children
   - Extract error messages from `<failure message="...">` and `<error message="...">` attributes
   - Extract stack traces from the text content of `<failure>` and `<error>` elements
   - Extract test metadata: `classname`, `name`, `time` attributes
   - Note the failure type based on `<failure>` (assertion) vs `<error>` (exception) tags

2. **Context Discovery**
   - Check recent changes that might have caused the failure:
     ```bash
     git diff origin/main --stat --name-only
     git log --oneline -10
     ```
   - Read the spec file at `path_to_spec_file` to understand requirements and expected behavior
   - Identify the code under test (the actual implementation being tested)
   - Find related tests that might provide context

3. **Root Cause Identification**
   - Determine if the test failure is due to:
     - **Code bug**: Implementation doesn't match expected behavior
     - **Test bug**: Test has incorrect assertions or setup
     - **Breaking change**: Recent changes broke existing functionality
     - **Environment issue**: Missing dependencies, configuration, or setup
     - **Timing issue**: Race conditions, async issues, timeouts

### Phase 2: Reproduce & Diagnose

Before making changes, confirm the failure:

1. **Reproduce the Failure**
   - CRITICAL: Construct the appropriate test execution command based on the test framework
   - Use test `classname` and `name` from JUnit XML to target specific tests
   - Run the failing test(s) to see the full error output
   - Confirm you can reproduce the exact failure
   - Capture the complete error message and stack trace

2. **Read Relevant Code**
   - Read the test file to understand test logic
   - Read the implementation file(s) being tested
   - Read related test files for patterns and context
   - Note existing patterns and conventions

3. **Diagnose Root Cause**
   - Trace through the stack trace to find the failure point
   - Compare expected vs actual behavior
   - Identify what specifically is incorrect
   - Determine the minimal fix required

### Phase 3: Fix Implementation

Apply targeted, minimal fixes:

1. **Determine Fix Strategy**
   - **If code bug**: Fix the implementation to match expected behavior
   - **If test bug**: Fix test assertions, setup, or expectations
   - **If breaking change**: Update tests to match new behavior OR fix the breaking change
   - **If environment issue**: Update dependencies, config, or setup
   - **If timing issue**: Add proper async handling, increase timeouts, or fix race conditions

2. **Apply Minimal Fix**
   - Make the smallest change that resolves the root cause
   - Follow existing code patterns and conventions
   - Preserve existing behavior for passing tests
   - Add error handling or validation if missing
   - Add logging to aid future debugging if appropriate

3. **Update Related Tests (if needed)**
   - If fixing a breaking change, update related tests
   - If adding new validation, add corresponding test cases
   - Ensure test descriptions still match what they test

### Phase 4: Validation

Verify the fix works and doesn't cause regressions:

1. **Run Fixed Test(s)**
   - CRITICAL: Re-run the constructed execution command for each fixed test
   - Confirm all previously failing tests now pass
   - Verify no new errors or warnings

2. **Run Related Tests**
   - Run tests in the same test file
   - Run tests for related functionality
   - Ensure no regressions introduced

3. **Syntax & Style Validation**
   - Run linting/formatting if configured
   - Run type checking if applicable
   - Fix any new issues introduced

## Execution Steps

Follow these steps in order:

### Step 1: Parse JUnit XML Test Failure Data

Read and parse the JUnit XML file at `failing_tests` path:

```yaml
FOR EACH <testcase> with <failure> or <error>:
  Extract:
    - Test name: @name attribute
    - Test class: @classname attribute
    - Error message: <failure>/@message or <error>/@message
    - Stack trace: Text content of <failure> or <error>
    - Failure type: <failure> = assertion, <error> = exception
    - Test duration: @time attribute

Example XML structure:
  <testcase classname="auth.LoginTests" name="test_invalid_password" time="0.652">
    <failure message="AssertionError: Expected status code 401, got 200" type="AssertionError">
      Stack trace here...
    </failure>
  </testcase>
```

### Step 2: Identify Test Framework & Locate Test Files

```yaml
1. Determine test framework from XML classname patterns:
   - JavaScript/TypeScript: classname like "path/to/test.spec.js"
   - Python: classname like "tests.test_module.TestClass"
   - Java: classname like "com.example.tests.AuthTests"
   - .NET: classname like "MyApp.Tests.AuthTests"

2. Search for test files using classname and test name:
   - Use Glob to find matching test files
   - Look for test files containing the test name
   - Common patterns: **/*.test.*, **/*.spec.*, **/test_*.py, **/*_test.go

3. Understand context:
   - Read the spec file at path_to_spec_file for requirements and expected behavior
   - Read the test file to understand what is being validated
   - Find the implementation being tested
   - Read the implementation file(s)
   - Note any recent changes (git diff/log)
```

### Step 3: Construct Execution Command & Reproduce Failure

```yaml
Construct the test execution command based on framework:

JavaScript/TypeScript:
  - Jest: npm test -- --testNamePattern="test_name"
  - Vitest: npx vitest run --reporter=verbose --testNamePattern="test_name"
  - Mocha: npx mocha path/to/test.js --grep "test_name"
  - Playwright: npx playwright test --grep "test_name"

Python:
  - pytest: pytest path/to/test_file.py::TestClass::test_name -v
  - unittest: python -m unittest tests.test_module.TestClass.test_name

Java:
  - Maven: mvn test -Dtest=TestClassName#testMethodName
  - Gradle: gradle test --tests TestClassName.testMethodName

.NET:
  - dotnet test --filter "FullyQualifiedName~TestName"

Go:
  - go test -run TestName ./path/to/package

Then execute:
```

```bash
{constructed_execution_command}

# Capture and analyze the full error output
```

### Step 4: Diagnose Root Cause

Based on error analysis:
- Identify the specific line(s) causing the failure
- Understand why the failure occurs
- Determine if it's a code bug, test bug, or breaking change
- Plan the minimal fix

### Step 5: Apply Fix

```yaml
IF code bug:
  - MODIFY: Implementation file(s)
  - FIX: Specific logic, calculation, or behavior
  - PRESERVE: Existing functionality for passing tests
  - TEST: Verify fix resolves the issue

IF test bug:
  - MODIFY: Test file(s)
  - FIX: Incorrect assertions, setup, or expectations
  - ALIGN: With actual correct behavior
  - TEST: Verify test now passes and validates correctly

IF breaking change:
  - DECIDE: Fix the breaking change OR update tests
  - MODIFY: Implementation or tests accordingly
  - DOCUMENT: Why the change was necessary
  - TEST: Verify all related tests pass

IF environment issue:
  - FIX: Dependencies, configuration, or setup
  - DOCUMENT: What was missing or misconfigured
  - TEST: Verify tests pass with correct setup

IF timing issue:
  - FIX: Async handling, timeouts, or race conditions
  - ADD: Proper await/promises/synchronization
  - TEST: Run multiple times to verify stability
```

### Step 6: Validate Fix

```bash
# Re-run each failing test using constructed execution command
{constructed_execution_command}

# Expected: All previously failing tests now pass

# Run related tests to check for regressions
{related_test_command}

# Expected: No new failures
```

### Step 7: Final Checks

```bash
# Run syntax/style checks
{lint_command}

# Run type checks (if applicable)
{type_check_command}

# Expected: No new errors or warnings
```

## Common Failure Patterns

### Assertion Failures

```
Symptom: "Expected X but got Y"
Root Cause: Implementation returns incorrect value
Fix: Correct the implementation logic

OR

Symptom: "Expected X but got Y"
Root Cause: Test expectation is incorrect
Fix: Update test assertion to match correct behavior
```

### Null/Undefined Errors

```
Symptom: "Cannot read property 'x' of undefined"
Root Cause: Missing null/undefined check
Fix: Add validation or null handling
```

### Async/Timing Issues

```
Symptom: "Timeout exceeded" or "Promise not resolved"
Root Cause: Missing await, incorrect async handling
Fix: Add proper async/await or increase timeout if justified
```

### Import/Module Errors

```
Symptom: "Cannot find module" or "Import error"
Root Cause: Missing dependency or incorrect import path
Fix: Install dependency or correct import path
```

### Type Errors

```
Symptom: "Type 'X' is not assignable to type 'Y'"
Root Cause: Type mismatch in implementation or test
Fix: Correct the type annotations or implementation
```

## Anti-Patterns to Avoid

- ❌ Don't skip reproduction - always run the test first
- ❌ Don't make sweeping changes - be surgical and minimal
- ❌ Don't fix tests by removing assertions - fix the actual issue
- ❌ Don't blindly update test expectations - understand why they fail
- ❌ Don't ignore stack traces - they point to the exact problem
- ❌ Don't skip validation - always re-run the test after fixing
- ❌ Don't forget to check for regressions in related tests
- ❌ Don't modify unrelated code while fixing the test
- ❌ Don't increase timeouts without understanding why tests are slow
- ❌ Don't mock excessively just to make tests pass - fix the real issue

## Report

After resolving all test failures, provide a structured report:

### Test Resolution Summary

```markdown
## Metadata
Spec File: `{path_to_spec_file}`

## Fixed Tests

{For each resolved test:}

### ✅ {test_name} ({test_file})

**Root Cause**: {Brief description of why the test failed}

**Fix Applied**: {Specific changes made to resolve the failure}

**Validation**: ✓ Test now passes

---

## Summary Statistics

- Total tests analyzed: {N}
- Tests fixed: {N}
- Code changes: {N} file(s) modified
- Test changes: {N} file(s) modified

## Validation Results

- ✓ All previously failing tests now pass
- ✓ No regressions in related tests
- ✓ Syntax/style checks pass
- ✓ Type checks pass (if applicable)
```

## Example Workflow

```yaml
Input:
  failing_tests: path/to/test-results.xml

  XML content:
    <testcase classname="auth.LoginTests" name="test_invalid_password" time="0.652">
      <failure message="AssertionError: Expected status code 401, got 200" type="AssertionError">
        AssertionError: Expected status code 401, got 200
          at LoginTests.test_invalid_password (auth.test.js:45)
      </failure>
    </testcase>

Process:
  1. Parse XML: Extract test name, classname, error message, stack trace
  2. Locate: Find tests/auth.test.js (search using classname and test name)
  3. Read: tests/auth.test.js to understand test
  4. Read: src/auth.js (implementation under test)
  5. Construct: npm test -- --testNamePattern="test_invalid_password"
  6. Reproduce: Run constructed command, confirm failure
  7. Diagnose: Missing password validation in auth.js:23
  8. Fix: Add password validation check before authentication
  9. Validate: Re-run test, now passes
  10. Check: Run all auth tests, no regressions

Output:
  ✅ test_invalid_password (auth.LoginTests) - Fixed missing password validation
```

## Additional Notes

- Focus on fixing the root cause, not symptoms
- Make minimal changes to reduce risk
- Always validate fixes by re-running tests
- Check for regressions in related functionality
- Document why changes were necessary if not obvious
- Consider adding additional test cases if gaps are found
