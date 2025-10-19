---
argument-hint: [issue_description] [spec_path]
description: Apply targeted patch to fix review issue
---

# Patch

Create a **focused patch** to resolve a specific issue based on the `issue_description`. Make minimal, surgical changes to fix only the described issue.

## Variables

issue_description: $1 (contains both issue description and resolution)
spec_path: $2 (optional - if provided, read for context)

## Instructions

- IMPORTANT: You're applying a targeted patch to fix a specific review issue. Keep changes small, focused, and surgical
- Read the `issue_description` to understand exactly what needs to be fixed
- The `issue_description` contains both the problem and the suggested resolution
- If `spec_path` is provided, read it to understand the broader context and requirements
- Run `git diff --stat` to understand recent changes and avoid breaking existing work
- Make ONLY the changes necessary to fix the described issue - nothing more
- Follow existing code patterns and style in the files you modify
- Ultra think about the most efficient way to implement the fix with minimal code changes
- Validate your changes don't break existing functionality

## Implementation Steps

1. **Understand the Issue**
   - Parse the `issue_description` to identify the problem and proposed resolution
   - Read relevant files to understand current implementation
   - If `spec_path` provided, read it for context

2. **Make Minimal Changes**
   - Apply only the changes needed to fix the specific issue
   - Follow existing code patterns and conventions
   - Preserve all working functionality

3. **Validate the Fix**
   - Verify the specific issue is resolved
   - Check that no regressions were introduced
   - Run relevant tests if applicable

## Validation

After making changes:

- Read the modified files to confirm changes are correct
- Run `git diff` to review all modifications
- Verify the issue described in `issue_description` is now fixed
- Check that changes follow existing code patterns

## Patch Guidelines

**DO:**
- Make minimal, targeted changes
- Fix only what's described in the issue
- Follow existing code style and patterns
- Preserve all working functionality
- Use descriptive variable/function names that match the codebase

**DON'T:**
- Make unrelated changes or improvements
- Refactor working code
- Change coding style or conventions
- Add features not described in the issue
- Break existing functionality

## Report

After completing the patch, briefly confirm what was fixed (1-2 sentences).
