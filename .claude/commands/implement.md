---
argument-hint: [path_to_spec_file]
description: Implement a feature
---

# Implementation Execution

Execute the implementation plan from the spec file.

## Variables

- `path_to_spec_file`: $1

## Execution Process

1. **Load Plan**

   - Read the spec file at `path_to_spec_file`
   - Understand all context, requirements, and instructions
   - Load all referenced files and documentation from "Context & References"

2. **ULTRATHINK**

   - Think deeply about the implementation approach
   - Use TodoWrite to create todos from "Implementation Tasks" section
   - Identify dependencies and potential issues

3. **Execute Implementation Tasks**

   - Execute each task in exact order from the plan
   - Follow ACTION, FILE, and INSTRUCTIONS for each task
   - Follow FIND, INJECT/FIX, PRESERVE, MIRROR patterns
   - Apply logging and error handling as specified in the plan
   - Mark each todo as in_progress, then completed

4. **Run Validation Loop**

   - Execute each validation level from the plan in order
   - Fix any errors before proceeding to next level
   - Do not skip validation steps

5. **Verify Completion**

   - Check all Acceptance Criteria are met
   - Review Final Validation Checklist
   - Re-read spec file to ensure nothing was missed

6. **Reference the Plan**
   - Always refer back to the spec file when in doubt
   - Follow the plan's patterns and strategies exactly

## Report

After completing the implementation:

- Summarize the work done in bullet points
- Report files and lines changed with `git diff --stat`
- Confirm all validation levels passed
- Confirm all acceptance criteria met
