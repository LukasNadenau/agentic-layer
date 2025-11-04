---
argument-hint: [path_to_draft_file] [path_to_output_file]
description: Classify a draft as FEATURE or BUG
---

# Draft Classification

Classify the draft text at `path_to_draft_file` as either FEATURE or BUG and write the result to `path_to_output_file`.

## Variables

- `path_to_draft_file`: $1
- `path_to_output_file`: $2

## Instructions

1. Read the draft file at `path_to_draft_file`
2. Analyze the content to determine if it describes:
   - **FEATURE**: A new capability, enhancement, or functionality
   - **BUG**: A defect, error, or problem that needs to be fixed

## Classification Guidelines

**FEATURE indicators:**
- Adding new functionality
- Enhancing existing capabilities
- Implementing new user-facing features
- Improving user experience
- Adding new endpoints, methods, or components

**BUG indicators:**
- Fixing broken functionality
- Resolving errors or crashes
- Correcting unexpected behavior
- Patching security issues
- Fixing performance problems

## Report

Write ONLY one of the following two words to `path_to_output_file` with no additional text:
- `FEATURE`
- `BUG`

Do not include any explanation, summary, or additional formatting. Write exclusively the classification word to the file.
