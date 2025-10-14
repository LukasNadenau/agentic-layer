"""Module for resolving failed tests using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
#   "junitparser",
# ]
# ///

from dotenv import load_dotenv
from claude_agent_sdk import query, ClaudeAgentOptions
from junitparser import TestSuite

load_dotenv()


async def resolve_test(test_suite: TestSuite) -> bool:
    """
    Resolves failed tests in a test suite by calling Claude Code with the /resolve_failed_test command.

    Args:
        test_suite: A junitparser TestSuite object containing failed tests

    Returns:
        bool: True if resolution completed successfully, False otherwise
    """
    # Stringify the test suite to XML format
    stringified_tests = test_suite.tostring()

    # Create the resolve_failed_test command
    command = f"/resolve_failed_test {stringified_tests}"

    # Set up options with bypass permissions
    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        setting_sources=["project"],
        model="haiku"
    )

    # Use query to send the slash command
    async for _ in query(prompt=command, options=options):
        pass

    print(f" Resolution command completed for test suite: {test_suite.name}")
    return True
