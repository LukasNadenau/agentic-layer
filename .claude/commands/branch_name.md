---
argument-hint: [path_to_draft_file] [path_to_output_file]
description: Generate a branch name description
---

# Branch Name Generation

Generate a concise branch name description for the draft at `path_to_draft_file` and write it to `path_to_output_file`.

## Variables

- `path_to_draft_file`: $1
- `path_to_output_file`: $2

## Instructions

1. Read the draft file at `path_to_draft_file`
2. Generate a short, descriptive name (3-5 words maximum) that captures the key action or change
3. Use snake_case format (lowercase with underscores)
4. Focus on the primary action being taken

## Guidelines

**Good examples:**
- `add_user_auth`
- `fix_login_crash`
- `update_api_endpoint`
- `refactor_data_model`
- `remove_deprecated_code`

**Format rules:**
- Use action verbs (add, fix, update, remove, refactor, etc.)
- Keep it brief (3-5 words max)
- Use snake_case (lowercase_with_underscores)
- No special characters except underscores
- Be specific but concise

## Report

Write ONLY the short description in snake_case format to `path_to_output_file` with no additional text.

Do not include any explanation, prefix, suffix, or additional formatting. Write exclusively the snake_case description to the file.

Example outputs (these would be written to the file):
- `add_user_authentication`
- `fix_null_pointer_error`
- `update_payment_api`
