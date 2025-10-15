"""Agentic Development Workflow Complete Orchestration Script.

This script orchestrates the complete workflow from initialization through testing.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "pydantic-ai",
#   "junitparser",
# ]
# ///

import sys
import asyncio
import argparse

from adw_init import adw_init
from adw_plan import adw_plan
from adw_implement import adw_implement
from adw_test_loop import adw_test_loop
from get_or_create_folders import get_or_create_test_folder


async def adw_complete(draft_file_path: str, run_id: str = None, issue_id: str = None) -> bool:
    """Execute the complete ADW workflow.

    Args:
        draft_file_path: Path to the draft file to process
        run_id: Optional run ID (generated if not provided)
        issue_id: Optional issue ID for branch naming

    Returns:
        bool: True if the entire workflow completed successfully, False otherwise
    """
    print("\n" + "="*60)
    print("AGENTIC DEVELOPMENT WORKFLOW - COMPLETE ORCHESTRATION")
    print("="*60)

    # Step 1: Initialize
    print("\n[PHASE 1/4] INITIALIZATION")
    print("-"*60)
    try:
        run_id, draft_destination_path, branch_name, draft_class = await adw_init(
            draft_file_path, run_id, issue_id
        )
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f" Initialization failed: {e}", file=sys.stderr)
        return False

    # Step 2: Plan (create spec)
    print("\n[PHASE 2/4] PLANNING")
    print("-"*60)
    try:
        spec_file_path = await adw_plan(run_id, draft_destination_path, draft_class)
        if not spec_file_path:
            print(" Planning failed: spec file was not created", file=sys.stderr)
            return False
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f" Planning failed: {e}", file=sys.stderr)
        return False

    # Step 3: Implement
    print("\n[PHASE 3/4] IMPLEMENTATION")
    print("-"*60)
    try:
        success = await adw_implement(run_id, str(spec_file_path))
        if not success:
            print(" Implementation failed", file=sys.stderr)
            return False
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f" Implementation failed: {e}", file=sys.stderr)
        return False

    # Step 4: Test loop
    print("\n[PHASE 4/4] TESTING")
    print("-"*60)
    try:
        test_folder = get_or_create_test_folder(run_id)
        success = await adw_test_loop(str(test_folder), str(spec_file_path))
        if not success:
            print(" Testing failed: not all tests passed", file=sys.stderr)
            return False
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f" Testing failed: {e}", file=sys.stderr)
        return False

    # Success!
    print("\n" + "="*60)
    print(" COMPLETE WORKFLOW FINISHED SUCCESSFULLY!")
    print("="*60)
    print(f"  Run ID: {run_id}")
    print(f"  Branch: {branch_name}")
    print(f"  Draft class: {draft_class}")
    print(f"  Spec file: {spec_file_path}")
    print("="*60 + "\n")

    return True


async def main():
    """Main orchestration function for the complete ADW flow."""
    parser = argparse.ArgumentParser(
        description="Execute the complete Agentic Development Workflow: init � plan � implement � test"
    )
    parser.add_argument("--draft", required=True, help="Path to the draft file to process")
    parser.add_argument("--run_id", help="Optional run ID (generated if not provided)")
    parser.add_argument("--issue_id", help="Optional issue ID for branch naming")

    args = parser.parse_args()

    try:
        success = await adw_complete(args.draft, args.run_id, args.issue_id)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
