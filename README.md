# Agentic Development Workflow (ADW)

An AI-powered complete development workflow automation system that takes you from idea to tested implementation. Transform a draft document into fully implemented and tested code through an automated four-phase process: initialization, planning, implementation, and testing.

## Overview

ADW orchestrates an end-to-end development workflow using AI agents (via Pydantic AI). From a single draft file, it automatically classifies your idea, creates a git branch, generates a detailed specification, implements the code, and runs tests until they pass—all in one command.

## Features

- **Complete Automation**: Single command executes the entire workflow from draft to tested code
- **AI-Powered Classification**: Automatically determines if your draft describes a feature or bug fix
- **Smart Branch Naming**: Generates meaningful git branch names following conventions (e.g., `feat_run_abc123_add_user_auth`)
- **Specification Generation**: Creates detailed technical specs from your draft ideas
- **Automated Implementation**: AI agents implement code based on the generated specification
- **Test Loop**: Runs tests repeatedly, analyzing failures and fixing issues until all tests pass
- **Organized Run Management**: Creates structured folders for each development run in `.agentic-runs/`
- **Git Integration**: Automatically creates and checks out branches for your work

## Workflow Phases

When you run `adw_init_plan_implement_test.py`, the system executes four phases:

### Phase 1: Initialization

1. **Generate Run ID**: Creates a unique identifier for the workflow run
2. **Create Run Folder**: Sets up a dedicated folder in `.agentic-runs/`
3. **Copy Draft**: Copies your draft file into the run folder
4. **Read Draft**: Loads the draft content for processing
5. **Classify Draft**: Uses AI to determine if it's a FEATURE or BUG
6. **Generate Branch Name**: Creates a semantic branch name based on draft content
7. **Create Branch**: Creates and checks out a new git branch

### Phase 2: Planning

1. **Generate Specification**: Creates a detailed technical spec from your draft
2. **Save Spec File**: Stores the specification in the run folder

### Phase 3: Implementation

1. **Implement Code**: AI agents write code based on the specification
2. **Verify Implementation**: Ensures code changes align with the spec

### Phase 4: Testing

1. **Run Tests**: Executes the test suite
2. **Analyze Failures**: Identifies and diagnoses test failures
3. **Fix Issues**: Automatically fixes failing tests
4. **Loop**: Repeats until all tests pass or max iterations reached

## Setup

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Configure your environment variables in `.env`:

```
RUN_DIRECTORY=./.agentic-runs
ANTHROPIC_API_KEY=your-api-key
```

3. Ensure you have Python 3.13+ and required dependencies (managed via inline script metadata)

## Usage

### Complete Workflow (Recommended)

Execute the entire workflow from draft to tested implementation:

```bash
uv run .agentic-layer/adw_init_plan_implement_test.py --draft path/to/your/draft.md
```

### With Custom Run ID

```bash
uv run .agentic-layer/adw_init_plan_implement_test.py --draft path/to/your/draft.md --run_id my_custom_id
```

### With Issue ID

```bash
uv run .agentic-layer/adw_init_plan_implement_test.py --draft path/to/your/draft.md --issue_id ISSUE-123
```

### Individual Phase Scripts

You can also run individual phases separately:

- **Initialization only**: `uv run .agentic-layer/adw_init.py --draft path/to/draft.md`
- **Planning only**: `uv run .agentic-layer/adw_plan.py --run_id <run_id> --draft path/to/draft.md`
- **Implementation only**: `uv run .agentic-layer/adw_implement.py --run_id <run_id> --spec path/to/spec.md`
- **Testing only**: `uv run .agentic-layer/adw_test_loop.py --test_folder path/to/tests --spec path/to/spec.md`

## Testing

The project uses pytest for unit testing. Tests are located in the `tests/` directory.

### Running Tests

Run all tests:
```bash
uv run pytest
```

Run tests with verbose output:
```bash
uv run pytest -v
```

Run specific test file:
```bash
uv run pytest tests/test_generate_run_id.py
```

Run specific test:
```bash
uv run pytest tests/test_generate_run_id.py::test_generate_run_id_length
```

### Test Structure

- `tests/` - Root directory for all test files
- `tests/test_*.py` - Test files following pytest naming convention
- Test functions must start with `test_`

### Writing New Tests

1. Create a new file in `tests/` starting with `test_`
2. Import the module to test from `.agentic-layer/`
3. Write test functions starting with `test_`
4. Use clear arrange-act-assert structure
5. Run pytest to verify tests pass

## Project Structure

```
agentic-layer/
├── .agentic-layer/          # Core workflow scripts
│   ├── adw_init_plan_implement_test.py  # Complete workflow orchestration
│   ├── adw_init.py          # Phase 1: Initialization
│   ├── adw_plan.py          # Phase 2: Planning
│   ├── adw_implement.py     # Phase 3: Implementation
│   ├── adw_test_loop.py     # Phase 4: Testing
│   ├── classify_draft.py    # AI draft classification
│   ├── generate_branch_name.py  # AI branch name generation
│   ├── models.py            # Pydantic models
│   └── ...                  # Supporting utilities
├── .agentic-runs/           # Run output directory
│   └── {run_id}/            # Individual run folders
│       ├── draft_{run_id}.md     # Original draft
│       ├── spec_{run_id}.md      # Generated specification
│       └── tests/                # Test results
│           ├── test_results_1.xml
│           └── ...
├── example-prompts/         # Example draft templates
└── .env                     # Environment configuration
```
