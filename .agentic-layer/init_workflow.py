"""Module for initializing the Agentic Development Workflow."""
# /// script
# dependencies = [
#   "pydantic-ai",
#   "python-dotenv",
# ]
# ///

from pathlib import Path
from typing import Tuple

from generate_run_id import generate_run_id
from get_or_create_run_folder import get_or_create_run_folder
from copy_draft_to_run_folder import copy_draft_to_run_folder
from read_draft_text import read_draft_text
from classify_draft import classify_draft, DraftClass
from generate_branch_name import generate_branch_name
from create_branch import create_branch


async def adw_init(draft_file_path: str, run_id: str = None, issue_id: str = None) -> Tuple[str, str, str, DraftClass]:
    """Initialize the Agentic Development Workflow.

    Args:
        draft_file_path: Path to the draft file to process
        run_id: Optional run ID (generated if not provided)
        issue_id: Optional issue ID for branch naming

    Returns:
        Tuple of (run_id, draft_destination_path, branch_name, draft_class)
    """
    # Validate draft file exists
    if not Path(draft_file_path).exists():
        raise FileNotFoundError(f"Draft file not found: {draft_file_path}")

    # Step 1: Generate run ID if not provided
    if not run_id:
        print("Step 1: Generating run ID...")
        run_id = generate_run_id()
        print(f"  Generated run ID: {run_id}")
    else:
        print(f"Step 1: Using provided run ID: {run_id}")

    # Step 2: Create run folder
    print("Step 2: Creating run folder...")
    run_folder = get_or_create_run_folder(run_id)
    print(f"  Run folder created at: {run_folder}")

    # Step 3: Copy draft to run folder
    print("Step 3: Copying draft to run folder...")
    draft_destination_path = copy_draft_to_run_folder(run_id, draft_file_path)
    print(f"  Draft copied to: {draft_destination_path}")

    # Step 4: Read draft content
    print("Step 4: Reading draft content...")
    draft_text = read_draft_text(run_id)
    print(f"  Draft read successfully ({len(draft_text)} characters)")

    # Step 5: Classify the draft
    print("Step 5: Classifying draft...")
    draft_class = await classify_draft(draft_text)
    print(f"  Draft classified as: {draft_class}")

    # Step 6: Generate branch name
    print("Step 6: Generating branch name...")
    branch_name = await generate_branch_name(run_id, draft_class, draft_text, issue_id)
    print(f"  Generated branch name: {branch_name}")

    # Step 7: Create branch
    print("Step 7: Creating git branch...")
    create_branch(branch_name)
    print(f"  Branch created and checked out: {branch_name}")

    print("\n✓ ADW initialization complete!")
    print(f"  Run ID: {run_id}")
    print(f"  Draft file: {draft_file_path}")
    print(f"  Draft class: {draft_class}")
    print(f"  Branch: {branch_name}")

    return run_id, draft_destination_path, branch_name, draft_class
