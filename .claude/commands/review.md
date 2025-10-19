---
argument-hint: [run_id] [spec_file]
description: Review implementation against specification
---

# Review

Follow the `Instructions` below to **review work done against a specification file** to ensure implemented features match requirements. Use the spec file to understand the requirements and then use the git diff if available to understand the changes made. If there are issues, report them; if not, then report success.

## Variables

run_id: $1
spec_file: $2 (optional - if not provided, review will be based on git diff only)

## Instructions

- Check current git branch using `git branch` to understand context
- Run `git diff origin/main` to see all changes made in current branch. Continue even if there are no changes related to the spec file.
- If `spec_file` is provided, read it to understand the requirements
- Compare the implementation against the spec requirements (if provided) and general code quality
- IMPORTANT: Issue Severity Guidelines
  - Think hard about the impact of the issue on the feature and the user
  - Guidelines:
    - `skippable` - the issue is non-blocker for the work to be released but is still a problem
    - `tech_debt` - the issue is non-blocker for the work to be released but will create technical debt that should be addressed in the future
    - `blocker` - the issue is a blocker for the work to be released and should be addressed immediately. It will harm the user experience or will not function as expected.
- IMPORTANT: Return ONLY the JSON object with review results
  - IMPORTANT: Output your result in JSON format based on the `Report` section below.
  - IMPORTANT: Do not include any additional text, explanations, or markdown formatting
  - We'll immediately run JSON.parse() on the output, so make sure it's valid JSON
  - IMPORTANT: Write the JSON output to the file: `${RUN_DIRECTORY}/${run_id}/review/review.json`
- Ultra think as you work through the review process. Focus on the critical functionality paths and the user experience. Don't report issues if they are not critical to the feature.

## Report

- IMPORTANT: Write results exclusively as a JSON object based on the `Output Structure` section below to `${RUN_DIRECTORY}/${run_id}/review/review.json`
- `success` should be `true` if there are NO BLOCKING issues (implementation matches spec for critical functionality)
- `success` should be `false` ONLY if there are BLOCKING issues that prevent the work from being released
- `review_issues` can contain issues of any severity (skippable, tech_debt, or blocker)
- This allows subsequent agents to quickly identify and resolve blocking errors while documenting all issues

### Output Structure

```json
{
    "success": "boolean - true if there are NO BLOCKING issues (can have skippable/tech_debt issues), false if there are BLOCKING issues",
    "review_summary": "string - 2-4 sentences describing what was built and whether it matches the spec. Written as if reporting during a standup meeting. Example: 'The natural language query feature has been implemented with drag-and-drop file upload and interactive table display. The implementation matches the spec requirements for SQL injection protection and supports both CSV and JSON formats. Minor UI improvements could be made but all core functionality is working as specified.'",
    "review_issues": [
        {
            "review_issue_number": "number - the issue number based on the index of this issue (1, 2, 3, ...)",
            "screenshot_path": "",
            "issue_description": "string - description of the issue",
            "issue_resolution": "string - description of the resolution",
            "issue_severity": "string - severity of the issue: 'skippable', 'tech_debt', or 'blocker'"
        }
    ],
    "screenshots": []
}
```

## Example Output

Write to `${RUN_DIRECTORY}/${run_id}/review/review.json`:

```json
{
    "success": true,
    "review_summary": "Review step has been added to the ADW workflow between testing and linting phases. The implementation follows the existing patterns from test loop and includes proper error handling, logging, and iteration limits. All acceptance criteria appear to be met with no blocking issues.",
    "review_issues": [
        {
            "review_issue_number": 1,
            "screenshot_path": "",
            "issue_description": "Missing docstring parameter description for agent_type in adw_review function",
            "issue_resolution": "Add documentation for the agent_type parameter in the function docstring",
            "issue_severity": "tech_debt"
        }
    ],
    "screenshots": []
}
```
