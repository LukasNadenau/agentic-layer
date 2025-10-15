---
argument-hint: [run_id] [path_to_draft_file] [path_to_spec_file]
description: Plan a feature
---

# Feature Planning

Create a comprehensive implementation plan for a feature at `path_to_spec_file` following the `Plan Format`. Use the `Instructions` to guide your research and planning process.

## Variables

- `run_id`: $1
- `path_to_draft_file`: $2
- `path_to_spec_file`: $3

## Instructions

### Phase 1: Research & Context Gathering

Before creating the plan, thoroughly research the codebase and external resources:

1. **Codebase Analysis**
   - Search for similar features/patterns in the codebase
   - Identify existing conventions and patterns to follow
   - Note testing patterns and validation approaches
   - Understand the project architecture and structure

2. **External Research** (if needed)
   - Search for similar implementations and best practices
   - Gather library/framework documentation URLs
   - Find implementation examples and common pitfalls
   - Identify potential gotchas and edge cases

3. **Context Collection**
   - List all files relevant to the feature
   - Identify new files that need to be created
   - Document existing patterns to mirror
   - Note integration points with existing code

### Phase 2: Plan Creation

CRITICAL: Before writing the plan, THINK DEEPLY about:
- Feature requirements and user value
- Design approach and architecture
- Implementation strategy and order of tasks
- Validation approach and success criteria
- What context the implementer will need to succeed
- What patterns exist in the codebase to follow
- What could go wrong and how to prevent it
- How errors should be logged and handled for agent debugging
- What information an agent needs in logs to diagnose failures

The goal is one-pass implementation success through comprehensive context.

IMPORTANT: A coding agent will implement and debug this feature by reading logs and error messages. Ensure the plan includes:
- Clear logging strategy with what to log at each step
- Structured error handling that produces actionable error messages
- Debug information that helps identify root causes quickly

Create the plan following the `Plan Format` below:
- Replace every `<placeholder>` with detailed, specific content
- Design for extensibility and maintainability
- Follow existing codebase patterns and conventions
- Include comprehensive validation strategy
- Provide sufficient context for the implementer to succeed without asking questions

### Phase 3: Validation Strategy

Ensure the plan includes:
- Executable validation commands for syntax/style checking
- Test commands to validate functionality
- Build/compile commands to ensure no regressions
- Integration test approach if applicable

## Plan Format

Create a file at `path_to_spec_file` with the following structure:

```markdown
# Feature: <feature name>

## Metadata
run_id: `{run_id}`
path_to_draft_file: `{path_to_draft_file}`

## Feature Description
<Describe the feature in detail, including its purpose and value to users>

## User Story
As a <type of user>
I want to <action/goal>
So that <benefit/value>

## Problem Statement
<Clearly define the specific problem or opportunity this feature addresses>

## Solution Statement
<Describe the proposed solution approach and how it solves the problem>

## Context & References

### Documentation & Resources
MUST READ - Include these in context during implementation:

```yaml
- url: <Official API/library docs URL>
  why: <Specific sections/methods needed>
  section: <Particular section to reference>

- file: <path/to/example_pattern.ext>
  why: <Pattern to follow, what to learn from it>
  critical: <Key insight that prevents common errors>

- doc: <Library/framework documentation URL>
  section: <Specific section about implementation>
  critical: <Important detail that could be missed>
```

### Relevant Files
Existing files relevant to implementing this feature:

- `path/to/file1` - <reason for relevance, what patterns to follow>
- `path/to/file2` - <reason for relevance, what to mirror/avoid>

### New Files
Files that need to be created:

- `path/to/new_file1` - <purpose and responsibility>
- `path/to/new_file2` - <purpose and responsibility>

### Known Gotchas & Library Quirks
```
CRITICAL: <Library/framework name> requires <specific setup/pattern>
- <Specific gotcha or constraint from the codebase>
- <Common pitfall and how to avoid it>
- <Version-specific issues or considerations>
```

## Implementation Blueprint

### Data Models & Structure
If applicable, define the core data models, types, and structures needed:

```
<List data models, schemas, types, interfaces, or data structures>
<Include field definitions, validation rules, relationships>
<Note any existing patterns to follow from the codebase>

Examples:
- Database models/schemas
- API request/response types
- Domain models
- Configuration structures
- State management schemas
```

### Logging & Error Handling Strategy

CRITICAL: An AI agent will debug failures by reading logs. Design for agent-readability.

```yaml
Logging:
  What: Entry points, errors (with context), external calls, success
  Levels: DEBUG (execution flow), INFO (milestones), WARNING (recoverable), ERROR (failures)
  Pattern: <Reference existing logging pattern from codebase, e.g., path/to/logger.ext>

Error Handling:
  Types: <Input validation, external failures, resource issues, business logic violations>
  Include: What operation, what inputs (sanitized), what failed, where (file/function), how to fix
  Pattern: Catch specific errors, log with context, raise actionable error messages
```

### Implementation Tasks

IMPORTANT: Execute every task in order, top to bottom.

```yaml
Task 1: <Descriptive task name>
  ACTION: <MODIFY/CREATE/DELETE>
  FILE: <path/to/file>
  INSTRUCTIONS:
    - FIND: <pattern or location to find in existing code>
    - INJECT: <what to add and where>
    - PRESERVE: <existing behavior/patterns to maintain>
    - MIRROR: <path/to/similar_pattern.ext to follow>

Task 2: <Descriptive task name>
  ACTION: <CREATE>
  FILE: <path/to/new_file>
  INSTRUCTIONS:
    - MIRROR: <path/to/existing_example.ext>
    - MODIFY: <what to change from the example>
    - IMPLEMENT: <specific functionality>

<Continue with all tasks in implementation order...>

Task N: Run Validation
  ACTION: VALIDATE
  INSTRUCTIONS:
    - Execute all validation commands
    - Fix any errors iteratively
    - Verify zero regressions
```

### Per-Task Implementation Details

For complex tasks, include pseudocode or detailed logic:

```
Task X: <task name>

<Pseudocode showing the implementation approach with critical details>

Key considerations:
- PATTERN: <Existing pattern to follow - reference file/line>
- GOTCHA: <Critical detail that could cause issues>
- ERROR HANDLING: <How errors should be handled with context>
- LOGGING: <What to log at each step for debugging>
- VALIDATION: <How to validate this specific task>

Example:
  function newFeature(input):
    log.info("Starting newFeature", input_type=input.type)

    // PATTERN: Validate first (see path/to/validator.ext)
    try:
      validated = validateInput(input)
    catch ValidationError as e:
      log.error("Validation failed: {error}", error=e, input=sanitized(input))
      throw ValidationError("Invalid input: {reason}")

    // GOTCHA: Requires specific initialization (see path/to/example.ext)
    resource = initializeResource()

    // PATTERN: Use retry mechanism, log failures with context
    try:
      result = retryOnFailure(() => resource.execute(validated))
    catch ResourceError as e:
      log.error("Execution failed: {error}", error=e, state=resource.state, input=validated)
      throw FeatureError("Processing failed: {actionable message}")

    log.info("newFeature completed", summary=result.summary())
    return formatResponse(result)  // see path/to/responses.ext
```

### Integration Points

<Define where this feature integrates with existing systems>

```yaml
DATABASE:
  - <Describe schema changes, migrations, or data access patterns>

CONFIGURATION:
  - <List configuration values, environment variables, or settings>

APIS/ENDPOINTS:
  - <List new or modified API endpoints, routes, or interfaces>

SERVICES:
  - <List services or modules that need to be connected or modified>

UI/FRONTEND:
  - <List UI components, pages, or interactions to add/modify>
```

## Testing Strategy

### Unit Tests
<Describe unit tests needed for the feature. Include specific test cases following existing test patterns>

```
Test cases to implement:
- test_happy_path: <description of basic functionality test>
- test_validation_errors: <description of input validation tests>
- test_edge_cases: <description of edge case handling>
- test_error_handling: <description of error scenarios>
- test_error_messages: Verify error messages are actionable and contain context
- test_logging: Verify appropriate logs are generated at key points
- test_error_recovery: <description of how system recovers from failures>
```

### Integration Tests
<Describe integration tests needed, if applicable. Include how to test the feature end-to-end>

### Edge Cases
<List edge cases that need to be tested>

- <Edge case 1>
- <Edge case 2>
- <Edge case 3>

## Acceptance Criteria
<List specific, measurable criteria that must be met for the feature to be considered complete>

- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

## Validation Loop

Execute validation in levels, fixing errors before proceeding to next level.

### Level 1: Syntax & Style
```bash
<command to check syntax/linting>
<command to check types/static analysis>

# Expected: No errors. If errors occur, read and fix them before proceeding.
```

### Level 2: Unit Tests
```bash
<command to run unit tests with verbose output>

# Expected: All tests pass. If failures occur:
# 1. Read the error message carefully
# 2. Understand the root cause
# 3. Fix the code (never mock just to pass)
# 4. Re-run tests
# 5. Repeat until all pass
```

### Level 3: Build Validation
```bash
<command to build/compile the project>

# Expected: Clean build with no errors or warnings
```

### Level 4: Integration Tests (if applicable)
```bash
<command to start the application/service>

# Manual validation steps:
<List specific steps to manually verify the feature works>

# Expected behavior:
<Describe what should happen when testing manually>

# Where to check logs:
<Specify log file locations or commands to view logs>

# What to look for in logs:
- Entry point log message: <expected log message>
- Success completion log: <expected log message>
- If errors occur: <what error logs will indicate the problem>
```

## Final Validation Checklist
- [ ] All syntax/style checks pass
- [ ] All unit tests pass
- [ ] Build completes without errors
- [ ] Integration tests validate feature works end-to-end
- [ ] All acceptance criteria met
- [ ] No regressions in existing functionality
- [ ] Error cases handled gracefully with actionable error messages
- [ ] Appropriate logging at entry points, errors, and completion
- [ ] Error messages include context (what, where, why, how to fix)
- [ ] Logs are informative but not verbose
- [ ] No sensitive data in logs or error messages

## Anti-Patterns to Avoid
- ❌ Don't create new patterns when existing ones work
- ❌ Don't skip validation because "it should work"
- ❌ Don't ignore failing tests - fix them
- ❌ Don't hardcode values that should be configurable
- ❌ Don't catch all exceptions - be specific
- ❌ Don't log sensitive data (passwords, tokens, PII)
- ❌ Don't use generic error messages like "Something went wrong"
- ❌ Don't swallow errors without logging context
- ❌ Don't log too verbosely - logs should be scannable
- ❌ Don't throw errors without actionable information
- ❌ <Add project-specific anti-patterns to avoid>

## Notes
<Optional: List any additional notes, future considerations, or context that will be helpful during implementation>
```

## Report

After creating the plan:
- Return exclusively the path to the plan file created
- Do not include any additional explanation or summary
