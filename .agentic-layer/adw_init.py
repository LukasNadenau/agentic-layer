"""Agentic Development Workflow Initialization Script.

This script orchestrates the initialization of a new development workflow run.
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
from typing import Tuple

from console import console
from generate_run_id import generate_run_id
from get_or_create_folders import get_or_create_run_folder
from copy_draft_to_run_folder import copy_draft_to_run_folder
from read_draft_text import read_draft_text
from classify_draft import classify_draft
from models import DraftClass
from generate_branch_name import generate_branch_name
from create_branch import create_branch
from agent_types import AgentType
from arg_utils import add_agent_argument, parse_agent_type
from logging_config import setup_logging


def _print_initialization_summary(
    run_id: str, draft_file_path: str, draft_class, branch_name: str
):
    """Print the initialization completion summary."""
    logger = logging.getLogger(__name__)
    console.print("\n[green]✓[/green] ADW initialization complete!")
    console.print(f"  [cyan]Run ID:[/cyan] {run_id}")
    console.print(f"  [cyan]Draft file:[/cyan] {draft_file_path}")
    console.print(f"  [cyan]Draft class:[/cyan] {draft_class}")
    console.print(f"  [cyan]Branch:[/cyan] {branch_name}")

    logger.info("ADW initialization completed successfully")
    logger.info("Summary - Run ID: %s, Branch: %s, Classification: %s",
                run_id, branch_name, draft_class)


def _setup_run_folder_and_draft(run_id: str, draft_file_path: str) -> Tuple[str, str]:
    """Set up run folder and copy draft, return draft destination and content."""
    logger = logging.getLogger(__name__)

    # Create run folder
    console.print("[cyan]Step 2:[/cyan] Creating run folder...")
    logger.debug("Creating run folder for run_id: %s", run_id)
    run_folder = get_or_create_run_folder(run_id)
    console.print(f"  Run folder created at: {run_folder}")
    logger.info("Run folder created: %s", run_folder)

    # Copy draft to run folder
    console.print("[cyan]Step 3:[/cyan] Copying draft to run folder...")
    logger.debug("Copying draft from %s to run folder", draft_file_path)
    draft_destination_path = copy_draft_to_run_folder(run_id, draft_file_path)
    console.print(f"  Draft copied to: {draft_destination_path}")
    logger.info("Draft copied to: %s", draft_destination_path)

    # Read draft content
    console.print("[cyan]Step 4:[/cyan] Reading draft content...")
    logger.debug("Reading draft text from run folder")
    draft_text = read_draft_text(run_id)
    console.print(f"  Draft read successfully ({len(draft_text)} characters)")
    logger.debug("Draft text length: %s characters", len(draft_text))

    return draft_destination_path, draft_text


async def _classify_and_create_branch(
    run_id: str, draft_text: str, issue_id: str = None, agent_type: AgentType = AgentType.CLAUDE
) -> Tuple[DraftClass, str]:
    """Classify draft and create git branch, return classification and branch name."""
    logger = logging.getLogger(__name__)

    # Classify the draft
    console.print("[cyan]Step 5:[/cyan] Classifying draft...")
    logger.debug("Starting draft classification with %s agent", agent_type.value)
    try:
        status_text = f"[cyan]Classifying with {agent_type.value.capitalize()}...[/cyan]"
        with console.status(status_text):
            draft_class = await classify_draft(draft_text, agent_type)
        console.print(f"  Draft classified as: [bold]{draft_class}[/bold]")
        logger.info("Draft classified as: %s", draft_class)
    except Exception as e:
        logger.error("Draft classification failed: %s", e, exc_info=True)
        raise

    # Generate branch name
    console.print("[cyan]Step 6:[/cyan] Generating branch name...")
    logger.debug("Generating branch name for %s with issue_id: %s", draft_class, issue_id)
    try:
        status_text = f"[cyan]Generating with {agent_type.value.capitalize()}...[/cyan]"
        with console.status(status_text):
            branch_name = await generate_branch_name(run_id, draft_class, draft_text, issue_id, agent_type)
        console.print(f"  Generated branch name: [bold]{branch_name}[/bold]")
        logger.info("Generated branch name: %s", branch_name)
    except Exception as e:
        logger.error("Branch name generation failed: %s", e, exc_info=True)
        raise

    # Create branch
    console.print("[cyan]Step 7:[/cyan] Creating git branch...")
    logger.debug("Creating git branch: %s", branch_name)
    try:
        create_branch(branch_name)
        console.print(f"  Branch created and checked out: [bold]{branch_name}[/bold]")
        logger.info("Git branch created and checked out: %s", branch_name)
    except Exception as e:
        logger.error("Branch creation failed: %s", e, exc_info=True)
        raise

    return draft_class, branch_name


async def adw_init(
    draft_file_path: str,
    run_id: str = None,
    issue_id: str = None,
    agent_type: AgentType = AgentType.CLAUDE
) -> Tuple[str, str, str, DraftClass]:
    """Initialize the Agentic Development Workflow.

    Args:
        draft_file_path: Path to the draft file to process
        run_id: Optional run ID (generated if not provided)
        issue_id: Optional issue ID for branch naming
        agent_type: The agent type to use (default: CLAUDE)

    Returns:
        Tuple of (run_id, draft_destination_path, branch_name, draft_class)
    """
    logger = logging.getLogger(__name__)

    # Validate draft file exists
    if not Path(draft_file_path).exists():
        logger.error("Draft file not found: %s", draft_file_path)
        raise FileNotFoundError(f"Draft file not found: {draft_file_path}")

    # Step 1: Generate run ID if not provided
    if not run_id:
        console.print("[cyan]Step 1:[/cyan] Generating run ID...")
        logger.debug("Generating new run ID")
        run_id = generate_run_id()
        console.print(f"  Generated run ID: [bold]{run_id}[/bold]")
        logger.info("Generated run ID: %s", run_id)
    else:
        console.print(f"[cyan]Step 1:[/cyan] Using provided run ID: [bold]{run_id}[/bold]")
        logger.info("Using provided run ID: %s", run_id)

    # Initialize logging with run-specific log file
    setup_logging(run_id)
    logger = logging.getLogger(__name__)
    logger.info("="*60)
    logger.info("ADW Initialization started - Run ID: %s", run_id)
    logger.info("Draft: %s | Agent: %s", draft_file_path, agent_type.value)
    logger.info("="*60)

    # Steps 2-4: Set up folder and read draft
    draft_destination_path, draft_text = _setup_run_folder_and_draft(run_id, draft_file_path)

    # Steps 5-7: Classify and create branch
    draft_class, branch_name = await _classify_and_create_branch(
        run_id, draft_text, issue_id, agent_type
    )

    # Print summary
    _print_initialization_summary(run_id, draft_destination_path, draft_class, branch_name)

    return run_id, draft_destination_path, branch_name, draft_class


async def main():
    """Main orchestration function for the ADW initialization flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Initialize the Agentic Development Workflow")
    parser.add_argument("--draft", required=True, help="Path to the draft file to process")
    parser.add_argument("--run_id", help="Optional run ID (generated if not provided)")
    parser.add_argument("--issue_id", help="Optional issue ID for branch naming")
    add_agent_argument(parser)

    args = parser.parse_args()

    try:
        agent_type = parse_agent_type(args)
        await adw_init(args.draft, args.run_id, args.issue_id, agent_type)
    except FileNotFoundError as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(1)
    except argparse.ArgumentError as e:
        print(f"Argument error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
