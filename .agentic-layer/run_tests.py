"""Module for implementing specification files using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions

load_dotenv()


async def implement_spec(run_id: str, test_result_folder: str) -> bool:
    """
    Runs tests calling Claude Code with the /test command.

    Args:
        run_id: The run identifier
        test_result_folder: Path to the test result folder

    Returns:
        bool: True when ready, False otherwise
    """
    # Create the test command
    command = f"/test {run_id} {test_result_folder}"

    # Set up options with bypass permissions
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        model="haiku"
    )

    # Use query to send the slash command
    async for _ in query(prompt=command, options=options):
        pass

    print(" Tests command completed")
    return True
