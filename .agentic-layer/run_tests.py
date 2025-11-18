"""Module for implementing specification files using Claude Code."""
# /// script
# dependencies = [
#   "claude-agent-sdk",
#   "python-dotenv",
# ]
# ///

import logging
from dotenv import load_dotenv
from coding_agent import call_coding_agent
from agent_types import AgentType

load_dotenv()


async def run_tests(
    test_result_folder: str,
    agent_type: AgentType = AgentType.CLAUDE
) -> bool:
    """
    Runs tests calling the coding agent with the /test command.

    Args:
        test_result_folder: Path to the test result folder
        agent_type: The coding agent to use (CLAUDE or COPILOT)

    Returns:
        bool: True when ready, False otherwise
    """
    logger = logging.getLogger(__name__)
    logger.info("Running tests, results in: %s", test_result_folder)

    # Call the coding agent to run tests
    try:
        await call_coding_agent(
            agent_type, "test", [test_result_folder], model="haiku"
        )
    except Exception as e:
        logger.error("Test execution failed: %s", e, exc_info=True)
        raise

    logger.info("Tests command completed")
    return True
