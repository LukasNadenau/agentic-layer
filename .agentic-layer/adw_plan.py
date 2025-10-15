"""Agentic Development Workflow Planning Script.

This script orchestrates the creation of specification files for a workflow run.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import sys
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv

from get_or_create_folders import get_or_create_run_folder
from models import DraftClass
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


async def adw_plan(run_id: str, draft_file_path: str, draft_class: DraftClass) -> Path | None:
    """
    Creates a spec file by calling Claude Code with the appropriate command.

    Args:
        run_id: The run identifier
        draft_file_path: Path to the draft file
        draft_class: Classification of the draft (DraftClass.FEATURE or DraftClass.BUG)

    Returns:
        Path | None: Path to the spec file if successfully created, None otherwise
    """
    # Get or create run folder
    run_folder = get_or_create_run_folder(run_id)

    # Generate spec file path
    spec_file_path = run_folder / f"spec_{run_id}.md"

    # Determine which command to use based on draft class
    if draft_class == DraftClass.FEATURE:
        command = f"/feature {run_id} {draft_file_path} {spec_file_path}"
    elif draft_class == DraftClass.BUG:
        command = f"/bug {run_id} {draft_file_path} {spec_file_path}"
    else:
        raise ValueError(f"Unknown draft class: {draft_class}. Expected DraftClass.FEATURE or DraftClass.BUG.")

    # Set up options with write restriction to spec file path only
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"]
    )

    # Use query to send the slash command
    async for _ in query(prompt=command, options=options):
        pass

    # Check if spec file was created
    spec_exists = spec_file_path.exists()

    if spec_exists:
        print(f"✓ Spec file created successfully at: {spec_file_path}")
        return spec_file_path
    else:
        print(f"✗ Spec file was not created at: {spec_file_path}")
        return None


async def main():
    """Main orchestration function for the ADW planning flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Create specification file for Agentic Development Workflow")
    parser.add_argument("--run_id", required=True, help="The run identifier")
    parser.add_argument("--draft", required=True, help="Path to the draft file")
    parser.add_argument("--draft_class", required=True, choices=["feature", "bug"], help="Classification of the draft (feature or bug)")

    args = parser.parse_args()

    # Convert draft_class string to DraftClass enum
    draft_class = DraftClass.FEATURE if args.draft_class.lower() == "feature" else DraftClass.BUG

    try:
        success = await adw_plan(args.run_id, args.draft, draft_class)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
