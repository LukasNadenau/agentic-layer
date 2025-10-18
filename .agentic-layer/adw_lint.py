"""Agentic Development Workflow Linting Script.

This script orchestrates code quality checking for a workflow run.
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
from coding_agent import call_coding_agent
from agent_types import AgentType
from arg_utils import add_agent_argument, parse_agent_type

load_dotenv()


async def adw_lint(spec_file_path: str, agent_type: AgentType = AgentType.CLAUDE) -> bool:
    """
    Run linting by calling coding agent with the /lint command.

    Args:
        spec_file_path: Path to the spec file (provides context for fixes)
        agent_type: Type of coding agent to use (default: CLAUDE)

    Returns:
        bool: True if linting completed successfully, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting linting for spec: %s", spec_file_path)

    try:
        status_text = f"[cyan]{agent_type.value.capitalize()} is linting...[/cyan]"
        with console.status(status_text):
            await call_coding_agent(agent_type, "lint", [spec_file_path])
    except Exception as e:
        logger.error("Coding agent failed during linting: %s", e, exc_info=True)
        raise

    console.print(f"[green]✓[/green] Linting command completed for spec: {spec_file_path}")
    logger.info("Linting completed successfully for spec: %s", spec_file_path)
    return True


async def main():
    """Main orchestration function for the ADW linting flow."""
    parser = argparse.ArgumentParser(
        description="Run linting for Agentic Development Workflow"
    )
    parser.add_argument("--spec", required=True, help="Path to the spec file")
    add_agent_argument(parser)

    args = parser.parse_args()

    try:
        agent_type = parse_agent_type(args)
        success = await adw_lint(args.spec, agent_type)
        if not success:
            sys.exit(1)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
