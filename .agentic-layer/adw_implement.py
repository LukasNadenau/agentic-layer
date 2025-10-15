"""Agentic Development Workflow Implementation Script.

This script orchestrates the implementation of specification files for a workflow run.
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
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

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
    # Create the implement command
    command = f"/implement {spec_file_path}"

    # Set up options with bypass permissions
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        model="haiku"
    )

    # Use query to send the slash command
    async for _ in query(prompt=command, options=options):
        pass

    print(f"✓ Implementation command completed for spec: {spec_file_path}")
    return True


async def main():
    """Main orchestration function for the ADW implementation flow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Implement specification file for Agentic Development Workflow")
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
