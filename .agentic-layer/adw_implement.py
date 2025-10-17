"""Agentic Development Workflow Implementation Script.

This script orchestrates the implementation of specification files for a workflow run.
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
from dotenv import load_dotenv
from console import console
from claude_agent_sdk import query
from claude_options import get_default_claude_options

load_dotenv()


async def adw_implement(spec_file_path: str) -> bool:
    """
    Implements a spec file by calling Claude Code with the /implement command.

    Args:
        run_id: The run identifier
        spec_file_path: Path to the spec file

    Returns:
        bool: True if implementation completed successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting implementation for spec: %s", spec_file_path)

    # Create the implement command
    command = f"/implement {spec_file_path}"
    logger.debug("Sending command: %s", command)

    # Use query to send the slash command
    options = get_default_claude_options()
    try:
        with console.status("[cyan]Claude Code is implementing...[/cyan]"):
            async for message in query(prompt=command, options=options):
                logger.debug("Claude code message: %s", message)
    except Exception as e:
        logger.error("Claude Code SDK query failed during implementation: %s", e, exc_info=True)
        raise

    console.print(f"[green]✓[/green] Implementation command completed for spec: {spec_file_path}")
    logger.info("Implementation completed successfully for spec: %s", spec_file_path)
    return True


async def main():
    """Main orchestration function for the ADW implementation flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Implement specification file for Agentic Development Workflow"
    )
    parser.add_argument("--spec", required=True, help="Path to the spec file")

    args = parser.parse_args()

    try:
        success = await adw_implement(args.spec)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
