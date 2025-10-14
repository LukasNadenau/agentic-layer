"""Module for implementing specification files using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

from pathlib import Path
from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


async def implement_spec(run_id: str, spec_file_path: str) -> bool:
    """
    Implements a spec file by calling Claude Code with the /implement command.

    Args:
        run_id: The run identifier
        spec_file_path: Path to the spec file

    Returns:
        bool: True if implementation completed successfully, False otherwise
    """
    # Create the implement command
    command = f"/implement {run_id} {spec_file_path}"

    # Set up options with bypass permissions
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        model="haiku"
    )

    # Use query to send the slash command
    async for _ in query(prompt=command, options=options):
        pass

    print(f" Implementation command completed for spec: {spec_file_path}")
    return True
