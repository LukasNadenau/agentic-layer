---
argument-hint: [path_to_test_results]
description: Run unit tests and e2e tests
---

# Run Tests

Read the `Instructions` to identify and prepare and then follow the `Execution Steps` to execute all unit tests and end-to-end (e2e) tests in the project, outputting results in JUnit XML format at the specified `path_to_test_results`.

## Variables

`path_to_test_results`: $1

## Instructions

### Phase 1: Test Framework Discovery

Identify all testing frameworks and test configurations in the project:

1. **Search for Test Configuration Files**

   - Look for common test config files: `jest.config.js`, `vitest.config.ts`, `playwright.config.ts`, `cypress.config.js`, `pytest.ini`, `phpunit.xml`, `karma.conf.js`, `mocha.opts`, `.mocharc.json`, etc.
   - Check `package.json` for test scripts and testing dependencies
   - Check language-specific configs: `pom.xml` (Java), `Cargo.toml` (Rust), `go.mod` (Go), etc.

2. **Identify Testing Frameworks**
   Common frameworks by language:

   - **JavaScript/TypeScript**: Jest, Vitest, Mocha, Jasmine, Playwright, Cypress, WebdriverIO
   - **Python**: pytest, unittest, nose2
   - **Java**: JUnit, TestNG
   - **C#/.NET**: xUnit, NUnit, MSTest
   - **Go**: go test
   - **Ruby**: RSpec, Minitest
   - **Rust**: cargo test
   - **PHP**: PHPUnit

3. **Locate Test Directories**
   - Find test files by pattern: `**/*.test.*`, `**/*.spec.*`, `**/test_*.py`, `**/*_test.go`, etc.
   - Common test directories: `test/`, `tests/`, `__tests__/`, `spec/`, `e2e/`, `integration/`

### Phase 2: Test Execution Strategy

Execute tests with JUnit XML output:

1. **Prepare Output Directory**

   - Ensure `path_to_test_results` directory exists
   - Create subdirectories if needed: `unit/`, `e2e/`, `integration/`

2. **Execute Tests with JUnit XML Output**

   **CRITICAL**: Always use CLI flags/options to generate JUnit XML format directly. Only generate XML manually as a last resort if the framework doesn't support it.

   Common JUnit XML output flags:

   **JavaScript/TypeScript:**

   - Jest: `--reporters=default --reporters=jest-junit` with `JEST_JUNIT_OUTPUT_DIR` env var
   - Vitest: `--reporter=junit --outputFile=path/to/results.xml`
   - Playwright: `--reporter=junit` with `PLAYWRIGHT_JUNIT_OUTPUT_NAME`
   - Cypress: `--reporter junit --reporter-options mochaFile=path/to/results.xml`
   - Mocha: `--reporter mocha-junit-reporter --reporter-options mochaFile=path/to/results.xml`

   **Python:**

   - pytest: `--junit-xml=path/to/results.xml`
   - unittest: Use `xmlrunner` package with `python -m xmlrunner discover -o path/to/results`

   **Java:**

   - Maven: `mvn test` (outputs to `target/surefire-reports/` by default)
   - Gradle: `gradle test` with `test.reports.junitXml.destination`

   **C#/.NET:**

   - dotnet: `dotnet test --logger "junit;LogFilePath=path/to/results.xml"`

   **Go:**

   - go test: `go test -v ./... | go-junit-report > path/to/results.xml` (requires go-junit-report)

   **Ruby:**

   - RSpec: `rspec --format RspecJunitFormatter --out path/to/results.xml`

   **Rust:**

   - cargo: `cargo test -- --format=json | cargo2junit > path/to/results.xml`

   **PHP:**

   - PHPUnit: `phpunit --log-junit path/to/results.xml`

3. **Run Tests in Sequence**

   - Execute unit tests first, output to `{path_to_test_results}/unit-tests.xml`
   - Execute e2e tests second, output to `{path_to_test_results}/e2e-tests.xml`
   - Execute integration tests if present, output to `{path_to_test_results}/integration-tests.xml`

4. **Handle Test Failures**
   - Continue running all test suites even if some fail
   - Capture exit codes to report overall success/failure
   - Ensure all XML files are generated even when tests fail

### Phase 3: Validation

After test execution:

1. **Verify XML Files Created**

   - Check that XML files exist at expected paths
   - Verify XML files are valid (contain `<testsuites>` or `<testsuite>` root elements)
   - Confirm non-zero file sizes

2. **Report Summary**
   - Parse XML files to extract: total tests, failures, errors, skipped
   - Report summary statistics for each test suite
   - Highlight any failures or errors with file paths and line numbers if available

## Execution Steps

Follow these steps in order:

1. **Identify Testing Frameworks**

   - Search for test configuration files in the project root
   - Read `package.json`, `pom.xml`, `Cargo.toml`, or equivalent for test dependencies
   - Identify which testing frameworks are used

2. **Ensure Output Directory Exists**

   ```bash
   mkdir -p "{path_to_test_results}"
   ```

3. **Install Required Reporters (if needed)**

   - For Jest: Check if `jest-junit` is installed, install if missing
   - For Mocha: Check if `mocha-junit-reporter` is installed
   - For Go: Check if `go-junit-report` is available
   - For Python: Check if `pytest-junit` or `xmlrunner` is available

4. **Execute Unit Tests**

   - Run the appropriate test command with JUnit XML output flag
   - Direct output to `{path_to_test_results}/unit-tests.xml`
   - Example: `npm test -- --reporters=jest-junit`

5. **Execute E2E Tests**

   - Run e2e test command with JUnit XML output flag
   - Direct output to `{path_to_test_results}/e2e-tests.xml`
   - Example: `npm run test:e2e -- --reporter=junit`

6. **Verify Results**

   - List files in `{path_to_test_results}`
   - Confirm XML files were created
   - Parse and report summary statistics

7. **Report Status**
   - Exit with status code 0 if all tests passed
   - Exit with status code 1 if any tests failed
   - Report test suite summaries with pass/fail counts

## Expected Output Structure

The generated JUnit XML files should follow this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Test Suite Name" tests="N" failures="N" errors="N" time="N.NNN">
  <testsuite name="Suite Name" tests="N" failures="N" errors="N" skipped="N" time="N.NNN" timestamp="ISO-8601">
    <testcase classname="test.ClassName" name="test_name" time="N.NNN">
      <!-- Passing test -->
    </testcase>
    <testcase classname="test.ClassName" name="test_failure" time="N.NNN">
      <failure message="Assertion message" type="AssertionError">
        Stack trace and details
      </failure>
    </testcase>
    <testcase classname="test.ClassName" name="test_error" time="N.NNN">
      <error message="Error message" type="ErrorType">
        Stack trace and details
      </error>
    </testcase>
  </testsuite>
</testsuites>
```

## Common Patterns

**Node.js/Jest:**

```bash
npm test -- --reporters=default --reporters=jest-junit
# Set JEST_JUNIT_OUTPUT_DIR to {path_to_test_results}
```

**Node.js/Vitest:**

```bash
npx vitest run --reporter=junit --outputFile={path_to_test_results}/results.xml
```

**Python/pytest:**

```bash
pytest --junit-xml={path_to_test_results}/results.xml
```

**Java/Maven:**

```bash
mvn test
cp target/surefire-reports/*.xml {path_to_test_results}/
```

**Go:**

```bash
go test -v ./... 2>&1 | go-junit-report > {path_to_test_results}/results.xml
```

**.NET:**

```bash
dotnet test --logger "junit;LogFilePath={path_to_test_results}/results.xml"
```

## Troubleshooting

- If a framework doesn't natively support JUnit XML, search for reporter plugins/packages
- If no reporter is available, parse test output and generate XML manually following the JUnit schema
- Ensure path separators are correct for the operating system (use forward slashes or escape backslashes)
- Check test script definitions in package.json or equivalent config files
- If tests hang, add timeout flags: `--timeout=300000` (Jest), `--testTimeout=300000` (Vitest)

## Report

After completing all test execution and XML generation:

1. Report the paths to all generated XML files
2. Provide a summary table:
   ```
   Test Suite    | Total | Passed | Failed | Errors | Skipped | Duration
   ------------- | ----- | ------ | ------ | ------ | ------- | --------
   Unit Tests    |   50  |   48   |   2    |   0    |   0     | 5.234s
   E2E Tests     |   20  |   19   |   0    |   1    |   0     | 45.123s
   ------------- | ----- | ------ | ------ | ------ | ------- | --------
   TOTAL         |   70  |   67   |   2    |   1    |   0     | 50.357s
   ```
3. If any tests failed, list the failed test names and locations
