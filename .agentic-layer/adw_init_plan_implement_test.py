"""Agentic Development Workflow Complete Orchestration Script.

This script orchestrates the complete workflow from initialization through testing.
"""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "pydantic-ai",
#   "junitparser",
#   "rich",
# ]
# ///

import sys
import asyncio
import argparse
import logging

from console import console, phase_header, success, error
from logging_config import setup_logging
from adw_init import adw_init
from adw_plan import adw_plan
from adw_implement import adw_implement
from adw_test_loop import adw_test_loop
from get_or_create_folders import get_or_create_test_folder
from agent_types import AgentType
from arg_utils import add_agent_argument, parse_agent_type
from rich.panel import Panel


async def _run_planning_phase(
    run_id: str, draft_destination_path: str, draft_class, agent_type: AgentType
) -> str:
    """Execute the planning phase and return spec file path."""
    logger = logging.getLogger(__name__)
    console.print(phase_header("PLANNING", 2, 4))
    logger.info("Phase 2/4: Planning - Creating specification file")

    try:
        spec_file_path = await adw_plan(run_id, draft_destination_path, draft_class, agent_type)
        if not spec_file_path:
            error("Planning failed: spec file was not created")
            logger.error("Planning failed: spec file was not created")
            raise RuntimeError("Planning failed: spec file was not created")
        success(f"Spec created: {spec_file_path}")
        logger.info("Planning completed successfully. Spec file: %s", spec_file_path)
        return spec_file_path
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        error(f"Planning failed: {e}")
        logger.error("Planning failed: %s", e, exc_info=True)
        raise


async def _run_implementation_phase(spec_file_path: str, agent_type: AgentType):
    """Execute the implementation phase."""
    logger = logging.getLogger(__name__)
    console.print(phase_header("IMPLEMENTATION", 3, 4))
    logger.info("Phase 3/4: Implementation - Executing specification")

    try:
        success_impl = await adw_implement(str(spec_file_path), agent_type)
        if not success_impl:
            error("Implementation failed")
            logger.error("Implementation failed")
            raise RuntimeError("Implementation failed")
        success("Implementation completed")
        logger.info("Implementation completed successfully")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        error(f"Implementation failed: {e}")
        logger.error("Implementation failed: %s", e, exc_info=True)
        raise


async def _run_testing_phase(run_id: str, spec_file_path: str, agent_type: AgentType):
    """Execute the testing phase."""
    logger = logging.getLogger(__name__)
    console.print(phase_header("TESTING", 4, 4))
    logger.info("Phase 4/4: Testing - Running test validation loop")

    try:
        test_folder = get_or_create_test_folder(run_id)
        success_test = await adw_test_loop(str(test_folder), str(spec_file_path), agent_type)
        if not success_test:
            error("Testing failed: not all tests passed")
            logger.error("Testing failed: not all tests passed")
            raise RuntimeError("Testing failed: not all tests passed")
        success("All tests passed")
        logger.info("Testing completed successfully - all tests passed")
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        error(f"Testing failed: {e}")
        logger.error("Testing failed: %s", e, exc_info=True)
        raise


async def adw_complete(
    draft_file_path: str,
    run_id: str = None,
    issue_id: str = None,
    agent_type: AgentType = AgentType.CLAUDE
) -> bool:
    """Execute the complete ADW workflow.

    Args:
        draft_file_path: Path to the draft file to process
        run_id: Optional run ID (generated if not provided)
        issue_id: Optional issue ID for branch naming

    Returns:
        bool: True if the entire workflow completed successfully, False otherwise
    """
    # Display initial header (before logging setup since we don't have run_id yet)
    console.print(Panel.fit(
        "[bold cyan]AGENTIC DEVELOPMENT WORKFLOW[/bold cyan]\n"
        "[white]Complete Orchestration[/white]",
        border_style="cyan"
    ))

    # Phase 1: Initialize
    console.print(phase_header("INITIALIZATION", 1, 4))
    console.rule("[cyan]Starting initialization...[/cyan]")

    try:
        run_id, draft_destination_path, branch_name, draft_class = await adw_init(
            draft_file_path, run_id, issue_id
        )
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        error(f"Initialization failed: {e}")
        return False

    # Set up logging (after we have run_id)
    setup_logging(run_id)
    logger = logging.getLogger(__name__)
    logger.info("="*60)
    logger.info("ADW Complete workflow started - Run ID: %s", run_id)
    logger.info("Draft: %s | Branch: %s | Classification: %s",
                draft_file_path, branch_name, draft_class)
    logger.info("="*60)

    try:
        # Phase 2-4: Plan, Implement, Test
        spec_file_path = await _run_planning_phase(
            run_id, draft_destination_path, draft_class, agent_type
        )
        await _run_implementation_phase(spec_file_path, agent_type)
        await _run_testing_phase(run_id, spec_file_path, agent_type)

        # Success summary
        console.print(Panel.fit(
            f"[bold green]✓ WORKFLOW COMPLETED SUCCESSFULLY[/bold green]\n\n"
            f"[cyan]Run ID:[/cyan] {run_id}\n"
            f"[cyan]Branch:[/cyan] {branch_name}\n"
            f"[cyan]Classification:[/cyan] {draft_class}\n"
            f"[cyan]Spec File:[/cyan] {spec_file_path}",
            border_style="green",
            title="[bold]Success[/bold]"
        ))
        logger.info("="*60)
        logger.info("COMPLETE WORKFLOW FINISHED SUCCESSFULLY")
        logger.info("Run ID: %s | Branch: %s | Spec: %s", run_id, branch_name, spec_file_path)
        logger.info("="*60)
        return True
    except (FileNotFoundError, ValueError, RuntimeError):
        return False


async def main():
    """Main orchestration function for the complete ADW flow."""
    parser = argparse.ArgumentParser(
        description="Execute the complete Agentic Development Workflow: "
        "init → plan → implement → test"
    )
    parser.add_argument("--draft", required=True, help="Path to the draft file to process")
    parser.add_argument("--run_id", help="Optional run ID (generated if not provided)")
    parser.add_argument("--issue_id", help="Optional issue ID for branch naming")
    add_agent_argument(parser)

    args = parser.parse_args()

    try:
        agent_type = parse_agent_type(args)
        workflow_success = await adw_complete(args.draft, args.run_id, args.issue_id, agent_type)
        if not workflow_success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
