"""Agentic Development Workflow Planning Script.

This script orchestrates the creation of specification files for a workflow run.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "rich",
# ]
# ///

import sys
import asyncio
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

from console import console
from get_or_create_folders import get_or_create_run_folder
from models import DraftClass
from coding_agent import call_coding_agent
from agent_types import AgentType
from arg_utils import add_agent_argument, parse_agent_type

load_dotenv()


async def adw_plan(
    run_id: str,
    draft_file_path: str,
    draft_class: DraftClass,
    agent_type: AgentType = AgentType.CLAUDE
) -> Path | None:
    """
    Creates a spec file by calling Claude Code with the appropriate command.

    Args:
        run_id: The run identifier
        draft_file_path: Path to the draft file
        draft_class: Classification of the draft (DraftClass.FEATURE or DraftClass.BUG)

    Returns:
        Path | None: Path to the spec file if successfully created, None otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting planning phase for run %s", run_id)

    # Get or create run folder
    run_folder = get_or_create_run_folder(run_id)

    # Generate spec file path
    spec_file_path = run_folder / f"spec_{run_id}.md"

    # Determine which command to use based on draft class
    if draft_class == DraftClass.FEATURE:
        slash_command = "feature"
    elif draft_class == DraftClass.BUG:
        slash_command = "bug"
    else:
        error_msg = (
            f"Unknown draft class: {draft_class}. "
            "Expected DraftClass.FEATURE or DraftClass.BUG."
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Call the coding agent
    try:
        status_text = f"[cyan]{agent_type.value.capitalize()} is planning...[/cyan]"
        with console.status(status_text):
            await call_coding_agent(
                agent_type, slash_command,
                [run_id, draft_file_path, str(spec_file_path)]
            )
    except Exception as e:
        logger.error("Coding agent failed during planning: %s", e, exc_info=True)
        raise

    # Check if spec file was created
    spec_exists = spec_file_path.exists()

    if spec_exists:
        console.print(f"[green]✓[/green] Spec file created successfully at: {spec_file_path}")
        logger.info("Spec file created successfully: %s", spec_file_path)
        return spec_file_path

    console.print(f"[red]✗[/red] Spec file was not created at: {spec_file_path}")
    logger.error("Spec file was not created at expected path: %s", spec_file_path)
    return None


async def main():
    """Main orchestration function for the ADW planning flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Create specification file for Agentic Development Workflow"
    )
    parser.add_argument("--run_id", required=True, help="The run identifier")
    parser.add_argument("--draft", required=True, help="Path to the draft file")
    parser.add_argument(
        "--draft_class",
        required=True,
        choices=["feature", "bug"],
        help="Classification of the draft (feature or bug)"
    )
    add_agent_argument(parser)

    args = parser.parse_args()

    # Convert draft_class string to DraftClass enum
    draft_class = DraftClass.FEATURE if args.draft_class.lower() == "feature" else DraftClass.BUG

    try:
        agent_type = parse_agent_type(args)
        success = await adw_plan(args.run_id, args.draft, draft_class, agent_type)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
