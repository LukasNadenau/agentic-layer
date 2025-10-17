"""Module for implementing specification files using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import logging
from dotenv import load_dotenv
from claude_agent_sdk import query
from claude_options import get_default_claude_options

load_dotenv()


async def run_tests(test_result_folder: str) -> bool:
    """
    Runs tests calling Claude Code with the /test command.

    Args:
        run_id: The run identifier
        test_result_folder: Path to the test result folder

    Returns:
        bool: True when ready, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Running tests, results in: %s", test_result_folder)

    # Create the test command
    command = f"/test {test_result_folder}"
    logger.debug("Sending command: %s", command)

    # Use query to send the slash command
    options = get_default_claude_options(model="haiku")
    try:
        async for _ in query(prompt=command, options=options):
            pass
    except Exception as e:
        logger.error("Test execution failed: %s", e, exc_info=True)
        raise

    logger.info("Tests command completed")
    return True
